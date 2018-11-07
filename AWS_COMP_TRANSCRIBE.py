import boto3
import urllib, json
#import urllib2

#AWS Variable Declarations
s3bucket='ram20180720'
region='us-east-1'
s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe',region_name=region)
comprehend = boto3.client(service_name='comprehend',region_name=region)

#Reading the President Trump's speech in MP3
url='https://archive.org/download/20170120PresidentTrumpInaugurationSpeech/20170120%20President%20Trump%20Inauguration%20Speech.mp3'
response = urllib.request.urlopen(url)
data = response.read()

#Putting the MP3 file in S3 Bucket
s3.Bucket(s3bucket).put_object(Key='speech1.mp3', Body=data)


job_name="MyJob21"
#------ CODE TO CONVERT MP3 TO TEXT -------- #
# ------ UNCOMMENT FROM HERE TO START TRANSCRIBING -----#

#job_uri = "https://s3.amazonaws.com/ram20180720/speech1.mp3"

# transcribe.start_transcription_job(
#     TranscriptionJobName=job_name,
#     Media={
#         'MediaFileUri' : job_uri
#     },
#     MediaFormat = 'mp3',
#     LanguageCode = 'en-US'
# )

# ------ UNCOMMENT TILL HERE TO FINISH TRANSCRIBING -----#


while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print('Still...running')
#print(status)

#========================================
JsonUri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
response = urllib.request.urlopen(JsonUri)
data = json.loads(response.read())
result = data['results']['transcripts'][0]

text = result['transcript'][:1000]
print(text)

def detect_text(text):
    detectedText = comprehend.detect_dominant_language(Text=text)
    print('\n==============================')
    print('DETECTING LANGUAGE...')
    print('==============================')
    for language in detectedText['Languages']:
        print("Language : {}\t\t\t\tScore : {}".format(language['LanguageCode'], language['Score']))

    print('\n==============================')
    print('DETECTING ENTITIES...')
    print('==============================')
    detectedText = comprehend.detect_entities(Text=text, LanguageCode='en')
    for entity in detectedText['Entities']:
        print("Text : {}\t\t\t\t\t\t\t\t\t\t\ttype : {}\t\t\t\tScore : {}".format(entity['Text'],entity['Type'], entity['Score']))

    print('\n==============================')
    print('DETECTING KEY PHRASES...')
    print('==============================')
    detectedText = comprehend.detect_key_phrases(Text=text,LanguageCode='en')
    for phrase in detectedText['KeyPhrases']:
        print("Text : {}\t\t\t\t\t\tScore : {}".format(phrase['Text'],phrase['Score']))

    print('\n==============================')
    print('DETECTING SENTIMENT...')
    print('==============================')
    detectedText = comprehend.detect_sentiment(Text=text,LanguageCode='en')
    print(detectedText['Sentiment'])

print('-----------------------------------')
detect_text(text)
print('-----------------------------------')
