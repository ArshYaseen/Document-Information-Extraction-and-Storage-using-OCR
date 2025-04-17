import cv2
import pytesseract
from PIL import Image

def extract_roi(image_path, roi_coordinates):
    # Load the image
    image = cv2.imread(image_path)
    
    # Get the dimensions of the image
    height, width, _ = image.shape
    
    # Normalize ROI coordinates based on image dimensions
    normalized_rois = []
    for coordinates in roi_coordinates:
        x1, y1, x2, y2 = coordinates
        norm_x1, norm_y1 = int(x1 * width), int(y1 * height)
        norm_x2, norm_y2 = int(x2 * width), int(y2 * height)
        normalized_coordinates = (norm_x1, norm_y1, norm_x2, norm_y2)
        normalized_rois.append(normalized_coordinates)
    
    # Extract ROIs based on normalized coordinates
    rois = []
    for coordinates in normalized_rois:
        x1, y1, x2, y2 = coordinates
        roi = image[y1:y2, x1:x2]
        rois.append(roi)
    
    return rois

def perform_ocr_on_rois(rois):
    extracted_texts = []
    for i, roi in enumerate(rois):
        # Convert the ROI to PIL Image format
        pil_image = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        
        # Perform OCR on the ROI
        text = pytesseract.image_to_string(pil_image)
        
        # Save or process each ROI as needed
        cv2.imwrite(f'roi_{i+1}.jpg', roi)
        extracted_texts.append(text)
    
    return extracted_texts

# Example usage
image_path = 'doc1.jpg'

# Custom coordinates for ROIs as percentages (x1, y1, x2, y2)
roi_coordinates = [
    (0.381, 0.027, 0.524, 0.068),  # 1 (Classification)
    (0.095, 0.058, 0.905, 0.120),  # 2 (letter pad head)
    (0.286, 0.108, 0.667, 0.142),  # 3 (Exchange or Contact detail of dte)
    (0.029, 0.135, 0.477, 0.174),  # 4 (Reference NO)
    (0.619, 0.135, 0.953, 0.181),  # 5 (Date)
    (0.029, 0.160, 0.857, 0.197),  # 6 (Subject)
    (0.024, 0.189, 0.999, 0.508),  # 7 (Description)
    (0.024, 0.529, 0.667, 0.821),  # 8 (Distribution list)
    (0.305, 0.812, 0.727, 0.917),  # 9 (CC)
    (0, 0.805, 0.124, 1),          # 10 (Diary No)
    (0.625, 0.434, 0.953, 0.591),  # 11 (signature)
    (0.619, 0.566, 0.857, 0.640),  # 12 (Comments)
    (0.619, 0.676, 0.857, 1)       # 13 (Handwritten Comments/ Signatures)
]

rois = extract_roi(image_path, roi_coordinates)
extracted_texts = perform_ocr_on_rois(rois)

# Print the extracted texts
for i, text in enumerate(extracted_texts):
    print(f'Text from ROI {i+1}:')
    print(text)
    print('--------------------------------')

# Save the combined text output if needed
combined_text_output = '\n\n'.join(extracted_texts)
with open('extracted_texts.txt', 'w') as file:
    file.write(combined_text_output)
