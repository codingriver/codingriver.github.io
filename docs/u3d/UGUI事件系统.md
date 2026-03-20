
---
title: "UGUI事件系统"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["UGUI"]
categories: ["Unity"]
---

<!--more-->


OnInutEvent.cs
```cs
//=====================================================
// - FileName:    	OnInputEvent.cs
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		#CreateTime#
// - UserName:		#AuthorName#
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.Events;
//https://docs.unity3d.com/Manual/SupportedEvents.html
//firstSelectedGameObject：这个值可以在面板设置，如果你需要游戏在启动的时候自动选中某个对象，需要鼠标的那一下点击。
//currentSelectedGameObject：当前选中的对象，你可以通过这个值判断当前是否鼠标点击在对象上，因为也许你有拖动摄像机的功能，但是你又不喜欢点击某些对象的时候这个功能又被响应，所以通过这个变量判断是一个很好的办法。
//  IsPointerOverGameObject：当前鼠标是否在事件系统可以检测的对象上。
//SetSelectedGameObject：这个接口也许你会忽略，但是它很棒。因为你点击场景对象的时候，如果不调用这个接口，你的对象是收不到OnSelect事件的，currentSelectedGameObject的值也不会被设置的，必须在点击事件里调用这个接口设置选中对象！

//EventTrigger模拟
/// <summary>
/// 
/// </summary>
public class OnInputEvent : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerDownHandler, IPointerUpHandler, IPointerClickHandler, IInitializePotentialDragHandler, IBeginDragHandler, IDragHandler, IEndDragHandler, IDropHandler, IScrollHandler, IUpdateSelectedHandler, ISelectHandler, IDeselectHandler, IMoveHandler, ISubmitHandler, ICancelHandler, IEventSystemHandler
{

	// Use this for initialization
	void Start () {
        //test
        AddListener();
        //test
        AddListenerClick(gameObject, OnClick);
	}
	
	// Update is called once per frame
    //void Update () {
		
    //}

    void Init()
    {

    }
    #region EventTrigger
    //public static void AddListener(GameObject obj, EventTriggerType type,XLua.LuaFunction func,XLua.LuaTable caller)
    public void AddListener()
    {
        var trigger= gameObject.AddComponent<EventTrigger>();
        EventTrigger.Entry entry = new EventTrigger.Entry();
        entry.eventID = EventTriggerType.PointerClick;
        entry.callback.AddListener(OnPointerClick);
        trigger.triggers.Add(entry);
        
    }
    /// <summary>
    /// 当鼠标按下并抬起
    /// 在同一物体上按下并释放
    /// </summary>
    /// <param name="eventData"></param>
    private void OnPointerClick(BaseEventData eventData)
    {
        Dg.Log("OnPoinerClick:BaseEventData:::");
    }
    #endregion

    #region event button
    public static void AddListenerClick(GameObject obj,UnityAction action)
    {
        if(obj==null)
        {
            return;
        }

        Button btn = obj.GetComponent<Button>();
        if(btn==null)
        {
            return;
        }
        btn.onClick.AddListener(action);

    }

    public static void OnClick()
    {
        Dg.Log("OnClick");
    }
    #endregion

    #region interface
    /// <summary>
    /// 当开始拖拽
    /// </summary>
    /// <param name="eventData"></param>
    public void OnBeginDrag(PointerEventData eventData)
    {
        Dg.Log("OnBeginDrag");
    }

    /// <summary>
    ///  当拖拽中
    /// </summary>
    /// <param name="eventData"></param>
    public void OnDrag(PointerEventData eventData)
    {
        Dg.Log("OnDrag");
    }
    /// <summary>
    /// 当放下
    /// 拖拽结束(拖拽结束后的位置(即鼠标位置)如果有物体，则那个物体调用)
    /// 按下的ui和抬起的ui不相同时会被调用
    /// </summary>
    /// <param name="eventData"></param>
    public void OnDrop(PointerEventData eventData)
    {
        Dg.Log("OnDrop");
    }
    /// <summary>
    /// 当结束拖拽
    /// </summary>
    /// <param name="eventData"></param>
    public void OnEndDrag(PointerEventData eventData)
    {
        Dg.Log("OnEndDrag");
    }
    /// <summary>
    /// 拖拽时的初始化，跟IPointerDownHandler差不多，在按下时调用 
    /// </summary>
    /// <param name="eventData"></param>
    public void OnInitializePotentialDrag(PointerEventData eventData)
    {
        Dg.Log("OnInitializePotentialDrag");
    }
    /// <summary>
    ///  当移动时
    ///  物体移动时(与InputManager里的Horizontal和Vertica按键相对应)，前提条件是物体被选中
    /// </summary>
    /// <param name="eventData"></param>
    public void OnMove(AxisEventData eventData)
    {
        Dg.Log("OnMove");
    }

    /// <summary>
    /// 当鼠标按下
    /// 
    /// </summary>
    /// <param name="eventData"></param>
    public void OnPointerDown(PointerEventData eventData)
    {
        Dg.Log("OnPointerDown");
    }
    /// <summary>
    /// 当鼠标按下并抬起
    /// 在同一物体上按下并释放
    /// </summary>
    /// <param name="eventData"></param>
    public void OnPointerClick(PointerEventData eventData)
    {
        Dg.Log("OnPointerClick");

        //EventSystem.current.SetSelectedGameObject(gameObject);
    }

    /// <summary>
    /// 当鼠标抬起
    /// </summary>
    /// <param name="eventData"></param>
    public void OnPointerUp(PointerEventData eventData)
    {
        Dg.Log("OnPointerUp");
    }

    /// <summary>
    ///  当鼠标进入
    /// </summary>
    /// <param name="eventData"></param>
    public void OnPointerEnter(PointerEventData eventData)
    {
        Dg.Log("OnPointerEnter");
    }

    /// <summary>
    /// 当鼠标离开
    /// </summary>
    /// <param name="eventData"></param>
    public void OnPointerExit(PointerEventData eventData)
    {
        Dg.Log("OnPointerExit");
    }

    /// <summary>
    /// 当滚动(滚轮滚动)
    /// </summary>
    /// <param name="eventData"></param>
    public void OnScroll(PointerEventData eventData)
    {
        Dg.Log("OnScroll");
    }


    /// <summary>
    /// 当对象取消选的
    /// 物体从选中到取消选中时
    /// </summary>
    /// <param name="eventData"></param>
    public void OnDeselect(BaseEventData eventData)
    {
        Dg.Log("OnDeselect");
    }

    /// <summary>
    /// 当对象变为选定
    /// 物体被选中时(EventSystem.current.SetSelectedGameObject(gameObject))
    /// </summary>
    /// <param name="eventData"></param>
    public void OnSelect(BaseEventData eventData)
    {
        Dg.Log("OnSelect");
    }
    /// <summary>
    ///  当提交按钮被按下
    ///  提交按钮被按下时(与InputManager里的Submit按键相对应，PC上默认的是Enter键)，前提条件是物体被选中
    /// <param name="eventData"></param>
    public void OnSubmit(BaseEventData eventData)
    {
        Dg.Log("OnSubmit");
    }

    /// <summary>
    ///   当取消按钮被按下
    ///   取消按钮被按下时(与InputManager里的Cancel按键相对应，PC上默认的是Esc键)，前提条件是物体被选中
    /// </summary>
    /// <param name="eventData"></param>
    public void OnCancel(BaseEventData eventData)
    {
        Dg.Log("OnCancel");
    }
    /// <summary>
    /// 当每个选择对象(被选中的物体每帧调用)
    /// </summary>
    /// <param name="eventData"></param>
    public void OnUpdateSelected(BaseEventData eventData)
    {
        Dg.Log("OnUpdateSelected");
    }
    #endregion

}

```
