import zipfile
import os
import glob
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom

# 加载XML文件
def modify_xmlfile (file_path):
    # tree = ET.parse(file_path)
    # root = tree.getroot()
    root = ET.fromstring(file_path)
    # 遍历XML树，查找命名空间
    namespace = None
    for elem in root:
    # for elem in root: in root.iter():
        tag = elem.tag
        if '}' in tag:
            namespace = tag.split('}')[0][1:]
            break

    # 定义命名空间
    ns = {'ns': namespace}
    # 查找 <environments> 元素
    environment = root.find('ns:environments', ns)
    env_list = [ 'serveros.openeuler2203sp1x64' , 'serveros.openeuler2203x64' ]
    # 查找是否存在 <environment id="serveros.openeuler2203sp1x64"/> 元素
    for id_value in env_list:
        # print(id_value)
        env_id='ns:environment[@id="{}"]'.format(id_value)
        existing_env = environment.find(env_id, ns)
    # 如果不存在，则插入该元素
        # print(existing_env)
        if existing_env is None:
            new_env = ET.Element('environment', {'id': id_value })
            environment.append(new_env)
            # 重新格式化XML树
            # ET.indent(new_env, space='  ', level=0)
    # 重新注册命名空间，将前缀映射为空字符串
    ET.register_namespace('', namespace)
    
    #转换成字符串删除多余的换行
    xml_dom = xml.dom.minidom.parseString(ET.tostring(root))
    xml_str = xml_dom.toprettyxml(indent="  ", encoding='UTF-8')
    lines = xml_str.split(b"\n")
    #去除空白字符并换行
    xml_str = b"\n".join(line for line in lines if line.strip())
    # # 保存修改后的 XML 文件
    # with open(file_path, 'wb') as f:
    #     f.write(xml_str)
    #返回xml信息
    return  xml_str


# 定义 ZIP 文件路径
# zip_file_path = 'your_zip_file.zip'

def process_zip_file(zip_file_path,output_folder,file_name):
    # 打开原始 ZIP 文件和新的 ZIP 文件
    with zipfile.ZipFile(zip_file_path, 'r') as original_zip, zipfile.ZipFile(os.path.join(output_folder, zip_file_path), 'w') as updated_zip:

        # 遍历原始 ZIP 文件中的所有文件
        for item in original_zip.infolist():
            #打开versioninfo.xml文件
            if item.filename == file_name:
                print(f"{file_name} exist {zip_file_path} ")
                with original_zip.open(item) as versioninfo_path:
                    #修改versioninfo.xml文件
                    content = modify_xmlfile(versioninfo_path.read())
            # 将文件内容写入更新后的 ZIP 文件
                updated_zip.writestr(item, content)
            else:
                data=original_zip.read(item.filename)
                updated_zip.writestr(item,data)

    # 更新后的 ZIP 文件保存在 TEMPFILE 文件夹下的 updated.zip 文件中
if os.path.exists('TEMP_FILE'):
    shutil.rmtree('TEMP_FILE')
os.makedirs('TEMP_FILE', exist_ok=True)
out_file= 'TEMP_FILE'  
xml_file_name = 'META-INF/versioninfo.xml'
# version_file_path='META-INF'
completed_tasks = 0
zip_files = glob.glob('*.zip')
for zip_file in zip_files:
    # 更新计数器 
    completed_tasks += 1 
    # 计算进度百分比 
    progress = completed_tasks / len(zip_files) * 100
    # 打印进度 
    print(f"Progress: {progress:.2f}%") 
    process_zip_file(zip_file,out_file,xml_file_name)
    print(f"{zip_file}  has been updated ")
    
# 保持命令窗口打开 
input("task is over Press Enter to exit...")   