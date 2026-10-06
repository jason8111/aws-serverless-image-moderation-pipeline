import json
import boto3
import os

rekognition = boto3.client('rekognition')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ImageAnalysisResults')

def lambda_handler(event, context):
    # 1. Parse bucket name and object key from S3 Event
    record = event['Records'][0]['s3']
    bucket_name = record['bucket']['name']
    image_key = record['object']['key']
    
    image_spec = {'S3Object': {'Bucket': bucket_name, 'Name': image_key}}
    
    # 2. Rekognition Moderation Analysis
    mod_response = rekognition.detect_moderation_labels(Image=image_spec, MinConfidence=60.0)
    moderation_labels = [label['Name'] for label in mod_response.get('ModerationLabels', [])]
    is_flagged = len(moderation_labels) > 0
    
    # 3. Rekognition Facial Sentiment
    face_response = rekognition.detect_faces(Image=image_spec, Attributes=['ALL'])
    facial_emotions = []
    for face in face_response.get('FaceDetails', []):
        emotions = sorted(face.get('Emotions', []), key=lambda x: x['Confidence'], reverse=True)
        if emotions:
            facial_emotions.append(emotions[0]['Type'])
        
    # 4. Rekognition OCR Text Extraction
    text_response = rekognition.detect_text(Image=image_spec)
    extracted_lines = [item['DetectedText'] for item in text_response.get('TextDetections', []) if item['Type'] == 'LINE']
    extracted_text = " ".join(extracted_lines)
    
    # 5. Comprehend Sentiment Analysis on Extracted Text
    text_sentiment = "N/A"
    if extracted_text.strip():
        sentiment_resp = comprehend.detect_sentiment(Text=extracted_text, LanguageCode='en')
        text_sentiment = sentiment_resp.get('Sentiment', 'NEUTRAL')
        
    # 6. Save Results to DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            'ImageKey': image_key,
            'IsFlagged': is_flagged,
            'ModerationLabels': moderation_labels,
            'FacialEmotions': facial_emotions,
            'ExtractedText': extracted_text,
            'TextSentiment': text_sentiment
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Processing complete', 'is_flagged': is_flagged})
    } 