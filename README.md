### About
This lambda function is kicked off by our `unzipEnsentaBatchImages` lambda function. This function is given an array of file names(assumed to all be front images), downloads the zip file for our check images, and uploads all images(as .png) in the given list to our check images bucket(same bucket that houses our mobile images).

### Building an AWS Ready Zip File

We use the `Pillow` binary library as part of our image conversion process. We must spin up a docker container to ensure that our binaries are build to run on `linux`. We store a list of all of these dependencies in the `requirements.txt` file.

1) Build zip file:
```sh
$ docker build -t lambda-function .
```

2) Create a container from our docker image:
```sh
$ ID=$(docker create lambda-function /bin/true)
```

3) Copy the `.zip` file:
```sh
$ docker cp $ID:/ .
```

### AWS Function Settings

| Field | Setting |
| ------ | ------ |
| Trigger | Invoked async by `unzipEnsentaBatchImages` lambda function|
| Handler | `lambda_function.lambda_handler` |
| Memory(MB) | 3008 MB(max) -- A typical run of 250 images consumes 60 MB over 16300 ms |
| Timeout | 60 seconds |

### Permissions

| Service | Resource | Actions |
| ------ | ------ | ------ |
| Cloudwatch | arn:aws:logs:\*:\*:\* | Allow: logs:* |
| S3 | arn:aws:s3:::* | Allow: s3:GetObject |
| S3 | arn:aws:s3:::* | Allow: s3:PutObject |
