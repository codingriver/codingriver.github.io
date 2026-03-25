---
title: "Shader案例"
date: "2022-03-24"
tags:
  - 随笔
  - 笔记
  - 编辑器扩展
  - Shader
  - 图形学
categories:
  - ANote
comments: true
---
# Shader案例

### 角色展示

![](image/Shader-Cases/2021-12-21-20-18-01.png)

>需要的贴图：  
>漫反射贴图；法线贴图；Metal，Roughness，SkinArea通道贴图CompMask（M,R,S）；次表面散射LUT查找图；IBL Specular CubeMap环境图；IBL Diffuse 球谐数据（提前读取IBL Diffuse CubeMap数据）;头发Aniso各向异性Noise贴图

![](image/Shader-Cases/avatorshow.gif)  
*漫反射，镜面反射，环境反射，环境高光*

#### 身体部分 

组成：
- 直接光漫反射
    Lambert
- 直接光的镜面反射
    Blinn-Phong
    *皮肤区域给一个很弱的高光（油光）*
- 间接光的漫反射 
    SH（球谐）
- 间接光的镜面反射
    CubeMap （Specular） 
- LUT SSS次表面散射（皮肤处理）
    LUT实现
- 色彩矫正
    ToneMaping ACES


```hlsl
Shader "Custom/Role_Standard"
{
    Properties
    {
		_MainTex ("Texture", 2D) = "white" {}
		_CompMask("CompMask(R M)",2D) = "white"{}
		_NormalMap("NormalMap",2D) = "bump"{}
		_SpecShininess("Spec Shininess",Float)=10
        _RoughnessAdjust("Roughness Adjust",Range(-1,1))=0
        _MetalAdjust("Metal Adjust",Range(-1,1))=0
        _SkinLUT("Skin LUT",2D)="white"{}
        _CurveOffset("Curve Offset",Range(0,1))=1
        _LutOffset("LutOffset",Range(0,1))=0
		[Header(IBL Specular)]
		_Tint("Tint",Color)=(1,1,1,1)
		_Expose("Expose",Float)=1.0		
		_EnvMap("Env Cube",Cube)="white"{}
		_Rotate("Rotate",Range(0,360))=0
		
		[Toggle(_DIFFUSE_ON)]_DiffuseCheck("Diffuse Check",Float)=0
		[Toggle(_SPECULAR_ON)]_Specular_Check("Specular Check",Float)=0
		[Toggle(_SH_ON)]_SHCheck("SH Check",Float)=0
		[Toggle(_IBL_ON)]_IBLCheck("IBL Check",Float)=0
		[Toggle(_OILSKIN_ON)]_OilSkinCheck("Oil Skin Check",Float)=0
		
		[Space(20)]
		[Header(SH)]
		[HideInInspector]custom_SHAr("Custom SHAr", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHAg("Custom SHAg", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHAb("Custom SHAb", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHBr("Custom SHBr", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHBg("Custom SHBg", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHBb("Custom SHBb", Vector) = (0, 0, 0, 0)
		[HideInInspector]custom_SHC("Custom SHC", Vector) = (0, 0, 0, 1)			
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            Tags{"LightMode" = "ForwardBase"}
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase
            #pragma shader_feature _DIFFUSE_ON
            #pragma shader_feature _SPECULAR_ON
            #pragma shader_feature _SH_ON
            #pragma shader_feature _IBL_ON
            #pragma shader_feature _OILSKIN_ON
            
            #include "UnityCG.cginc"
            #include"AutoLight.cginc"

            struct appdata  // appdata_full
            {
                float4 vertex : POSITION; //模型空间顶点坐标
                half2 texcoord : TEXCOORD0; //第一套UV（模型最多只能有4套UV）
				half3 normal : NORMAL; //顶点法线
				half4 tangent : TANGENT; //顶点切线(模型导入Unity后自动计算得到)
            };

            struct v2f
            {
                float4 pos : SV_POSITION; //输出裁剪空间下的顶点坐标数据，给光栅化使用，必须要写的数据
                float2 uv : TEXCOORD0; //自定义数据体
                half3 normal_dir : TEXCOORD1;
                half3 tangent_dir : TEXCOORD2;
                half3 binormal_dir : TEXCOORD3;
                half3 pos_world : TEXCOORD4;
                //最多可以写16个：TEXCOORD0 ~ TEXCOORD15。
                LIGHTING_COORDS(5,6)   ///SHADOW 第一步
            };

			sampler2D _MainTex;
			sampler2D _CompMask;
			float4 _MainTex_ST;
			float4 _LightColor0;
			float _Shininess;
			float4 _AmbientColor;
			float _SpecIntensity;
			sampler2D _AOMap;
			sampler2D _SpecMask;
			sampler2D _NormalMap;
			float _NormalIntensity;
			sampler2D _ParallaxMap;
			float _Parallax;
            float _SpecShininess;
            float _RoughnessAdjust;
            float _MetalAdjust;
			float4 _Tint;
			float _Expose;            
            float _Rotate;
            samplerCUBE _EnvMap;
            float4 _EnvMap_HDR;
            sampler2D _SkinLUT;
            float _CurveOffset;
            float _LutOffset;
			half4 custom_SHAr;
			half4 custom_SHAg;
			half4 custom_SHAb;
			half4 custom_SHBr;
			half4 custom_SHBg;
			half4 custom_SHBb;
			half4 custom_SHC;	
			
            
            float3 ShadeSH(float3 normal_dir)
            {
				float4 normalForSH = float4(normal_dir, 1.0);
				//SHEvalLinearL0L1
				half3 x;
				x.r = dot(custom_SHAr, normalForSH);
				x.g = dot(custom_SHAg, normalForSH);
				x.b = dot(custom_SHAb, normalForSH);

				//SHEvalLinearL2
				half3 x1, x2;
				// 4 of the quadratic (L2) polynomials
				half4 vB = normalForSH.xyzz * normalForSH.yzzx;
				x1.r = dot(custom_SHBr, vB);
				x1.g = dot(custom_SHBg, vB);
				x1.b = dot(custom_SHBb, vB);

				// Final (5th) quadratic (L2) polynomial
				half vC = normalForSH.x*normalForSH.x - normalForSH.y*normalForSH.y;
				x2 = custom_SHC.rgb * vC;

				float3 sh = max(float3(0.0, 0.0, 0.0), (x + x1 + x2));
				sh = pow(sh, 1.0 / 2.2);  
				return sh;
            }
            
			float3 ACESFilm(float3 x)
			{
				float a = 2.51f;
				float b = 0.03f;
				float c = 2.43f;
				float d = 0.59f;
				float e = 0.14f;
				return saturate((x*(a*x + b)) / (x*(c*x + d) + e));
			};
			
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv=TRANSFORM_TEX(v.texcoord,_MainTex);
                o.pos_world=mul(unity_ObjectToWorld,v.vertex).xyz;
                o.normal_dir=normalize(mul(v.normal,(float3x3)unity_WorldToObject));
                o.tangent_dir=normalize(mul((float3x3)unity_ObjectToWorld,v.tangent.xyz));
                o.binormal_dir=normalize(cross(o.normal_dir, o.tangent_dir))*v.tangent.w;
                TRANSFER_VERTEX_TO_FRAGMENT(o); ///SHADOW 第二步
                return o;
            }

            half4 frag (v2f i) : SV_Target
            {
                // Base Color
                half4 base_color=tex2D(_MainTex,i.uv);
                base_color=pow(base_color,2.2);// gamma转Liner空间
                half3 comp_mask=tex2D(_CompMask,i.uv);         
                half skin_area=1.0-comp_mask.b;
                half roughness=saturate(comp_mask.r+_RoughnessAdjust);
                half metal=saturate(comp_mask.g+ _MetalAdjust);
                half3 spec_color=lerp(0.04,base_color.rgb,metal);
                base_color=base_color*(1-metal);
                
                half3 pos_world=i.pos_world;
                half3 normal_dir=normalize(i.normal_dir);
                half3 tangent_dir=normalize(i.tangent_dir);
                half3 binormal_dir=normalize(i.binormal_dir);
                half3 view_dir=normalize(_WorldSpaceCameraPos.xyz-pos_world);
                float3x3 TBN=float3x3(tangent_dir,binormal_dir,normal_dir);
        
                
                // Noraml 法线
                half4 normalmap=tex2D(_NormalMap,i.uv);
                half3 normal_data=UnpackNormal(normalmap);
                // normal_data.xy = normal_data.xy * _NormalIntensity;
                normal_dir=normalize(mul(normal_data,TBN));
                //normal_dir = normalize(tangent_dir * normal_data.x * _NormalIntensity + binormal_dir * normal_data.y * _NormalIntensity + normal_dir * normal_data.z);

                // Light Info
                half3 light_dir=normalize(_WorldSpaceLightPos0.xyz);
                half4 light_color=_LightColor0.rgba;
                half atten=LIGHT_ATTENUATION(i);
                

                
                
                
                // Direct Diffuse 漫反射,Lambert
                half NdotL=max(0.0,dot(normal_dir,light_dir));
                half3 diffuse= base_color.rgb*NdotL*light_color.rgb*atten;
                half2 uv_lut=half2(NdotL*atten+_LutOffset,_CurveOffset);
                half3 lut_color_gamma=tex2D(_SkinLUT,uv_lut);
                half3 lut_color=pow(lut_color_gamma,2.2);
                half3 sss_diffuse=lut_color*base_color*_LightColor0.rgb;
                #ifdef _DIFFUSE_ON
                half3 direct_diffuse=lerp(diffuse,sss_diffuse,skin_area);
                #else
                half3 direct_diffuse=half3(0,0,0);
                #endif
                
                // Direct Specular 镜面反射（高光） Blinn-Phong
                half smoothness=1.0-roughness;
                half3 half_dir=normalize(view_dir+light_dir);
                half NdotH=max(0.0,dot(normal_dir,half_dir));
                half shininess=lerp(1,_SpecShininess,smoothness);
                half spec=pow(NdotH,shininess);
                #ifdef _OILSKIN_ON
                half3 spec_skin_color=lerp(spec_color,0.1,skin_area); //皮肤油光
                #else
                half3 spec_skin_color=spec_color;
                #endif
                
                #ifdef _SPECULAR_ON
                half3 direct_specular=spec*spec_skin_color*light_color.rgb*atten;
                #else
                half3 direct_specular=half3(0,0,0);
                #endif
                
                //Indirect Diffuse 间接光的漫反射
                float half_lambert=dot(normal_dir,light_dir)*0.5+0.5;
                #ifdef _SH_ON
                half3 env_diffuse= ShadeSH(normal_dir)*base_color*half_lambert;
                #else
                half3 env_diffuse=half3(0,0,0);
                #endif                
                
                // Indirect Specular 间接光的镜面反射
				half3 rViewDir=reflect(-view_dir,normal_dir);
				float rad=_Rotate*UNITY_PI/180;
				float2x2 Rotation=float2x2(cos(rad),sin(rad),-sin(rad),cos(rad));
				rViewDir.xz=mul(Rotation,rViewDir.xz);
				
			    roughness=roughness*(1.7-0.7*roughness);
				float mip_level=(roughness)*6.0;
				half4 color_cube=texCUBElod(_EnvMap,float4(rViewDir,mip_level));
				half3 env_specular=DecodeHDR(color_cube,_EnvMap_HDR)*_Expose*spec_color*half_lambert*(1-skin_area);
                #ifdef _IBL_ON
                #else
                env_specular=half3(0,0,0);
                #endif                
                
                
				half3 final_color = (direct_diffuse + direct_specular + env_diffuse+env_specular);
				half3 tone_color = ACESFilm(final_color);
				tone_color = pow(tone_color, 1.0 / 2.2);                
                return half4(tone_color,1.0);
                // return half4(final_color,1.0);
            }
            ENDCG
        }
        
    }
    Fallback "Diffuse" ///SHADOW 第四步
}


```

