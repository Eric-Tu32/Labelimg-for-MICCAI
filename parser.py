import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import re

#創建空白XML
def create_pretty_xml(filename, folder_name = "", image_name = "", image_path = "", width=256, height=256, depth=3):
    # Root element
    annotation = ET.Element("annotation")
    
    # Sub-elements
    ET.SubElement(annotation, "folder").text = folder_name
    ET.SubElement(annotation, "filename").text = image_name
    ET.SubElement(annotation, "path").text = image_path
    
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)
    
    ET.SubElement(annotation, "segmented").text = "0"
    
    # Pretty-print the XML
    rough_string = ET.tostring(annotation, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="\t")
    
    # Write the pretty XML to a file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Pretty XML created: {filename}")

#添加object
def append_object(filename, coordinates = tuple(), name = "CMB", pose="Unspecified", truncated="0", difficult="0"):
    # Parse the existing XML file
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Create a new <object> element
    obj = ET.Element("object")
    ET.SubElement(obj, "name").text = name
    ET.SubElement(obj, "pose").text = pose
    ET.SubElement(obj, "truncated").text = truncated
    ET.SubElement(obj, "difficult").text = difficult
    
    bndbox = ET.SubElement(obj, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(coordinates[0])
    ET.SubElement(bndbox, "ymin").text = str(coordinates[1])
    ET.SubElement(bndbox, "xmax").text = str(coordinates[2])
    ET.SubElement(bndbox, "ymax").text = str(coordinates[3])
    
    # Append the new <object> to the root
    root.append(obj)
    
    # Pretty-print the XML
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="\t")
    
    # Save the updated XML back to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Pretty object appended to: {filename}")

#從XML找出bounding boxes (output: [(xmin, ymin, xmax, ymax), (...), (...)])
def extract_bounding_boxes(xml_file):
    bounding_boxes = []
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find all <object> elements
    for obj in root.findall("object"):
        # Locate the <bndbox> element within each <object>
        bndbox = obj.find("bndbox")
        if bndbox is not None:
            # Extract xmin, ymin, xmax, ymax
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)
            # Append the bounding box as a tuple
            bounding_boxes.append((xmin, ymin, xmax, ymax))
    
    return bounding_boxes

'''
例子: 目錄有0.xml, 4.xml, 5.xml, 7.xml, 13.xml。MRI厚度64張。
創建1, 3, 6, 8, 12, 14.xml
把原始五個檔案的bounding box寫入鄰近的xml
'''
def process_directory(dir = str(), last_index = 63):
    num_list = list() #eg: [0, 4, 5, 7, 13] depth = 32
    original_bbs = dict() #eg: {0: [(bb)], 4: [(bb)], 5:[(bb)]...}

    for filename in os.listdir(dir):
         if filename.endswith(".xml"):
            match = re.match(r"(\d+)\.xml", filename)
            if match:
                num_list.append(int(match.group(1)))
                original_bbs[int(match.group(1))] = extract_bounding_boxes(os.path.join(dir, filename))

    for i in range(len(num_list)):
        print(f"Pivot File: {num_list[i]}.xml")

        prev = num_list[i] - 1
        nxt = num_list[i] + 1

        prev_bbs, nxt_bbs = list(), list()

        if prev >= 0:
            prev_file_path = os.path.join(dir, f"{prev}.xml")
            if prev not in num_list:
                num_list.append(prev)
                create_pretty_xml(prev_file_path)
            prev_bbs = extract_bounding_boxes(prev_file_path)
            for box in original_bbs[num_list[i]]:
                if box not in prev_bbs:
                    append_object(prev_file_path, box)
        
        if nxt <= last_index:
            nxt_file_path = os.path.join(dir, f"{nxt}.xml")
            if nxt not in num_list:
                num_list.append(nxt)
                create_pretty_xml(nxt_file_path)
            nxt_bbs = extract_bounding_boxes(nxt_file_path)
            for box in original_bbs[num_list[i]]:
                if box not in nxt_bbs:
                    append_object(nxt_file_path, box)
            

if __name__ == "__main__":
    xml_directory = r"C:\Users\eric\Downloads\Mri of knee"

    #init example
    # create_pretty_xml(os.path.join(xml_directory, "0.xml"))
    # create_pretty_xml(os.path.join(xml_directory, "4.xml"))
    # create_pretty_xml(os.path.join(xml_directory, "5.xml"))
    # create_pretty_xml(os.path.join(xml_directory, "7.xml"))
    # create_pretty_xml(os.path.join(xml_directory, "13.xml"))
    # append_object(os.path.join(xml_directory, "0.xml"), (0, 0, 2, 2))
    # append_object(os.path.join(xml_directory, "0.xml"), (1, 1, 3, 3))
    # append_object(os.path.join(xml_directory, "4.xml"), (4, 4, 8, 8))
    # append_object(os.path.join(xml_directory, "4.xml"), (44, 44, 46, 46))
    # append_object(os.path.join(xml_directory, "5.xml"), (15, 15, 25, 25))
    # append_object(os.path.join(xml_directory, "7.xml"), (7, 7, 14, 14))
    # append_object(os.path.join(xml_directory, "13.xml"), (13, 13, 26, 26))


    #印出原本的bounding boxes
    for file in os.listdir(xml_directory):
        name, extension = os.path.splitext(file)
        if extension == ".xml":
            print(os.path.basename(file), extract_bounding_boxes(os.path.join(xml_directory, file)))

    process_directory(xml_directory)
    print("Complete")

    #印出後來的
    for file in os.listdir(xml_directory):
        print(os.path.basename(file), extract_bounding_boxes(os.path.join(xml_directory, file)))
