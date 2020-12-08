import boto3
import urllib

#print('Loading function')
rekognition = boto3.client('rekognition')

# --------------- Main handler ------------------
def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:
        response = rekognition.recognize_celebrities(Image={"S3Object": {"Bucket": bucket, "Name": key}})
        for celebrity in response['CelebrityFaces']:
            print('Name: {}'.format(celebrity['Name']))
            print('Id: {}'.format(celebrity['Id']))
            print('Position:')
            print('   Left: {:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
            print('   Top: {:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
            print('Info')
            for url in celebrity['Urls']:
                print('   {}'.format(url))
        # Print response to console.
        print(response)
        #return response
    except Exception as e:
        #print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e