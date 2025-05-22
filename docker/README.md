# Building ScoutSuite Docker Image

## Quick Start

1. Navigate to docker directory:
   ```bash
   cd docker
   ```

2. Build AWS image:
   ```bash
   docker build -t scoutsuitedockerimage -t latest -f Dockerfile-aws . 
   ```

## Build Options

The build script supports multiple targets:
- `./build.sh aws` - Build AWS image only
- `./build.sh all` - Build all images
- `./build.sh base` - Build base image
- `./build.sh gcp` - Build GCP image
- `./build.sh azure` - Build Azure image

## Configuration

The AWS build uses these settings:
- Name: scoutsuite-aws
- Version: 1.0.0
- Image tag: latest

## Verify Build

Check your image:
```bash
docker images | grep scoutsuite-aws
```

## Next Steps

1. Run container:
   ```bash
   docker run -it --name scoutsuite scoutsuite-aws:latest
   ```

2. Copy AWS credentials:
   ```bash
   docker cp ~/.aws/credentials scoutsuite:/root/.aws/
   ```

3. Copy DockerScoutSuiteRunner latest and run the script
   ```bash
   docker cp tools\automation\scripts\DockerScoutSuiteRunner.py /root/ScoutSuite
   python DockerScoutSuiteRunner.py
   ```

## Build Arguments

The following build arguments can be customized:
- NAME: Image name
- DESCRIPTION: Image description
- VENDOR: Image vendor/owner
- VERSION: Image version
- IMAGE_NAME: Docker image name

## Tags

- latest: Most recent build
- x.y.z: Version specific builds

## Troubleshooting

If the build script closes immediately:

1. Open PowerShell or Command Prompt
2. Navigate to the docker directory:
   ```bash
   cd c:\Users\ashika.sreerambushan\source\repos\ScoutSuite\docker
   ```

3. Run build script with bash:
   ```bash
   bash build.sh aws
   ```

4. Alternative: Run docker build directly:
   ```bash
   docker build -t scoutsuite-aws:latest -f Dockerfile-aws .
   ```

5. Check for errors in the output
   ```bash
   docker images | grep scoutsuite-aws
   ```