#### 头发部分
> 头发处理：Kajiya-Kay各向异性头发（[Kajiya-Kay头发](https://zhuanlan.zhihu.com/p/363591383)）

组成：
- 直接光的漫反射
    Lambert
- 直接光的镜面反射，双层高光
    Kajiya-Kay各向异性头发（[Kajiya-Kay头发](https://zhuanlan.zhihu.com/p/363591383)）
- 间接光的镜面反射
    CubeMap （Specular）


```hlsl
Shader "Custom/Role_Hair"
{
    Properties
    {
		_MainTex ("Texture", 2D) = "white" {}
		_BaseColor("Base Color",Color)=(1,1,1,1)
		_NormalMap("NormalMap",2D) = "bump"{}
		_RoughnessAdjust("Roughness Adjust",Range(0,1))=0
		
		[Header(Specular)]
		_AnisoMap("Aniso Map",2D)="gray"{}
		_SpecColor1("Spec Color 1",Color)=(1,1,1,1)
		_SpecShininess1("Spec Shininess 1",Range(0,1))=0.1
		_SpecNoise1("Spec Noise 1",float)=1
		_SpecOffset1("Spec Offset 1",float)=0
		_SpecColor2("Spec Color 2",Color)=(1,1,1,1)
		_SpecShininess2("Spec Shininess 2",Range(0,1))=0.1
		_SpecNoise2("Spec Noise 2",float)=1
		_SpecOffset2("Spec Offset 2",float)=0		
		
		[Header(IBL Specular)]
		_Tint("Tint",Color)=(1,1,1,1)
		_Expose("Expose",Float)=1.0		
		_EnvMap("Env Cube",Cube)="white"{}
		_Rotate("Rotate",Range(0,360))=0
		
		[Toggle(_DIFFUSE_ON)]_DiffuseCheck("Diffuse Check",Float)=0
		[Toggle(_SPECULAR_ON)]_Specular_Check("Specular Check",Float)=0
		// [Toggle(_SH_ON)]_SHCheck("SH Check",Float)=0
		[Toggle(_IBL_ON)]_IBLCheck("IBL Check",Float)=0		
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            Tags{"LightMode" = "ForwardBase"}
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase
            #pragma shader_feature _DIFFUSE_ON
            #pragma shader_feature _SPECULAR_ON
            #pragma shader_feature _SH_ON
            #pragma shader_feature _IBL_ON
            #pragma shader_feature _OILSKIN_ON
            
            #include "UnityCG.cginc"
            #include"AutoLight.cginc"

            struct appdata  // appdata_full
            {
                float4 vertex : POSITION; //模型空间顶点坐标
                half2 texcoord : TEXCOORD0; //第一套UV（模型最多只能有4套UV）
				half3 normal : NORMAL; //顶点法线
				half4 tangent : TANGENT; //顶点切线(模型导入Unity后自动计算得到)
            };

            struct v2f
            {
                float4 pos : SV_POSITION; //输出裁剪空间下的顶点坐标数据，给光栅化使用，必须要写的数据
                float2 uv : TEXCOORD0; //自定义数据体
                half3 normal_dir : TEXCOORD1;
                half3 tangent_dir : TEXCOORD2;
                half3 binormal_dir : TEXCOORD3;
                half3 pos_world : TEXCOORD4;
                //最多可以写16个：TEXCOORD0 ~ TEXCOORD15。
                LIGHTING_COORDS(5,6)   ///SHADOW 第一步
            };

			sampler2D _MainTex;
			sampler2D _CompMask;
			float4 _MainTex_ST;
			float4 _LightColor0;
			float _Shininess;
			float4 _AmbientColor;
			float _SpecIntensity;
			sampler2D _AOMap;
			sampler2D _SpecMask;
			sampler2D _NormalMap;
			float _NormalIntensity;
			sampler2D _ParallaxMap;
			float _Parallax;
            float _SpecShininess;
            float _RoughnessAdjust;
            float _MetalAdjust;
			float4 _Tint;
			float _Expose;            
            float _Rotate;
            samplerCUBE _EnvMap;
            float4 _EnvMap_HDR;
            sampler2D _SkinLUT;
            float _CurveOffset;
            float _LutOffset;
			half4 custom_SHAr;
			half4 custom_SHAg;
			half4 custom_SHAb;
			half4 custom_SHBr;
			half4 custom_SHBg;
			half4 custom_SHBb;
			half4 custom_SHC;	
			float _BaseColor;
			sampler2D _AnisoMap;
			float4 _AnisoMap_ST;
			
			
		float4 _SpecColor1;
		float _SpecShininess1;
		float _SpecNoise1;
		float _SpecOffset1;
		float4 _SpecColor2;
		float _SpecShininess2;
		float _SpecNoise2;
		float _SpecOffset2;
            
			float3 ACESFilm(float3 x)
			{
				float a = 2.51f;
				float b = 0.03f;
				float c = 2.43f;
				float d = 0.59f;
				float e = 0.14f;
				return saturate((x*(a*x + b)) / (x*(c*x + d) + e));
			};
			
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv=TRANSFORM_TEX(v.texcoord,_MainTex);
                o.pos_world=mul(unity_ObjectToWorld,v.vertex).xyz;
                o.normal_dir=normalize(mul(v.normal,(float3x3)unity_WorldToObject));
                o.tangent_dir=normalize(mul((float3x3)unity_ObjectToWorld,v.tangent.xyz));
                o.binormal_dir=normalize(cross(o.normal_dir, o.tangent_dir))*v.tangent.w;
                TRANSFER_VERTEX_TO_FRAGMENT(o); ///SHADOW 第二步
                return o;
            }

            half4 frag (v2f i) : SV_Target
            {
                // Base Color
                half4 base_color=tex2D(_MainTex,i.uv);
                base_color=pow(base_color,2.2);// gamma转Liner空间
                half4 spec_color=base_color;
                
                half roughness=saturate(_RoughnessAdjust);
                
                half3 pos_world=i.pos_world;
                half3 normal_dir=normalize(i.normal_dir);
                half3 tangent_dir=normalize(i.tangent_dir);
                half3 binormal_dir=normalize(i.binormal_dir);
                half3 view_dir=normalize(_WorldSpaceCameraPos.xyz-pos_world);
                float3x3 TBN=float3x3(tangent_dir,binormal_dir,normal_dir);
        
                
                // Noraml 法线
                half4 normalmap=tex2D(_NormalMap,i.uv);
                half3 normal_data=UnpackNormal(normalmap);
                // normal_data.xy = normal_data.xy * _NormalIntensity;
                normal_dir=normalize(mul(normal_data,TBN));
                //normal_dir = normalize(tangent_dir * normal_data.x * _NormalIntensity + binormal_dir * normal_data.y * _NormalIntensity + normal_dir * normal_data.z);

                // Light Info
                half3 light_dir=normalize(_WorldSpaceLightPos0.xyz);
                half4 light_color=_LightColor0.rgba;
                half atten=LIGHT_ATTENUATION(i);
                

                
                
                
                // Direct Diffuse 漫反射,Lambert
                
                half NdotL=max(0.0,dot(normal_dir,light_dir));
                half half_lambert=NdotL*0.5+0.5;
                half3 direct_diffuse=base_color;
                
                // Direct Specular 镜面反射（高光） Blinn-Phong
                float aniso_noise=tex2D(_AnisoMap,i.uv*_AnisoMap_ST.xy+_AnisoMap_ST.zw).r-0.5;
                
                half3 half_dir=normalize(view_dir+light_dir);
                half NdotH=dot(normal_dir,half_dir);
                half TdotH=dot(tangent_dir,half_dir);
                
                half NdotV=max(0.0,dot(normal_dir,view_dir));
                float aniso_atten=saturate(sqrt(max(0.0,half_lambert/NdotV)))*atten;
                
                // spec1
                float3 spec_color1=_SpecColor1.rgb+base_color;
                half3 b_offset1=normal_dir*(_SpecOffset1+_SpecNoise1*aniso_noise);
                half3 binormal_dir1=normalize(binormal_dir+b_offset1);
                half BdotH1=dot(binormal_dir1,half_dir)/_SpecShininess1;
                float3 spec_term1=exp(-(TdotH*TdotH+BdotH1*BdotH1)/(1.0+NdotH));
                float3 final_spec1=spec_term1*aniso_atten*spec_color1*light_color.rgb;
                
                //spec2 
                float3 spec_color2=_SpecColor2.rgb+base_color;
                half3 b_offset2=normal_dir*(_SpecOffset2+_SpecNoise2*aniso_noise);
                half3 binormal_dir2=normalize(binormal_dir+b_offset2);
                half BdotH2=dot(binormal_dir2,half_dir)/_SpecShininess2;
                float3 spec_term2=exp(-(TdotH*TdotH+BdotH2*BdotH2)/(1.0+NdotH));
                float3 final_spec2=spec_term2*aniso_atten*spec_color2*light_color.rgb;                

                // Indirect Specular 间接光的镜面反射
				half3 rViewDir=reflect(-view_dir,normal_dir);
				float rad=_Rotate*UNITY_PI/180;
				float2x2 Rotation=float2x2(cos(rad),sin(rad),-sin(rad),cos(rad));
				rViewDir.xz=mul(Rotation,rViewDir.xz);
				
			    roughness=roughness*(1.7-0.7*roughness);
				float mip_level=(roughness)*6.0;
				half4 color_cube=texCUBElod(_EnvMap,float4(rViewDir,mip_level));
				float3 color_ibl=DecodeHDR(color_cube,_EnvMap_HDR);
				half3 env_specular=color_ibl*_Expose*half_lambert*aniso_noise;
                #ifdef _IBL_ON
                #else
                env_specular=half3(0,0,0);
                #endif                
                #ifdef _DIFFUSE_ON
                #else
                direct_diffuse=half3(0,0,0);
                #endif   
                #ifdef _SPECULAR_ON
                #else
                final_spec1=half3(0,0,0);
                final_spec2=half3(0,0,0);
                #endif                                   
                
				half3 final_color = (final_spec1 + final_spec2+direct_diffuse+env_specular);
				// half3 final_color = (direct_diffuse + direct_specular+env_specular);
				half3 tone_color = ACESFilm(final_color);
				tone_color = pow(tone_color, 1.0 / 2.2);                
                return half4(tone_color,1.0);
                // return half4(final_color,1.0);
            }
            ENDCG
        }
        
    }
    Fallback "Diffuse" ///SHADOW 第四步
}

```

### 玉龙


![](image/Shader-Cases/CleanShot2022-03-17.gif)
*漫反射，透射光（高光），环境光*

透射光实现：根据光反方向（增加法线的扭曲，表示玉龙表面的粗糙情况影响光线的方向）和视线方向夹角来判定透射光的强度（假设从玉龙后面有个手电筒和人眼的夹角，越小表示人眼看到的光线越多，光越强），然后通过厚度图来模拟玉龙的通透性


```hlsl
Shader "CS03/Dragon"
{
    Properties
    {
		_DiffuseColor ("Diffuse Color", Color) = (1,1,1,1)
		_Opacity("Opacity",Float)=1
		_AddColor ("Add Color", Color) = (1,1,1,1)
		_Distort("Distort",Range(0,1))=0
		_Power("Power",Float)=2
		_Scale("Scale",Float)=1
		_ThicknessMap ("Thickness Map", 2D) = "black" {}
		_CubeMap ("Cube Map", CUBE) = "white" {}
		_EnvRotate("Env Rotate",Range(0,360))=0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            Tags{"LightMode" = "ForwardBase"}
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase
            #include "UnityCG.cginc"
            #include"AutoLight.cginc"

            struct appdata  // appdata_full
            {
                float4 vertex : POSITION; //模型空间顶点坐标
                half2 texcoord : TEXCOORD0; //第一套UV（模型最多只能有4套UV）
				half2 texcoord1 : TEXCOORD1; //第二套UV
				half2 texcoord2 : TEXCOORD2; //第三套UV
				half2 texcoord3 : TEXCOORD3;  //第四套UV，模型最多只能有4套UV
				half4 color : COLOR; //顶点颜色
				half3 normal : NORMAL; //顶点法线
				half4 tangent : TANGENT; //顶点切线(模型导入Unity后自动计算得到)
            };

            struct v2f
            {
                float4 pos : SV_POSITION; //输出裁剪空间下的顶点坐标数据，给光栅化使用，必须要写的数据
                float2 uv : TEXCOORD0; //自定义数据体
                half3 normal_dir : TEXCOORD1;
                half3 tangent_dir : TEXCOORD2;
                half3 binormal_dir : TEXCOORD3;
                half3 pos_world : TEXCOORD4;
                //最多可以写16个：TEXCOORD0 ~ TEXCOORD15。
            };

			sampler2D _MainTex;
			float4 _MainTex_ST;
			float4 _LightColor0;
			sampler2D _NormalMap;
			float _Distort;
			float _Power;
			float _Scale;
			sampler2D _ThicknessMap;
            samplerCUBE _CubeMap;
            float4 _CubeMap_HDR;
            float _EnvRotate;
            float4 _DiffuseColor;
            float4 _AddColor;
            float _Opacity;
			
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv=TRANSFORM_TEX(v.texcoord,_MainTex);
                o.pos_world=mul(unity_ObjectToWorld,v.vertex).xyz;
                o.normal_dir=normalize(mul(v.normal,(float3x3)unity_WorldToObject));
                o.tangent_dir=normalize(mul((float3x3)unity_ObjectToWorld,v.tangent.xyz));
                o.binormal_dir=normalize(cross(o.normal_dir, o.tangent_dir))*v.tangent.w;
                return o;
            }

            half4 frag (v2f i) : SV_Target
            {
                half3 pos_world=i.pos_world;
                half3 normal_dir=normalize(i.normal_dir);
                half3 tangent_dir=normalize(i.tangent_dir);
                half3 binormal_dir=normalize(i.binormal_dir);
                half3 view_dir=normalize(_WorldSpaceCameraPos.xyz-pos_world);
                float3x3 TBN=float3x3(tangent_dir,binormal_dir,normal_dir);
                // Light
                half3 light_dir=normalize(_WorldSpaceLightPos0.xyz);
                half4 light_color=_LightColor0.rgba;
                half atten=1.0;
                
                //漫反射
                float NdotL=max(0.0,dot(normal_dir,light_dir));
                float3 color_diffuse=NdotL*_DiffuseColor.rgb*light_color.rgb;
                float sky_light=(dot(normal_dir,float3(0,1,0))+1.0)*0.5;
                float3 color_sky=sky_light*_DiffuseColor.rgb;
                float3 final_diffuse=color_diffuse+_AddColor.rgb+color_sky*_Opacity;
                
                // 透射光
                float3 back_dir=-normalize(light_dir+normal_dir*_Distort);
                float VdotB=max(0.0,dot(view_dir,back_dir));
                float backlight_term=max(0.0,pow(VdotB,_Power))*_Scale;
                float thickness=1.0-tex2D(_ThicknessMap,i.uv).r;
                half3 back_color=backlight_term*light_color*thickness;           

                // 光泽反射
                float3 rView_dir=reflect(-view_dir,normal_dir);
                float drag=_EnvRotate*UNITY_PI/180.0;
                float2x2 Roration=float2x2(cos(drag),sin(drag),-sin(drag),cos(drag));
                rView_dir.xz=mul(Roration,rView_dir.xz);
                half4 color_cube=texCUBE(_CubeMap,rView_dir);
                float3 color_env=DecodeHDR(color_cube,_CubeMap_HDR);
                half fresnel=1.0-max(0.0,dot(normal_dir,view_dir));
                float3 final_env=color_env*fresnel;
                
                float3 color_final=final_diffuse+final_env+ back_color;
                
                // return half4(thickness.xxx,1.0);
                return half4(color_final,1.0);
            }
            ENDCG
        }     
        Pass
        {
            Tags{"LightMode" = "ForwardAdd"}
            Blend One One
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdadd
            #include "UnityCG.cginc"
            #include"AutoLight.cginc"

            struct appdata  // appdata_full
            {
                float4 vertex : POSITION; //模型空间顶点坐标
                half2 texcoord : TEXCOORD0; //第一套UV（模型最多只能有4套UV）
				half2 texcoord1 : TEXCOORD1; //第二套UV
				half2 texcoord2 : TEXCOORD2; //第三套UV
				half2 texcoord3 : TEXCOORD3;  //第四套UV，模型最多只能有4套UV
				half4 color : COLOR; //顶点颜色
				half3 normal : NORMAL; //顶点法线
				half4 tangent : TANGENT; //顶点切线(模型导入Unity后自动计算得到)
            };

            struct v2f
            {
                float4 pos : SV_POSITION; //输出裁剪空间下的顶点坐标数据，给光栅化使用，必须要写的数据
                float2 uv : TEXCOORD0; //自定义数据体
                half3 normal_dir : TEXCOORD1;
                half3 tangent_dir : TEXCOORD2;
                half3 binormal_dir : TEXCOORD3;
                half3 pos_world : TEXCOORD4;
                //最多可以写16个：TEXCOORD0 ~ TEXCOORD15。
                LIGHTING_COORDS(5,6)
            };

			sampler2D _MainTex;
			float4 _MainTex_ST;
			float4 _LightColor0;
			sampler2D _NormalMap;
			float _Distort;
			float _Power;
			float _Scale;
			sampler2D _ThicknessMap;
            samplerCUBE _CubeMap;
            float4 _CubeMap_HDR;
            float _EnvRotate;
            float4 _DiffuseColor;
            float4 _AddColor;
            float _Opacity;
			
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv=TRANSFORM_TEX(v.texcoord,_MainTex);
                o.pos_world=mul(unity_ObjectToWorld,v.vertex).xyz;
                o.normal_dir=normalize(mul(v.normal,(float3x3)unity_WorldToObject));
                o.tangent_dir=normalize(mul((float3x3)unity_ObjectToWorld,v.tangent.xyz));
                o.binormal_dir=normalize(cross(o.normal_dir, o.tangent_dir))*v.tangent.w;
                TRANSFER_VERTEX_TO_FRAGMENT(o);
                return o;
            }

            half4 frag (v2f i) : SV_Target
            {
                half shadow = SHADOW_ATTENUATION(i); ///SHADOW 第三步
            
                half3 pos_world=i.pos_world;
                half3 normal_dir=normalize(i.normal_dir);
                half3 tangent_dir=normalize(i.tangent_dir);
                half3 binormal_dir=normalize(i.binormal_dir);
                half3 view_dir=normalize(_WorldSpaceCameraPos.xyz-pos_world);
                float3x3 TBN=float3x3(tangent_dir,binormal_dir,normal_dir);
                // Light
                half3 light_dir=normalize(_WorldSpaceLightPos0.xyz);
                half4 light_color=_LightColor0.rgba;
                half atten=LIGHT_ATTENUATION(i);
                
                // 透射光
                float3 back_dir=-normalize(light_dir+normal_dir*_Distort);
                float VdotB=max(0.0,dot(view_dir,back_dir));
                float backlight_term=max(0.0,pow(VdotB,_Power))*_Scale;
                float thickness=1.0-tex2D(_ThicknessMap,i.uv).r;
                half3 back_color=backlight_term*light_color*thickness;           
                
                float3 color_final=back_color;
                return half4(color_final,1.0);
            }
            ENDCG
        }             
    }
    Fallback "Diffuse" ///SHADOW 第四步
}


```


### 钻石

![](image/Shader-Cases/CleanShot2022-03-17.gif)

*双Pass渲染，一个背面渲染（cubemap的反射和折射），一个前面渲染（折射和菲涅尔）*

*ASE*
```hlsl
// Made with Amplify Shader Editor
// Available at the Unity Asset Store - http://u3d.as/y3X 
Shader "CS07/Diamond"
{
	Properties
	{
		_ColorA("Color A", Color) = (0.02491992,0.09269338,0.754717,0)
		_RefractTex("RefractTex", CUBE) = "white" {}
		_ReflectTex("ReflectTex", CUBE) = "white" {}
		_ReflectIntensity("ReflectIntensity", Float) = 1
		_RefractIntensity("RefractIntensity", Float) = 1
		_RimPower("RimPower", Float) = 5
		_RimBias("RimBias", Float) = 0
		_RimScale("RimScale", Float) = 0
		_RimColor("RimColor", Color) = (0,0,0,0)

	}
	
	SubShader
	{
		
		
		Tags { "RenderType"="Opaque" "Queue"="Geometry" }
	LOD 100

		
		
		
		Pass
		{
			Name "Unlit"
			Tags { "LightMode"="ForwardBase" }

		CGINCLUDE
		#pragma target 3.0
		ENDCG
		Blend Off
		AlphaToMask Off
		Cull Front
		ColorMask RGBA
		ZWrite On
		ZTest LEqual
		Offset 0 , 0
		

			CGPROGRAM

			

			#ifndef UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX
			//only defining to not throw compilation error over Unity 5.5
			#define UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input)
			#endif
			#pragma vertex vert
			#pragma fragment frag
			#pragma multi_compile_instancing
			#include "UnityCG.cginc"
			#define ASE_NEEDS_FRAG_WORLD_POSITION


			struct appdata
			{
				float4 vertex : POSITION;
				float4 color : COLOR;
				float3 ase_normal : NORMAL;
				UNITY_VERTEX_INPUT_INSTANCE_ID
			};
			
			struct v2f
			{
				float4 vertex : SV_POSITION;
				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				float3 worldPos : TEXCOORD0;
				#endif
				float4 ase_texcoord1 : TEXCOORD1;
				UNITY_VERTEX_INPUT_INSTANCE_ID
				UNITY_VERTEX_OUTPUT_STEREO
			};

			uniform float4 _ColorA;
			uniform samplerCUBE _RefractTex;
			uniform samplerCUBE _ReflectTex;
			uniform float _RefractIntensity;

			
			v2f vert ( appdata v )
			{
				v2f o;
				UNITY_SETUP_INSTANCE_ID(v);
				UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(o);
				UNITY_TRANSFER_INSTANCE_ID(v, o);

				float3 ase_worldNormal = UnityObjectToWorldNormal(v.ase_normal);
				o.ase_texcoord1.xyz = ase_worldNormal;
				
				
				//setting value to unused interpolator channels and avoid initialization warnings
				o.ase_texcoord1.w = 0;
				float3 vertexValue = float3(0, 0, 0);
				#if ASE_ABSOLUTE_VERTEX_POS
				vertexValue = v.vertex.xyz;
				#endif
				vertexValue = vertexValue;
				#if ASE_ABSOLUTE_VERTEX_POS
				v.vertex.xyz = vertexValue;
				#else
				v.vertex.xyz += vertexValue;
				#endif
				o.vertex = UnityObjectToClipPos(v.vertex);

				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
				#endif
				return o;
			}
			
			fixed4 frag (v2f i ) : SV_Target
			{
				UNITY_SETUP_INSTANCE_ID(i);
				UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(i);
				fixed4 finalColor;
				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				float3 WorldPosition = i.worldPos;
				#endif
				float3 ase_worldNormal = i.ase_texcoord1.xyz;
				float3 ase_worldViewDir = UnityWorldSpaceViewDir(WorldPosition);
				ase_worldViewDir = normalize(ase_worldViewDir);
				float3 ase_worldReflection = reflect(-ase_worldViewDir, ase_worldNormal);
				float4 texCUBENode7 = texCUBE( _ReflectTex, ase_worldReflection );
				float4 temp_output_12_0 = ( _ColorA * texCUBE( _RefractTex, ase_worldReflection ) * texCUBENode7 * _RefractIntensity );
				
				
				finalColor = temp_output_12_0;
				return finalColor;
			}
			ENDCG
		}
		
		Pass
		{
			Name "Second"
			Tags { "LightMode"="ForwardBase" }

		CGINCLUDE
		#pragma target 3.0
		ENDCG
		Blend One One
		AlphaToMask Off
		Cull Back
		ColorMask RGBA
		ZWrite On
		ZTest LEqual
		Offset 0 , 0
		

			CGPROGRAM

			

			#ifndef UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX
			//only defining to not throw compilation error over Unity 5.5
			#define UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input)
			#endif
			#pragma vertex vert
			#pragma fragment frag
			#pragma multi_compile_instancing
			#include "UnityCG.cginc"
			#define ASE_NEEDS_FRAG_WORLD_POSITION


			struct appdata
			{
				float4 vertex : POSITION;
				float4 color : COLOR;
				float3 ase_normal : NORMAL;
				UNITY_VERTEX_INPUT_INSTANCE_ID
			};
			
			struct v2f
			{
				float4 vertex : SV_POSITION;
				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				float3 worldPos : TEXCOORD0;
				#endif
				float4 ase_texcoord1 : TEXCOORD1;
				UNITY_VERTEX_INPUT_INSTANCE_ID
				UNITY_VERTEX_OUTPUT_STEREO
			};

			uniform float4 _ColorA;
			uniform samplerCUBE _RefractTex;
			uniform samplerCUBE _ReflectTex;
			uniform float _RefractIntensity;
			uniform float _ReflectIntensity;
			uniform float _RimPower;
			uniform float _RimScale;
			uniform float _RimBias;
			uniform float4 _RimColor;

			
			v2f vert ( appdata v )
			{
				v2f o;
				UNITY_SETUP_INSTANCE_ID(v);
				UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(o);
				UNITY_TRANSFER_INSTANCE_ID(v, o);

				float3 ase_worldNormal = UnityObjectToWorldNormal(v.ase_normal);
				o.ase_texcoord1.xyz = ase_worldNormal;
				
				
				//setting value to unused interpolator channels and avoid initialization warnings
				o.ase_texcoord1.w = 0;
				float3 vertexValue = float3(0, 0, 0);
				#if ASE_ABSOLUTE_VERTEX_POS
				vertexValue = v.vertex.xyz;
				#endif
				vertexValue = vertexValue;
				#if ASE_ABSOLUTE_VERTEX_POS
				v.vertex.xyz = vertexValue;
				#else
				v.vertex.xyz += vertexValue;
				#endif
				o.vertex = UnityObjectToClipPos(v.vertex);

				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
				#endif
				return o;
			}
			
			fixed4 frag (v2f i ) : SV_Target
			{
				UNITY_SETUP_INSTANCE_ID(i);
				UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(i);
				fixed4 finalColor;
				#ifdef ASE_NEEDS_FRAG_WORLD_POSITION
				float3 WorldPosition = i.worldPos;
				#endif
				float3 ase_worldNormal = i.ase_texcoord1.xyz;
				float3 ase_worldViewDir = UnityWorldSpaceViewDir(WorldPosition);
				ase_worldViewDir = normalize(ase_worldViewDir);
				float3 ase_worldReflection = reflect(-ase_worldViewDir, ase_worldNormal);
				float4 texCUBENode7 = texCUBE( _ReflectTex, ase_worldReflection );
				float4 temp_output_12_0 = ( _ColorA * texCUBE( _RefractTex, ase_worldReflection ) * texCUBENode7 * _RefractIntensity );
				float dotResult21 = dot( ase_worldNormal , ase_worldViewDir );
				float clampResult23 = clamp( dotResult21 , 0.0 , 1.0 );
				float temp_output_24_0 = ( 1.0 - clampResult23 );
				float4 temp_output_16_0 = ( temp_output_12_0 + ( texCUBENode7 * _ReflectIntensity * temp_output_24_0 ) );
				float saferPower25 = max( temp_output_24_0 , 0.0001 );
				float temp_output_30_0 = ( ( max( pow( saferPower25 , _RimPower ) , 0.0 ) * _RimScale ) + _RimBias );
				
				
				finalColor = ( temp_output_16_0 + ( temp_output_16_0 * temp_output_30_0 * ( temp_output_30_0 * _RimColor ) ) );
				return finalColor;
			}
			ENDCG
		}
		
	}
	CustomEditor "ASEMaterialInspector"
	
	
}
/*ASEBEGIN
Version=18500
2500;488;1639;969;571.4478;525.8101;1.694416;True;False
Node;AmplifyShaderEditor.CommentaryNode;40;-1788.975,781.5402;Inherit;False;2012.625;729.3613;Fresnel;13;22;19;21;23;26;24;25;27;29;28;31;30;32;;1,1,1,1;0;0
Node;AmplifyShaderEditor.WorldNormalVector;19;-1738.975,831.5402;Inherit;False;False;1;0;FLOAT3;0,0,1;False;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.ViewDirInputsCoordNode;22;-1716.198,1112.462;Inherit;False;World;False;0;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.DotProductOpNode;21;-1330.5,1006.167;Inherit;False;2;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;1;FLOAT;0
Node;AmplifyShaderEditor.ClampOpNode;23;-1181.688,992.5009;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.OneMinusNode;24;-1000.987,1000.093;Inherit;False;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;26;-1107.281,1180.793;Inherit;False;Property;_RimPower;RimPower;5;0;Create;True;0;0;False;0;False;5;10;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.PowerNode;25;-809.6565,994.0192;Inherit;False;True;2;0;FLOAT;0;False;1;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.WorldReflectionVector;13;-1153.126,32.63672;Inherit;False;False;1;0;FLOAT3;0,0,0;False;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.RangedFloatNode;29;-647.2493,1140.901;Inherit;False;Property;_RimScale;RimScale;7;0;Create;True;0;0;False;0;False;0;5;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMaxOpNode;27;-617.2493,995.9019;Inherit;False;2;0;FLOAT;0;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;7;-562.063,172.0891;Inherit;True;Property;_ReflectTex;ReflectTex;2;0;Create;True;0;0;False;0;False;-1;None;7ecb52b18a453124283cee921dc388cf;True;0;False;white;LockedToCube;False;Object;-1;Auto;Cube;8;0;SAMPLERCUBE;;False;1;FLOAT3;0,0,0;False;2;FLOAT;0;False;3;FLOAT3;0,0,0;False;4;FLOAT3;0,0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.ColorNode;2;-506.5,-301.5;Inherit;False;Property;_ColorA;Color A;0;0;Create;True;0;0;False;0;False;0.02491992,0.09269338,0.754717,0;0.5754717,0.5754717,0.5754717,0;True;0;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.RangedFloatNode;17;-514.6671,98.24844;Inherit;False;Property;_RefractIntensity;RefractIntensity;4;0;Create;True;0;0;False;0;False;1;5;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;6;-570.063,-90.91089;Inherit;True;Property;_RefractTex;RefractTex;1;0;Create;True;0;0;False;0;False;-1;None;e9efb1d234a58c04cbb0a0c9eb87d214;True;0;False;white;LockedToCube;False;Object;-1;Auto;Cube;8;0;SAMPLERCUBE;;False;1;FLOAT3;0,0,0;False;2;FLOAT;0;False;3;FLOAT3;0,0,0;False;4;FLOAT3;0,0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;28;-399.2493,1052.902;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;31;-469.4467,1211.618;Inherit;False;Property;_RimBias;RimBias;6;0;Create;True;0;0;False;0;False;0;0;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;15;-466.0444,392.8555;Inherit;False;Property;_ReflectIntensity;ReflectIntensity;3;0;Create;True;0;0;False;0;False;1;1;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleAddOpNode;30;-172.2493,1094.901;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.ColorNode;36;255.3527,989.3035;Inherit;False;Property;_RimColor;RimColor;8;0;Create;True;0;0;False;0;False;0,0,0,0;0.8970588,0.8623443,0.4551255,0;True;0;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;18;-131.6671,296.2484;Inherit;False;3;3;0;COLOR;0,0,0,0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;12;-81.06299,-120.9109;Inherit;False;4;4;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;2;COLOR;0,0,0,0;False;3;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleAddOpNode;16;119.3329,185.2484;Inherit;False;2;2;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;35;460.0375,793.4158;Inherit;False;2;2;0;FLOAT;0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;33;309.5573,294.3183;Inherit;False;3;3;0;COLOR;0,0,0,0;False;1;FLOAT;0;False;2;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleAddOpNode;34;540.5623,209.1047;Inherit;False;2;2;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.FresnelNode;32;-708.2494,1308.901;Inherit;False;Standard;WorldNormal;ViewDir;False;False;5;0;FLOAT3;0,0,1;False;4;FLOAT3;0,0,0;False;1;FLOAT;0;False;2;FLOAT;1;False;3;FLOAT;5;False;1;FLOAT;0
Node;AmplifyShaderEditor.TemplateMultiPassMasterNode;39;977.4616,398.2424;Float;False;False;-1;2;ASEMaterialInspector;100;9;New Amplify Shader;0a6bbb37052a2458b860677ab2960714;True;Second;0;1;Second;2;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;True;2;RenderType=Opaque=RenderType;Queue=Geometry=Queue=0;False;0;True;4;1;False;-1;1;False;-1;0;1;False;-1;0;False;-1;True;0;False;-1;0;False;-1;False;False;False;False;False;False;True;0;False;-1;True;0;False;-1;True;True;True;True;True;0;False;-1;False;False;False;True;False;255;False;-1;255;False;-1;255;False;-1;7;False;-1;1;False;-1;1;False;-1;1;False;-1;7;False;-1;1;False;-1;1;False;-1;1;False;-1;True;0;False;-1;True;0;False;-1;True;True;0;False;-1;0;False;-1;True;1;LightMode=ForwardBase;True;2;0;;0;0;Standard;0;False;0
Node;AmplifyShaderEditor.TemplateMultiPassMasterNode;38;987.6282,-86.66805;Float;False;True;-1;2;ASEMaterialInspector;100;9;CS07/Diamond;0a6bbb37052a2458b860677ab2960714;True;Unlit;0;0;Unlit;2;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;True;2;RenderType=Opaque=RenderType;Queue=Geometry=Queue=0;False;0;True;0;1;False;-1;0;False;-1;0;1;False;-1;0;False;-1;True;0;False;-1;0;False;-1;False;False;False;False;False;False;True;0;False;-1;True;1;False;-1;True;True;True;True;True;0;False;-1;False;False;False;True;False;255;False;-1;255;False;-1;255;False;-1;7;False;-1;1;False;-1;1;False;-1;1;False;-1;7;False;-1;1;False;-1;1;False;-1;1;False;-1;True;0;False;-1;True;0;False;-1;True;True;0;False;-1;0;False;-1;True;1;LightMode=ForwardBase;True;2;0;;0;0;Standard;1;Vertex Position,InvertActionOnDeselection;1;0;2;True;True;False;;False;0
WireConnection;21;0;19;0
WireConnection;21;1;22;0
WireConnection;23;0;21;0
WireConnection;24;0;23;0
WireConnection;25;0;24;0
WireConnection;25;1;26;0
WireConnection;27;0;25;0
WireConnection;7;1;13;0
WireConnection;6;1;13;0
WireConnection;28;0;27;0
WireConnection;28;1;29;0
WireConnection;30;0;28;0
WireConnection;30;1;31;0
WireConnection;18;0;7;0
WireConnection;18;1;15;0
WireConnection;18;2;24;0
WireConnection;12;0;2;0
WireConnection;12;1;6;0
WireConnection;12;2;7;0
WireConnection;12;3;17;0
WireConnection;16;0;12;0
WireConnection;16;1;18;0
WireConnection;35;0;30;0
WireConnection;35;1;36;0
WireConnection;33;0;16;0
WireConnection;33;1;30;0
WireConnection;33;2;35;0
WireConnection;34;0;16;0
WireConnection;34;1;33;0
WireConnection;39;0;34;0
WireConnection;38;0;12;0
ASEEND*/
//CHKSM=D24C8BF7840C56CD057B1AAEC0FA1C82BDCD7B7D
```





