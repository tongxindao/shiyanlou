import libvirt
import re

def CreateVM(UserID, TemplateID, VMName):
    # Step1：从Template中获取虚拟机的配置信息
    image = GetImageFromTemplate(TemplateID)
    cpu = GETCPUFromTemplate(TemplateID)
    memory = GetMemoryFromTemplate(TemplateID)

    # Step2：获取可用的的服务器
    host_list = GetHosts()
    target_host = GetBestHostFromHosts(host_list)

    # Step3：创建虚拟机的磁盘文件
    # 磁盘文件可以使用qemu-img采用QCOW2的方式创建，执行方式可以使用SSH远程执行
    disk_file = CreateVMDiskWithSSH(target_host, image)

    # Step4：生成虚拟机的XML配置文件
    XMLFile = GetVMXMLFile(VMName, disk_file, cpu, memory)

    # Step5：创建虚拟机对象并初始化
    VM = VirtualMachine()
    VM.name = VMName
    VM.cpu = cpu
    ...
    VM.host_id = target_host.id
    VM.image_id = image.id
    VM.owner_id = UserID
    VM.status_code = VM_INIT

    # Step6：创建并启动虚拟机
    libvirt_host = GetLibvirtHost(target_host)
    domain = libvirt_host.createXML(XMLFile)
    if 如果创建成功则更新虚拟机状态:
        VM.status_code = VM_RUNNING

    # Step7：更新数据库
    db.session.commit()

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
