
---
title: "unity-ios审核ipv6"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity","IOS","Ipv6"]
categories: ["Unity"]
---

<!--more-->


> 两种方案

**简单版本：需要用域名**
```
            IPAddress[] address = null;

		
                      
            try
            {
                //string HostName = Dns.GetHostName(); //得到主机名  
      //www.***.com自己的域名
                address = Dns.GetHostAddresses("www.***.com");
//本机ip不行，有bug
//                address= Dns.GetHostAddresses(ip);
            }
            catch (Exception ex)
            {
                Dg.LogError("Dns.GetHostAddresses::Error:", ex.ToString());
            }

            if(address!=null)
            {
                foreach (var item in address)
                {
                    Dg.Log("address:::::::::", item.ToString());
                }
            }

            if (address != null && address.Length>0&&address[0].AddressFamily == AddressFamily.InterNetworkV6)
            {
                Dg.Log("网络类型:::InterNetworkV6");
                client = new TcpClient(AddressFamily.InterNetworkV6);
            }  
            else  
            {
                Dg.Log("网络类型:::InterNetwork");
                client = new TcpClient(AddressFamily.InterNetwork);

            }
//connect时用adress
```

----

**复杂版本：可以用ipv4的ip地址**
c#部分
```

#if UNITY_IPHONE && !UNITY_EDITOR    
[DllImport("__Internal")]
	private static extern string getIPv6(string mHost, string mPort);  
#endif
    //"192.168.1.1&&ipv4"
    public static string GetIPv6(string mHost, string mPort)
    {
#if UNITY_IPHONE && !UNITY_EDITOR
		string mIPv6 = getIPv6(mHost, mPort);
		return mIPv6;
#else
        return mHost + "&&ipv4";
#endif
    }

    void getIPType(String serverIp, String serverPorts, out String newServerIp, out AddressFamily mIPType)
    {
        mIPType = AddressFamily.InterNetwork;
        newServerIp = serverIp;
        try
        {
            string mIPv6 = GetIPv6(serverIp, serverPorts);
            if (!string.IsNullOrEmpty(mIPv6))
            {
                string[] m_StrTemp = System.Text.RegularExpressions.Regex.Split(mIPv6, "&&");
                if (m_StrTemp != null && m_StrTemp.Length >= 2)
                {
                    string IPType = m_StrTemp[1];
                    if (IPType == "ipv6")
                    {
                        newServerIp = m_StrTemp[0];
                        mIPType = AddressFamily.InterNetworkV6;
                    }
                }
            }
        }
        catch (Exception e)
        {
            Dg.LogError("GetIPv6 error:" + e.ToString());
        }

    }

	public TcpClient CreateTcpClient(String serverIp, String serverPorts,out String newServerIP)
    {
        String newServerIp = "";
        AddressFamily newAddressFamily = AddressFamily.InterNetwork;
#if UNITY_IPHONE && !UNITY_EDITOR
        getIPType(serverIp, serverPorts, out newServerIp, out newAddressFamily);
        if (!string.IsNullOrEmpty(newServerIp)) { serverIp = newServerIp; }
#endif
        TcpClient client = new TcpClient(newAddressFamily);
        Dg.Log("网络类型 AddressFamily :" + newAddressFamily.ToString() + "  ServerIp:" + serverIp);
		newServerIP = serverIp;
        return client;
    }

private TcpClient client;
//ip ：ipv4地址，
        public void Connect(string ip, int port,int connectTimeout)
        {
			string newIp=ip;
			client = ProviderService.Instance.CreateTcpClient(ip, port.ToString(),out newIp);
                      client.BeginConnect(newIp, port, ConnectCallBack, client);
      }
          private void ConnectCallBack(IAsyncResult ar)
        {
            Dg.Log("ConnectCallBack");
            try
            {
                if (client == null) return;

                client.EndConnect(ar);
                Dg.Log("ConnectCallBack1111");
                //连接成功了

            }
            catch (SocketException e)
            {
                Dg.LogError("SOCKET::ERROR:", e.ToString());
            }            
        }
```

object-c
```oc
//#import "BundleId.h"
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <err.h>

#define MakeStringCopy( _x_ ) ( _x_ != NULL && [_x_ isKindOfClass:[NSString class]] ) ? strdup( [_x_ UTF8String] ) : NULL

const char* getIPv6(const char *mHost,const char *mPort)
{
	if( nil == mHost )
		return NULL;
	const char *newChar = "No";
	const char *cause = NULL;
	struct addrinfo* res0;
	struct addrinfo hints;
	struct addrinfo* res;
	int n, s;
	
	memset(&hints, 0, sizeof(hints));
	
	hints.ai_flags = AI_DEFAULT;
	hints.ai_family = PF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	//IOS9.2及以后的版本才支持IPv6
	if((n=getaddrinfo(mHost, "http", &hints, &res0))!=0)
	{
		printf("getaddrinfo error: %s\n",gai_strerror(n));
		return NULL;
	}
	
	struct sockaddr_in6* addr6;
	struct sockaddr_in* addr;
	NSString * NewStr = NULL;
	char ipbuf[32];
	s = -1;
	for(res = res0; res; res = res->ai_next)
	{
		if (res->ai_family == AF_INET6)
		{
			addr6 =( struct sockaddr_in6*)res->ai_addr;
			newChar = inet_ntop(AF_INET6, &addr6->sin6_addr, ipbuf, sizeof(ipbuf));
			NSString * TempA = [[NSString alloc] initWithCString:(const char*)newChar 
encoding:NSASCIIStringEncoding];
			NSString * TempB = [NSString stringWithUTF8String:"&&ipv6"];
			
			NewStr = [TempA stringByAppendingString: TempB];
			printf("%s\n", newChar);
		}
		else
		{
			addr =( struct sockaddr_in*)res->ai_addr;
			newChar = inet_ntop(AF_INET, &addr->sin_addr, ipbuf, sizeof(ipbuf));
			NSString * TempA = [[NSString alloc] initWithCString:(const char*)newChar 
encoding:NSASCIIStringEncoding];
			NSString * TempB = [NSString stringWithUTF8String:"&&ipv4"];
			
			NewStr = [TempA stringByAppendingString: TempB];			
			printf("%s\n", newChar);
		}
		break;
	}
	
	
	freeaddrinfo(res0);
	
	printf("getaddrinfo OK");
	
	NSString * mIPaddr = NewStr;
	return MakeStringCopy(mIPaddr);
}
```
