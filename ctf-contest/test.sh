#!/bin/bash
#!/bin/bash

curlResult=$(curl -Is http://10.92.21.104:5001 | head -n 1)
if [[ "$curlResult" == *"200 OK"* ]]; then
    echo "red-team : service-A : passed"
else
    echo "red-team : service-A : **FAILED**"
fi

curlResult=$(curl -Is http://10.92.21.104:5002 | head -n 1)
if [[ "$curlResult" == *"200 OK"* ]]; then
    echo "red-team : service-B : passed"
else
    echo "red-team : service-B : **FAILED**"
fi

curlResult=$(curl -Is http://10.92.21.104:5011 | head -n 1)
if [[ "$curlResult" == *"200 OK"* ]]; then
    echo "fuchsia-team : service-A : passed"
else
    echo "fuchsia-team : service-A : **FAILED**"
fi

curlResult=$(curl -Is http://10.92.21.104:5012 | head -n 1)
if [[ "$curlResult" == *"200 OK"* ]]; then
    echo "fuchsia-team : service-B : passed"
else
    echo "fuchsia-team : service-B : **FAILED**"
fi

