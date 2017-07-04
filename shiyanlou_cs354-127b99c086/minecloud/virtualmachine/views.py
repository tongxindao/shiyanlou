#! /usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .forms import AddVirtualMachineForm
from .models import VirtualMachine
from ..extension import db
from ..template import Template
from ..user import User, USER_NORMAL, USER_ADMIN
from ..host import Host, HOST_OK, HOST_ERROR
from ..image import Image

import time

import xml.etree.ElementTree as ET
import libvirt

import sys

import os

import datetime

reload(sys)
sys.setdefaultencoding('utf8')

virtualmachine = Blueprint('virtualmachine', __name__, url_prefix='/virtualmachines')

@virtualmachine.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        form = AddVirtualMachineForm()
        if current_user.type_code == USER_NORMAL:
            virtualmachine_list = VirtualMachine.query.filter(VirtualMachine.owner_id == current_user.id).all()
        else:
            virtualmachine_list = VirtualMachine.query.filter().all()
        return render_template("virtualmachine/index.html", form=form, virtualmachine_list=virtualmachine_list)
    else:
        form = AddVirtualMachineForm(request.form)
        if form.validate_on_submit():
            if Template.query.filter(Template.id == int(str(form.template_id)[-3])).first() is not None:
                if len( VirtualMachine.query.filter(str(VirtualMachine.name) == str(form.name).split('"')[-2] ).all() ) == 0:
                    virtualmachine_instance = VirtualMachine()
                    form.populate_obj(virtualmachine_instance)
                    virtualmachine_instance.owner_id = current_user.id
                    virtualmachine_instance.create_time = time.strftime("%Y-%m-%d %H:%M:%S")

                    CreateVM(virtualmachine_instance.owner_id, virtualmachine_instance.template_id, virtualmachine_instance.name)

                    db.session.add(virtualmachine_instance)
                    db.session.commit()
                    return redirect(url_for('virtualmachine.index'))
                else:
                    return render_template("virtualmachine/error.html", info="虚拟机名为 '"+ str(form.name).split('"')[-2] +"' 已存在！")
            return render_template("virtualmachine/error.html", info="模板ID为 '" + str(form.template_id)[-3] + "' 已存在！")

@virtualmachine.route('/<int:virtualmachine_id>/delete', methods=['GET'])
@login_required
def delete_virtualmachine(virtualmachine_id):
    virtualmachine_instance = VirtualMachine.query.filter(VirtualMachine.id==virtualmachine_id).first()
    if virtualmachine_instance:
        db.session.delete(virtualmachine_instance)
        db.session.commit()
    return redirect(url_for('virtualmachine.index'))

def CreateVM(UserID, TemplateID, VMName):
    # Step1：从Template中获取虚拟机的配置信息
    image = GetImageFromTemplate(TemplateID)
    cpu = GetCPUFromTemplate(TemplateID)
    memory = GetMemoryFromTemplate(TemplateID)

    # Step2：获取可用的的服务器
    host_list = GetHosts()
    target_host = GetBestHostFromHosts(host_list)

    # Step3：创建虚拟机的磁盘文件
    # 磁盘文件可以使用qemu-img采用QCOW2的方式创建，执行方式可以使用SSH远程执行
    disk_file = CreateVMDiskWithSSH(target_host, image)

    # Step4：生成虚拟机的XML配置文件
    xml_disk_file = '/home/shiyanlou/Code/shiyanlou_cs354/virtscripts/minevm1.xml'
    XMLFile = GetVMXMLFile(VMName, xml_disk_file, cpu, memory)

    # Step5：创建虚拟机对象并初始化
    VM = VirtualMachine()
    VM.name = VMName
    VM.cpu = cpu
    
    # VM.host_id = target_host.id
    VM.host_id = Host.id
    VM.image_id = image.id
    VM.owner_id = UserID
    VM.status_code = VM_INIT

    # Step6：创建并启动虚拟机
    libvirt_host = GetLibvirtHost(target_host)
    domain = libvirt_host.createXML(XMLFile)
    if domain.state()[0] == 5: # 如果创建成功则更新虚拟机状态:
        VM.status_code = VM_RUNNING

    # Step7：更新数据库
    db.session.commit()

def GetImageFromTemplate(TemplateID):
    image_id = Template.query.filter(Template.id == TemplateID).first().id
    return Image.query.filter(Image.id == image_id).first()

def GetCPUFromTemplate(TemplateID):
    return Template.query.filter(Template.id == TemplateID).first().cpu_number
        
def GetMemoryFromTemplate(TemplateID):
    return Template.query.filter(Template.id == TemplateID).first().mem_size
    
def GetHosts():
    return Host.query.filter(Host.status_code == HOST_OK).all()
    
# 遍历扫描，查询每个服务器上的虚拟机数量，获取最小值的服务器，并把服务器对象返回。    
def GetBestHostFromHosts(host_list):
    return host_list
