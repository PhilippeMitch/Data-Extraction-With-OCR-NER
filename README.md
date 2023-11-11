# Data Extraction With OCR and NER

### Create data
We created about 30 boarding pass with some random information usinf google doc, and then download the doc into pdf format.
### Extract data
We converted the pdf file into multiple images, and then use Pytesseract to extract the text from each of the boarding images.

![best](https://github.com/PhilippeMitch/Data-Extraction-With-OCR-NER/blob/main/image/pdf_to_image.jpg)
### Text Cleaning and Organization
Once the text is extracted from the images, we perform basic cleaning procedures to prepare the
data for entity extraction and then save it into a csv file.
### Manual Labeling with BIO Tagging
We use BIO tagging to annotate each word or token in the text with a label indicating whether it is the
beginning of an entity, inside an entity, or outside any entity.

![best](https://github.com/PhilippeMitch/Data-Extraction-With-OCR-NER/blob/main/image/add_tag.jpg)
### Text Cleaning
After manually labeling the data using BIO tagging, To ensure high-quality training data, we perform text cleaning on the extracted text. This
involves removing any extra white spaces and eliminating special characters that are not relevant for training the model.
### Converting to Spacy Training Format
We convert the preprocessed data into the Spacy training format specifically
designed for Named Entity Recognition (NER).
### Train-Test Data Split
We split the processed data into training and testing sets.
### Training NER Model with Spacy
We train a Named Entity Recognition (NER) model using Spacy.

![best](https://github.com/PhilippeMitch/Data-Extraction-With-OCR-NER/blob/main/image/traning.jpg)
