# UGUI-Text换行问题

>UGUI关于富文本RichText参考 [UGUI使用富文本RichText](UGUI使用富文本RichText.md)

>可能有些开发人员碰到过做开发时发现UGUI的Text不能换行，有的朋友就会说可以通过`\n`换行，并附上了整条字符串，但解决办法并非如此。  
>这么说吧，通过代码直接给Text组件的text赋值`"<color=red>XXXX</color>\nXXXX"`绝对是可以换行效果的；然而，在Inspector面板的Text组件里输入同样的内容就不行，哪怕手动复制进去都不对，那出现这个问题的原因是为什么？  
>后来发现，原来它把`\n`偷偷变成了`\\n`了，所以我们只要把它变回来就行啦！  

```csharp
using UnityEngine;  
using UnityEngine.UI;  
public class RyanTextLineFeed : MonoBehaviour  
{  
    Text myText;  
    void Start ()  
    {  
        myText = GetComponent<Text> ();  
        myText.text = myText.text.Replace ("\\n", "\n");  
    }  
}  

```
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/UGUI-Text换行问题/20201006135345.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/UGUI-Text换行问题/20201006135359.png)  



>转自：[UGUI Text换行问题](https://gameinstitute.qq.com/community/detail/118697)