'''
    min_count = 666
    for host in host_list:
        if host.vms.count() < min_count:
            min_count = host.vms.count()
            #min_host = host
    return Host.query.filter(Host.vms.count() == min_count).first()
'''
    
def CreateVMDiskWithSSH(target_host, image):
    # 获取镜像文件的路径
    image_file = image.path 
        
    # 指定存放虚拟机磁盘的目录
    disk_path = "/home/shiyanlou/Code/shiyanlou_cs354/qemu-disk/"
        
    # 磁盘名用虚拟机的ID(也可以用随机值)
    # disk_name = GetUUID()
    disk_name = 'minevm1.qcow2'
        
    # 将要生成的磁盘文件路径
    disk_file = os.path.join(disk_path, disk_name)
      
    # disk_file = '/home/shiyanlou/Code/shiyanlou_cs354/qemu-disk/minevm1.qcow2'  
    # 创建磁盘文件的命令
    cmd = "qemu-img create -f qcow2 %s -b %s" % (disk_file, image_file)
        
    # ssh远程到目标服务器执行cmd，可以选择很多种方式执行
    target_host_ip = '127.0.0.1'
    ssh_cmd = 'ssh minecloud@%s "%s"' % (target_host_ip, cmd)
    os.popen(ssh_cmd).readlines()
        
    # 返回虚拟机磁盘文件路径
    return disk_file
        
def GetVMXMLFile(VMName, disk_file, cpu, memory):
    vm_xml = ET.parse(disk_file)
    vm_xml_root = vm_xml.getroot()
            
    for name in vm_xml_root.iter('name'):
        name.text = VMName
    
    for vcpu in vm_xml_root.iter('vcpu'):
        vcpu.text = str(cpu)
    
    for memory in vm_xml_root.iter('memory'):
        memory.text = str(memory)
                
    for disk_source in vm_xml_root.iterfind('devices/disk/source'):
        disk_source.set('file', disk_file)
                
    vm_create_path = os.path.join(os.getcwd(), VMName+'.xml')
    vm_xml.write(vm_create_path)
        
    return vm_xml
        
def GetLibvirtHost(target_host):
    target_host_ip = '127.0.0.1'
    hostUri = 'qemu+ssh://shiyanlou@%s/system' % target_host_ip
    return libvirt.open(hostUri)
        
# 获取VM的ID 
def GetUUID():  
    #return session.query.filter().last().id
    return datetime.datetime.now().strftime('%Y-%m-%d')

'''
def StartVM(VMID):
    # Step1：获取虚拟机对象
    vm = GetVMByID(VMID)
    # Step2：获取Libvirt对象
    domain = GetLibvirtDomainByVM(vm)
    # Step3：执行Libvirt API进行操作
    domain.create()

def ShutdownVM(VMID):
    # Step1：获取虚拟机对象
    vm = GetVMByID(VMID)
    # Step2：获取Libvirt对象
    domain = GetLibvirtDomainByVM(vm)
    # Step3：执行Libvirt API进行操作
    domain.destroy()

def RebootVM(VMID):
    # Step1：获取虚拟机对象
    vm = GetVMByID(VMID)
    # Step2：获取Libvirt对象
    domain = GetLibvirtDomainByVM(vm)
    # Step3：执行Libvirt API进行操作
    domain.reboot()

def deleteVM(VMID):
    # Step1：获取虚拟机对象
    vm = GetVMByID(VMID)
    # Step2：获取Libvirt对象
    domain = GetLibvirtDomainByVM(vm)
    # Step3：执行Libvirt API进行操作
    domain.destroy()
    domain.undefine()
    # Step4：删除虚拟机磁盘文件，可以使用SSH远程执行删除命令
    DeleteDiskFileWithSSH(vm.host)
    # Step5：更新数据库
    db.session.delete(vm)
    db.session.commit()

def GetVNCPort(host, vmname):
    domain = host.lookupByName(vmname)
    xml = domain.XMLDesc()
    reg = '\' port=\'(.*)\' a'
    vncport = re.search(reg, xml)
    if vncport == None:
        return None
    return vncport.group(1)

def CreateVMToken(vm):
    # Step1：获取VMC端口
    port = GetVNCPort(vm)
    # Step2：创建Token文件内容
    # Token文件格式：`token: host:port`
    token_string = GenerateTokenString(vm.host, port)
    # Step3：写入Token文件，可以使用SSH远程执行echo命令来创建token文件，文件命名可以使用VMID，方便后续的删除操作
    CreateTokenFileWithSSH(vm.host, token_string)

def DeleteVMToken(vm):
    # Step1：删除Token文件，可以使用SSH远程执行rm命令删除
    DeleteTokenFileWithSSH(vm.host, vm.id)

def checkHost(host):
    # Step1：测试服务器是否可以ping通
    status_code = PingTest(host)
    # Step2：测试服务器SSH连接
    status_code = SSHTest(host)
    # Step3：测试服务器Libvirt服务
    status_code = LibvirtTest(host)
'''
