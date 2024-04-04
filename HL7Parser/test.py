from hl7apy import parser
from hl7apy.core import Group, Segment
from hl7apy.exceptions import UnsupportedVersion
import pymongo
import re
# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hl7_db"]
collection = db["hl7_messages"]

hl7 = open("hl7.txt", "r").read()

try:
    msg = parser.parse_message(hl7.replace('\n', '\r'), find_groups=True, validation_level=2)
except UnsupportedVersion:
    msg = parser.parse_message(hl7.replace('\n', '\r'), find_groups=True, validation_level=2)

indent = "    "
indent_seg = "    "
indent_fld = "        "
print(msg.children)
def subgroup(group, indent):
    indent = indent + "    "
    print(indent, group)
    for group_segment in group.children:
        if isinstance(group_segment, Group):
            subgroup(group_segment)
        else:
            print(indent_seg, indent, group_segment)
            for attribute in group_segment.children:
                print(indent_fld, indent, attribute, attribute.value)
import re

def process_name(name):
    # Xử lý phần tên của trường
    name = re.search(r'\((.*?)\)', name).group(1)
    return name

def process_value(value):
    # Thay thế dấu ^ thành khoảng trắng
    value = value.replace('^', ' ')
    # Thay thế các khoảng trắng liên tiếp thành một khoảng trắng duy nhất
    value = re.sub(r'\s+', ' ', value)
    return value

def process_group(group, msg_dict):
    for group_segment in group.children:
        if isinstance(group_segment, Group):
            process_group(group_segment, msg_dict)  # Gọi đệ quy để xử lý các nhóm con
        else:
            segment_dict = {}
            for attribute in group_segment.children:
                # Xử lý phần tên và giá trị của trường
                field_name = attribute.name + " - " +  process_name(str(attribute))
                field_value = process_value(attribute.value)
                segment_dict[field_name] = field_value
            if group.name not in msg_dict:
                msg_dict[group.name] = [segment_dict]
            else:
                msg_dict[group.name].append(segment_dict)

def save_to_mongodb(msg):
    msg_dict = {}
    for segment in msg.children:
        if isinstance(segment, Segment):
            segment_dict = {}
            for attribute in segment.children:
                # Xử lý phần tên và giá trị của trường
                field_name = attribute.name + " - " + process_name(str(attribute))
                field_value = process_value(attribute.value)
                segment_dict[field_name] = field_value
            if segment.name not in msg_dict:
                msg_dict[segment.name] = [segment_dict]
            else:
                msg_dict[segment.name].append(segment_dict)
        elif isinstance(segment, Group):
            process_group(segment, msg_dict)

    # Lưu dictionary của tin nhắn vào MongoDB
    collection.insert_one(msg_dict)
    print("Message saved to MongoDB")


save_to_mongodb(msg)

