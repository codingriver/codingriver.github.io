
---
title: "GitHub-ssh失败Permission-denied-(publickey)"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: [""]
categories: ["随笔"]
---

<!--more-->



在执行命令时报错`ssh -T git@github.com`
```
$ ssh -T git@github.com
The authenticity of host 'github.com (192.30.255.113)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,192.30.255.113' (RSA) to the list of known hosts.
git@github.com: Permission denied (publickey).

```

使用命令查看 `ssh -v git@github.com`
```
$ ssh -v git@github.com
OpenSSH_7.6p1, OpenSSL 1.0.2l  25 May 2017
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Connecting to github.com [192.30.255.112] port 22.
debug1: Connection established.
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_rsa type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_rsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_dsa type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_dsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_ecdsa type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_ecdsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_ed25519 type -1
debug1: key_load_public: No such file or directory
debug1: identity file /c/Users/Wang/.ssh/id_ed25519-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_7.6
debug1: Remote protocol version 2.0, remote software version libssh_0.7.0
debug1: no match: libssh_0.7.0
debug1: Authenticating to github.com:22 as 'git'
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256@libssh.org
debug1: kex: host key algorithm: ssh-rsa
debug1: kex: server->client cipher: aes128-ctr MAC: hmac-sha2-256 compression: none
debug1: kex: client->server cipher: aes128-ctr MAC: hmac-sha2-256 compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: Server host key: ssh-rsa SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8
debug1: Host 'github.com' is known and matches the RSA host key.
debug1: Found key in /c/Users/Wang/.ssh/known_hosts:1
Warning: Permanently added the RSA host key for IP address '192.30.255.112' to the list of known hosts.
debug1: rekey after 4294967296 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey after 4294967296 blocks
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey
debug1: Next authentication method: publickey
debug1: Trying private key: /c/Users/Wang/.ssh/id_rsa
debug1: Trying private key: /c/Users/Wang/.ssh/id_dsa
debug1: Trying private key: /c/Users/Wang/.ssh/id_ecdsa
debug1: Trying private key: /c/Users/Wang/.ssh/id_ed25519
debug1: No more authentication methods to try.
git@github.com: Permission denied (publickey).
```
最后发现使用.ssh目录下的几个private key ，把自己私钥的文件名改成第一个Trying private key的名字id_rsa
然后在重新执行就能连上了



