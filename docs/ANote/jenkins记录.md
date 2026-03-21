---
title: "jenkins记录"
date: "2026-03-21"
tags:
  - 随笔
  - 笔记
  - Jenkins
  - 工具链
  - 项目记录
categories:
  - ANote
comments: true
---
# jenkins记录

mac 安装目录：`/usr/local/Cellar/jenkins-lts/2.235.5/bin`

---

<details>
  <summary><strong>LabRat</strong>: Place arrows on the board to route the most mice into your home base.<br><i>Click here for details</i></summary>
    
   <ul>
<li>Mice spawn at frequent, randomized intervals from locations randomly chosen at startup.</li>
<li>The board has holes at random locations, both mice and cats can fall into those holes and despawn when that happens.</li>
<li>At start of play, walls are randomly placed between grid cells.</li>
<li>Cats and mice travel on the grid, changing direction when they hit a wall or travel over an arrow.</li>
<li>Cats spawn in random squares. When a cat and mouse intersect, the mouse is eaten.</li>
<li>When a mouse hits a player's 'home base' (one of the four dots placed near the center of the grid), the mouse disappears, and the player is awarded a point.</li>
<li>Similarly, when a cat hits a player's 'home base', the cat disappears, and the player gets negative points.</li>
<li>Players can place arrows in cells of the board. The green player places green arrows, the red player places red arrows, etc. A player cannot place their arrows in a cell occupied by an arrow of another player.</li>
<li>Once a player has three arrows on the board, their next placed arrow removes their oldest arrow on the board.</li>
<li>Only one player is human. The AI players just place their arrows randomly at random intervals.</li>
<li>At the end of 30 seconds, the player with the most points wins.</li>
<li>Keyboard controls allow the user to reset the simulation.</li>
<li>Walls can be added at runtime by left clicking while holding the shift key down.</li>
   </ul>
</details>
![Lab Rat](image/jenkins记录/LabRat.gif)

---