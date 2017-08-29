import os
import re

# module sign
pattern = r'{{(.*?)}}'

def parse_args(obj):
    '''
    parse template
    '''

    # gets matched object
    comp = re.compile(pattern)

    # find all of the matched result
    ret = comp.findall(obj)

    # if matched and return it, or not then return null tuple
    return ret if ret else ()

def replace_template(app, path, **options):
    '''
    return template content
    '''

    # default return content, return when not found local template file
    content = '<h1>Not Found Template</h1>'

    # gets template file local path
    path = os.path.join(app.template_folder, path)

    # if path exist, then start parse replace
    if os.path.exists(path):

        # gets template file content
        with open(path, 'rb') as f:
            content = f.read().decode()

        # parse all of the sign
        args = parse_args(content)

        # if replace content not null, start replace
        if options:

            # ergodic all of the replace data, start replace
            for arg in args:

                # gets key from the sign
                key = arg.strip()

                # if key exist in replace data, then replace data, or not then replace null
                content = content.replace("{{%s}}" % arg, str(options.get(key, '')))
    
    # return template content
    return content
