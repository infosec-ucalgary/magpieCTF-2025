# Slow, Slow, Quick Quick, Slow
### Category: Cloud
### Author: James Lowther (Articuler) & Jeremy Stuart (Mr.Wizard)

## Description
If you're like me you have two things you yearn for: the 90s and slower internet. Well have we got the challenge for you!

No gimmicks, no games, just a link to the flag. Click to download it. If you can't, you'll have to find another way.

Here is the site: http://\<IP\>:9090/

Submit the flag in this format: `magpie{<SHA256 hash of the flag file>}`

## Hints
N/A

## Solution
First, look at that website. Just...a seizure waiting to happen. It's so bad that it's awful. We're really proud of it.

1) While the page looks like it's going to serve you up some 90s style Bonzi Buddy malware, clicking on the big red button *will* actually start to download the flag file!  But very quickly you should see the problem: it's wildly slow.  And after 30 seconds the download fails (it's being killed by the server).  Attempts to restart the download just do this over and over.  Any attempts to continue where the last download left off will result in a 416 status code being returned, meaning the server cannot "restart" downloads from where they ended.

1) There is a comment in the index.html pointing to a script called init.sh.  Download this script.

2) The script has a looooong list of ip addresses followed by a bash script.  Some research is needed to figure out what the list of ip addresses represent and what the bash script does.
    - **IP List**: These are IPs associated with Bitrise Linux/Docker build instances.
      - https://devcenter.bitrise.io/en/infrastructure/build-machines/configuring-your-network-to-access-our-build-machines.html
    - **Bash Script**: This script is complicated.  Boiled down, it's using `iptables` and `tc` to control the download speed of the `flag` file.  Any requests for `flag` coming from a Bitrise build instance is allowed to download at 100mb/s.  For any other IP address, the download is only allowed 5kb/s and is killed after 30 seconds.

3) The answer is to write a Bitrise workflow to download the flag, hash the file, and output the resulting hash.

Below is an example workflow that can get the SHA256 hash of the flag:

```yml
---
format_version: '13'
default_step_lib_source: https://github.com/bitrise-io/bitrise-steplib.git
project_type: other
workflows:
  primary:
    steps:
      - script:
          title: Download flag and hash
          inputs:
          - content: |-
              #!/bin/bash
              wget -O flag http://<REPLACE_WITH_CHALLENGE_IP>:9091/flag
              sha256sum flag
meta:
  bitrise.io:
    stack: linux-docker-android-22.04
    machine_type_id: standard
trigger_map:
- workflow: primary
  push_branch: main
- workflow: primary
  pull_request_source_branch: "*"
```

## Flag
`magpie{b34a0614ee6c7dd81eeda2b3f32137fb4c62aa1e6fc6ce84869baef8161d08ae}`
