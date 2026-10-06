## Key Highlights & Features



- Automated Moderation: Explicit, suggestive or unsafe images can be automatically moderated using Amazon Rekognition `DetectModerationLabels`.

- Multi-Modal Sentiment Analysis: Amazon Rekognition can identify `HAPPY`, `SAD` etc. In facial expression, while Amazon Comprehend can extract text from images/memes to determine sentiment.

- Zero Infrastructure Overhead: Entirely serverless architecture which scales on demand using AWS Lambda, S3 and DynamoDB

- Cost-Optimized: Within AWS Free Tier Limits and no standby computing costs

---



## Tech Stack & AWS Services



- [AWS Lambda](https://aws.amazon.com/lambda/) (Python 3.12) for Compute

- [Amazon S3](https://aws.amazon.com/s3/) for storage

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) for database

- [Amazon Rekognition](https://aws.amazon.com/rekognition/) for computer vision, OCR, facial analysis

- [Amazon Comprehend](https://aws.amazon.com/comprehend/) for NLP

- IAM configured for Principle of Least Privilege

---



## Project Structure



```text

aws-serverless-image-moderation-pipeline/

├── src/

│ └── lambda_function.py # Primary Lambda handler function

└── README.md # Project architecture & documentation
