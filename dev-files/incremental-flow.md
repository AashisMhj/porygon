## How the incremental flow works

1. Initialize a 3 Instance Pod first. This pod will start sending request to an url.
2. After 9 minutes increase the Pod count to 3 and will start sending request to same url as first pod.
3. Again after 5 instance increase the Pod count to 12 and will start sending request to same url.
4. Again after 5 instance increase the Pod count to 18 and will start sending request to same url.
5. Again after 5 minutes all instance are terminated a new pod is created which will start sending request to another url and the steps continue.
