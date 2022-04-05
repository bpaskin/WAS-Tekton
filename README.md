### Tekton Pipeline for deploy WebSphere Application Server Apps ###

This is a sample pipeline that can be used for deploying an application to a tWAS container and deploying it to OCP.  The pipeline will do the following:

1. Download code from a [Git](https://github.com) repository
2. Compile the code using [Maven](https://maven.apache.org)
3. Use the [Dockerfile](https://docs.docker.com/engine/reference/builder/) to build a new tWAS image and store it in the OCP [ImageStreams](https://docs.openshift.com/container-platform/4.10/openshift_images/image-streams-manage.html) repository
4. Create a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and [Route](https://docs.openshift.com/container-platform/4.10/networking/routes/route-configuration.html).	

The first 3 items are done with Tasks from the [Tekton Hub](https://hub.tekton.dev).

The [OpenShift](https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/) and [Tekton](https://github.com/tektoncd/cli/releases) CLIs are needed to run commands and setup the pipeline.

1. Login to your OCP cluster
2. Install the Tekton Pipeline
```
oc apply -f tekton/tekton-pipelines-install.yaml
```
3. Install the necessary Tekton Tasks from the Tekton Hub
```
tkn hub install task git-clone -n <project>
tkn hub install task maven -n <project>
tkn hub install task kaniko -n <project>
```
4. Add the custom Task
```
oc apply -f tekton/was-pipeline-task.yaml 
```
5. Add the PersistentVolumeClaim used to share between tasks.
```
oc apply -f tekton/was-pipeline-pvc.yaml
```
6. Install the Pipeline
```
oc apply -f tekton/was-pipeline.yaml
```

To run the pipeline, a sample Pipeline Run is included
```
oc apply -f tekton/was-pipeline-run.yaml
```
---
#### Setting up a trigger ####

