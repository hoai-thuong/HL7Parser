from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_from_record(record):
    # Tạo một tài liệu PDF
    c = canvas.Canvas("patient_test_results.pdf", pagesize=letter)

    # Thêm logo và header
    c.drawImage("lg.png", 520, 730, width=50, height=50)
    header_text = "Test Results Report"
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 750, header_text)  # Thay đổi tọa độ y thành 750

    # Lấy thông tin từ record
    patient_name = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_5 - PATIENT_NAME", "")
    patient_id = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_2 - PATIENT_ID", "")
    patient_dob = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_7 - DATE_TIME_OF_BIRTH", "")
    gender = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_8 - ADMINISTRATIVE_SEX", "")
    address = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_11 - PATIENT_ADDRESS", "")
    contact = record.get("ORU_R01_PATIENT", [{}])[0].get("PID_13 - PHONE_NUMBER_HOME", "")

    # Thêm thông tin vào PDF
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Patient Name: {patient_name}")
    c.drawString(50, 710, f"Patient ID: {patient_id}")
    c.drawString(50, 690, f"Date of Birth: {patient_dob}")
    c.drawString(50, 670, f"Gender: {gender}")
    c.drawString(50, 650, f"Address: {address}")
    c.drawString(50, 630, f"Contact: {contact}")

    # Vẽ đường gạch ngang
    c.line(50, 620, 550, 620)  # Vẽ đường gạch ngang tại y = 620

    # Lấy thông tin từ record
    description = record.get("ORU_R01_ORDER_OBSERVATION", [{}])[1].get("OBR_4 - UNIVERSAL_SERVICE_IDENTIFIER", "")
    hospital_id = record.get("ORU_R01_ORDER_OBSERVATION", [{}])[1].get("OBR_2 - PLACER_ORDER_NUMBER", "")
    lab_id = record.get("ORU_R01_ORDER_OBSERVATION", [{}])[1].get("OBR_3 - FILLER_ORDER_NUMBER", "")
    collect_time = record.get("ORU_R01_ORDER_OBSERVATION", [{}])[1].get("OBR_7 - OBSERVATION_DATE_TIME", "")
    result_time = record.get("ORU_R01_ORDER_OBSERVATION", [{}])[1].get("OBR_14 - SPECIMEN_RECEIVED_DATE_TIME", "")

    # Thêm thông tin vào PDF
    c.drawString(50, 600, f"Description: {description}")
    c.drawString(50, 580, f"Hospital ID: {hospital_id}")
    c.drawString(50, 560, f"Lab ID: {lab_id}")
    c.drawString(50, 540, f"Collection Time: {collect_time}")
    c.drawString(50, 520, f"Result Time: {result_time}")

    # Vẽ đường gạch ngang
    c.line(50, 510, 550, 510)  # Vẽ đường gạch ngang tại y = 510

    # Lấy thông tin từ record
    comp = record.get("ORU_R01_OBSERVATION", [{}])[0].get("OBX_3 - OBSERVATION_IDENTIFIER", "")
    value = record.get("ORU_R01_OBSERVATION", [{}])[0].get("OBX_5 - OBSERVATION_VALUE", "")
    unit = record.get("ORU_R01_OBSERVATION", [{}])[0].get("OBX_6 - UNITS", "")
    rng = record.get("ORU_R01_OBSERVATION", [{}])[0].get("OBX_7 - REFERENCES_RANGE", "")
    conclu = record.get("ORU_R01_OBSERVATION", [{}])[0].get("OBX_9 - PROBABILITY", "")

    # Thêm thông tin vào PDF
    c.drawString(50, 490, f"Composition_Description: {comp}")
    c.drawString(50, 470, f"Observation_Value: {value} {unit}")
    c.drawString(50, 450, f"Range: {rng}")
    c.drawString(50, 430, f"Conclusion: {conclu}")

    # Lưu và đóng tài liệu PDF
    c.save()

# Test với dữ liệu mẫu
import pymongo

# Kết nối tới MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["hl7_db"]
collection = db["hl7_messages"]

# Lấy bản ghi đầu tiên từ MongoDB
record = collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])

# Tạo tài liệu PDF từ bản ghi đầu tiên
create_pdf_from_record(record)
