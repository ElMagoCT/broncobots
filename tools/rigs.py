#!/usr/bin/env python3
"""
Robot figures for the scroll rigs.

Every figure is a plain inline <svg class="rig-svg"> that uses the shared
material classes from style.css (.fr .fr2 .ac .wire .dim .lbl ...) and exposes
animated pieces through data-part="..." hooks. assets/js/site.js drives those
hooks; with JS off each figure simply renders in its resting pose.

build.py substitutes __RIG:name__ in a content file with RIGS["name"].

Keeping them here rather than inline in the pages means all sixteen share one
vocabulary — same stroke weights, same hole pattern, same gear teeth — which is
what makes very different animations still read as one machine shop.
"""

import math

# --------------------------------------------------------------------------
# shared geometry helpers
# --------------------------------------------------------------------------

def gear(cx, cy, r, teeth=12, depth=None, cls="fr"):
    """A proper involute-ish gear outline. Used anywhere a gear appears so
    every gear on the site has identical tooth geometry."""
    depth = depth or r * 0.22
    pts = []
    step = math.pi / teeth
    for i in range(teeth):
        a0 = 2 * step * i
        for rad, a in ((r, a0 - step * 0.42), (r + depth, a0 - step * 0.20),
                       (r + depth, a0 + step * 0.20), (r, a0 + step * 0.42),
                       (r, a0 + step * 0.58), (r - 0.02, a0 + step * 1.42)):
            pts.append("%.1f,%.1f" % (cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return ('<polygon class="%s" points="%s"/>'
            '<circle class="hole" cx="%.1f" cy="%.1f" r="%.1f"/>'
            % (cls, " ".join(pts), cx, cy, r * 0.34))


def holes(x, y, n, gap=18, r=3.2):
    """Lightening holes — the repeating motif on every chassis plate."""
    return "".join('<circle class="hole" cx="%.0f" cy="%.0f" r="%.1f"/>'
                   % (x + i * gap, y, r) for i in range(n))


def wheel(cx, cy, r=22):
    return ('<circle class="fr3" cx="%d" cy="%d" r="%d"/>'
            '<circle class="hole" cx="%d" cy="%d" r="%d"/>'
            '<circle class="acf" cx="%d" cy="%d" r="4"/>'
            % (cx, cy, r, cx, cy, int(r * .55), cx, cy))


def chassis(x, y, w, h, label=""):
    """The standard robot body — reused at three scales."""
    s = ('<rect class="fr" x="%d" y="%d" width="%d" height="%d" rx="4"/>' % (x, y, w, h))
    s += holes(x + 16, y + h / 2, max(2, int((w - 24) // 18)), 18, min(4, h / 7))
    if label:
        s += ('<text class="lbl-b" x="%d" y="%d" text-anchor="middle">%s</text>'
              % (x + w / 2, y + h - 8, label))
    return s


# --------------------------------------------------------------------------
# 1. HOME — flywheel shooter
# --------------------------------------------------------------------------
SHOOTER = """
<svg class="rig-svg" viewBox="0 0 900 380" role="img"
     aria-label="A robot drives onto the field, elevates its shooter, spins up a flywheel and scores a ball through the goal.">
  <line class="floor" x1="20" y1="331" x2="880" y2="331"/>
  <g class="dim-solid" opacity=".45">
    <line x1="20" y1="340" x2="20" y2="352"/><line x1="880" y1="340" x2="880" y2="352"/>
    <line x1="20" y1="346" x2="880" y2="346" stroke-dasharray="5 4"/>
  </g>
  <text class="lbl" x="450" y="366" text-anchor="middle">FIELD &mdash; 12 FT</text>

  <!-- goal -->
  <g>
    <rect class="fr2" x="846" y="52" width="15" height="130" rx="3"/>
    <path class="wire" d="M846 182 L866 182 L866 331"/>
    <ellipse data-part="goalflash" cx="812" cy="150" rx="46" ry="16" fill="none"
             stroke="var(--ac)" stroke-width="4" opacity="0"/>
    <ellipse class="ac" cx="812" cy="150" rx="34" ry="9" fill="none" stroke-width="5"/>
    <path class="wire" d="M786 156 L790 184 M838 156 L834 184" opacity=".6"/>
    <text data-part="swish" class="lbl-ac" x="812" y="112" text-anchor="middle" opacity="0">SWISH</text>
  </g>

  <!-- flight arc -->
  <path data-part="arc" class="dim" d="M402 196 Q 620 -40 812 150" stroke="var(--ac)" opacity=".8"/>

  <!-- robot -->
  <g data-part="bot">
    <g data-part="turret">
      <rect class="fr2" x="368" y="212" width="72" height="38" rx="6"/>
      <polygon class="ac" points="428,214 452,196 460,208 436,232"/>
      <circle class="fr3" cx="398" cy="206" r="27"/>
      <g data-part="wheel">
        <circle class="hole" cx="398" cy="206" r="17"/>
        <line class="wire" x1="381" y1="206" x2="415" y2="206"/>
        <line class="wire" x1="398" y1="189" x2="398" y2="223"/>
        <circle class="acf" cx="398" cy="206" r="5"/>
      </g>
    </g>
    <rect class="fr" x="286" y="252" width="190" height="62" rx="5"/>
    <rect class="fr3" x="298" y="264" width="46" height="38" rx="3"/>
    <text class="lbl" x="321" y="288" text-anchor="middle">991</text>
    <g>__HOLES__</g>
    <g data-part="charge-row">
      <rect data-part="charge" class="acf" x="366" y="290" width="14" height="8" opacity=".25"/>
      <rect data-part="charge" class="acf" x="384" y="290" width="14" height="8" opacity=".25"/>
      <rect data-part="charge" class="acf" x="402" y="290" width="14" height="8" opacity=".25"/>
      <rect data-part="charge" class="acf" x="420" y="290" width="14" height="8" opacity=".25"/>
      <rect data-part="charge" class="acf" x="438" y="290" width="14" height="8" opacity=".25"/>
    </g>
    __WHEELS__
  </g>

  <!-- ball -->
  <circle data-part="ball" class="ac" cx="402" cy="196" r="14" stroke-width="2.6"/>

  <!-- readout -->
  <g>
    <rect class="fr3" x="34" y="40" width="196" height="88" rx="4"/>
    <text class="lbl" x="50" y="64">MATCH STATUS</text>
    <text data-part="status" class="lbl-ac" x="50" y="90" font-size="19">DRIVING</text>
    <text class="lbl" x="50" y="116">SCORE</text>
    <text data-part="score" class="lbl-b" x="212" y="118" font-size="28" text-anchor="end">0</text>
    <g transform="translate(150,56)">
      <circle data-part="led" class="acf" cx="0" cy="0" r="5" opacity=".22"/>
      <circle data-part="led" class="acf" cx="16" cy="0" r="5" opacity=".22"/>
      <circle data-part="led" class="acf" cx="32" cy="0" r="5" opacity=".22"/>
      <circle data-part="led" class="acf" cx="48" cy="0" r="5" opacity=".22"/>
    </g>
  </g>
</svg>
""".replace("__HOLES__", holes(360, 270, 6, 19, 4.4)).replace(
    "__WHEELS__", wheel(326, 314) + wheel(436, 314))


# --------------------------------------------------------------------------
# 2. TEAMS — three robots to scale
# --------------------------------------------------------------------------
SCALE = """
<svg class="rig-svg" viewBox="0 0 760 340" role="img"
     aria-label="The three programs drawn to scale: a small LEGO robot, an eighteen-inch FTC robot, and a large FRC robot.">
  <path data-part="floor-line" class="floor" d="M30 296 L730 296"/>

  <g data-part="bot-fll" data-module="fll" opacity="0">
    <g transform="translate(96,0)">
      <rect class="fr" x="-34" y="248" width="68" height="42" rx="4"/>
      <rect class="fr2" x="-20" y="230" width="40" height="20" rx="3"/>
      <circle class="fr3" cx="-20" cy="290" r="11"/><circle class="fr3" cx="20" cy="290" r="11"/>
      <circle class="acf" cx="0" cy="240" r="5"/>
    </g>
    <text data-part="lbl-fll" class="lbl-b" x="96" y="322" text-anchor="middle" opacity="0">FLL</text>
  </g>
  <path data-part="dim-fll" class="dim" d="M50 296 L50 228 M44 228 L56 228"/>
  <text class="lbl" x="34" y="222" text-anchor="middle">~9&Prime;</text>

  <g data-part="bot-ftc" data-module="ftc" opacity="0">
    <g transform="translate(330,0)">
      <rect class="ghost" x="-62" y="172" width="124" height="124"/>
      <rect class="fr" x="-52" y="212" width="104" height="70" rx="5"/>
      __FTCHOLES__
      <rect class="fr2" x="-30" y="184" width="46" height="30" rx="4"/>
      <path class="wire" d="M16 190 L52 178"/>
      <circle class="fr3" cx="-30" cy="284" r="15"/><circle class="fr3" cx="30" cy="284" r="15"/>
      <circle class="acf" cx="-30" cy="284" r="4"/><circle class="acf" cx="30" cy="284" r="4"/>
    </g>
    <text data-part="lbl-ftc" class="lbl-b" x="330" y="322" text-anchor="middle" opacity="0">FTC</text>
  </g>
  <path data-part="dim-ftc" class="dim" d="M252 296 L252 172 M246 172 L258 172"/>
  <text class="lbl" x="236" y="166" text-anchor="middle">18&Prime;</text>

  <g data-part="bot-frc" data-module="frc" opacity="0">
    <g transform="translate(600,0)">
      <rect class="fr" x="-88" y="176" width="176" height="106" rx="6"/>
      __FRCHOLES__
      <rect class="fr2" x="-54" y="112" width="70" height="66" rx="5"/>
      <polygon class="ac" points="16,120 74,96 82,112 24,138"/>
      <circle class="fr3" cx="-54" cy="284" r="24"/><circle class="fr3" cx="0" cy="284" r="24"/>
      <circle class="fr3" cx="54" cy="284" r="24"/>
      <circle class="acf" cx="-54" cy="284" r="6"/><circle class="acf" cx="0" cy="284" r="6"/>
      <circle class="acf" cx="54" cy="284" r="6"/>
      <text class="lbl" x="0" y="238" text-anchor="middle">991</text>
    </g>
    <text data-part="lbl-frc" class="lbl-b" x="600" y="322" text-anchor="middle" opacity="0">FRC</text>
  </g>
  <path data-part="dim-frc" class="dim" d="M486 296 L486 112 M480 112 L492 112"/>
  <text class="lbl" x="468" y="106" text-anchor="middle">~48&Prime;</text>
</svg>
""".replace("__FTCHOLES__", holes(-34, 247, 5, 18, 4)).replace(
    "__FRCHOLES__", holes(-64, 229, 8, 19, 5))


# --------------------------------------------------------------------------
# 3. FRC — telescoping elevator
# --------------------------------------------------------------------------
LIFT = """
<svg class="rig-svg" viewBox="0 0 620 500" role="img"
     aria-label="A three-stage elevator telescopes upward and places a game piece on the high goal.">
  <line class="floor" x1="40" y1="452" x2="580" y2="452"/>

  <!-- goal -->
  <g>
    <rect class="fr2" x="500" y="120" width="72" height="14" rx="3"/>
    <path class="wire" d="M536 134 L536 452"/>
    <text class="lbl" x="536" y="108" text-anchor="middle">HIGH GOAL</text>
    <rect data-part="placed" class="ac" x="518" y="96" width="34" height="26" rx="4" opacity="0"/>
  </g>

  <!-- height readout -->
  <g>
    <rect class="fr3" x="40" y="60" width="150" height="70" rx="4"/>
    <text class="lbl" x="56" y="84">EXTENSION</text>
    <text data-part="height" class="lbl-ac" x="56" y="114" font-size="24">0 in</text>
  </g>
  <g>
    <text data-part="stagelbl" class="lbl" x="222" y="404" opacity=".35">STAGE 1</text>
    <text data-part="stagelbl" class="lbl" x="222" y="384" opacity=".35">STAGE 2</text>
    <text data-part="stagelbl" class="lbl" x="222" y="364" opacity=".35">STAGE 3</text>
  </g>

  <!-- elevator, drawn bottom-up so stages nest -->
  <g data-part="stage1">
    <rect class="fr3" x="352" y="236" width="26" height="180" rx="4"/>
    <rect class="fr3" x="470" y="236" width="26" height="180" rx="4"/>
    <g data-part="stage2">
      <rect class="fr2" x="362" y="200" width="20" height="176" rx="3"/>
      <rect class="fr2" x="466" y="200" width="20" height="176" rx="3"/>
      <g data-part="stage3">
        <rect class="fr" x="372" y="168" width="15" height="172" rx="3"/>
        <rect class="fr" x="461" y="168" width="15" height="172" rx="3"/>
      </g>
    </g>
  </g>

  <!-- chain -->
  <path data-part="chain" class="wire" d="M424 416 L424 176" stroke-dasharray="8 7" opacity=".55"/>

  <!-- carriage + claw -->
  <g data-part="carriage">
    <rect class="fr" x="386" y="396" width="84" height="34" rx="4"/>
    __CARHOLES__
    <g transform="translate(0,278)">
      <path data-part="jaw-l" class="ac" d="M404 118 L392 92 L404 86 L416 112 Z"/>
      <path data-part="jaw-r" class="ac" d="M452 118 L464 92 L452 86 L440 112 Z"/>
    </g>
  </g>
  <rect data-part="piece" class="ac" x="411" y="384" width="34" height="26" rx="4"/>

  <!-- base -->
  <g>
    <rect class="fr" x="330" y="416" width="188" height="36" rx="5"/>
    __BASEHOLES__
    __LIFTWHEELS__
  </g>
</svg>
""".replace("__CARHOLES__", holes(400, 413, 4, 18, 4)).replace(
    "__BASEHOLES__", holes(348, 434, 8, 19, 4.4)).replace(
    "__LIFTWHEELS__", wheel(362, 452, 20) + wheel(486, 452, 20))


# --------------------------------------------------------------------------
# 4. FTC — the 18-inch cube rule
# --------------------------------------------------------------------------
CUBE = """
<svg class="rig-svg" viewBox="0 0 700 460" role="img"
     aria-label="An FTC robot starts folded inside the eighteen-inch starting cube, then unfolds an arm out beyond it during the match.">
  <line class="floor" x1="40" y1="392" x2="660" y2="392"/>

  <!-- the 18in cube, drawn edge by edge -->
  <g>
    <path data-part="cube-edge" class="ghost" d="M150 392 L150 172"/>
    <path data-part="cube-edge" class="ghost" d="M150 172 L370 172"/>
    <path data-part="cube-edge" class="ghost" d="M370 172 L370 392"/>
    <path data-part="cube-edge" class="ghost" d="M150 172 L206 124"/>
    <path data-part="cube-edge" class="ghost" d="M206 124 L426 124"/>
    <path data-part="cube-edge" class="ghost" d="M426 124 L370 172"/>
    <path data-part="cube-edge" class="ghost" d="M426 124 L426 344"/>
    <path data-part="cube-edge" class="ghost" d="M370 392 L426 344"/>
  </g>
  <path data-part="cube-dim" class="dim" d="M132 392 L132 172 M126 172 L138 172 M126 392 L138 392"/>
  <text data-part="cube-lbl" class="lbl" x="112" y="288" text-anchor="middle" opacity="0"
        transform="rotate(-90 112 288)">18 INCHES</text>

  <text data-part="stamp-legal" class="lbl-ac" x="260" y="152" text-anchor="middle" opacity="0">LEGAL AT START</text>
  <text data-part="stamp-expand" class="lbl-ac" x="566" y="286" text-anchor="middle" opacity="0">EXPANDS IN MATCH</text>
  <path data-part="reach-dim" class="dim" d="M370 412 L460 412 M460 406 L460 418 M370 406 L370 418"/>
  <text data-part="reach-lbl" class="lbl" x="415" y="434" text-anchor="middle" opacity="0">BEYOND START VOLUME</text>

  <!-- scoring target the arm reaches -->
  <g data-part="outside" opacity="0">
    <rect class="fr2" x="416" y="110" width="88" height="14" rx="3"/>
    <path class="wire" d="M460 124 L460 392"/>
    <text class="lbl" x="460" y="100" text-anchor="middle">GOAL</text>
  </g>

  <!-- robot -->
  <g>
    <rect class="fr" x="212" y="300" width="150" height="66" rx="5"/>
    __CUBEHOLES__
    <text class="lbl" x="287" y="342" text-anchor="middle">23737</text>
    __CUBEWHEELS__
    <!-- arm pivots at 300,268 -->
    <g data-part="arm-lower" transform="rotate(-95 300 268)">
      <rect class="fr2" x="292" y="152" width="17" height="120" rx="4"/>
      <circle class="fr3" cx="300" cy="268" r="13"/>
      <circle class="acf" cx="300" cy="268" r="5"/>
      <g data-part="arm-upper" transform="rotate(165 300 152)">
        <rect class="fr" x="294" y="52" width="14" height="108" rx="4"/>
        <g transform="translate(301,54)">
          <g data-part="intake">
            <circle class="ac" cx="0" cy="0" r="19" fill="none" stroke-width="5"/>
            <line class="wire" x1="-19" y1="0" x2="19" y2="0"/>
            <line class="wire" x1="0" y1="-19" x2="0" y2="19"/>
          </g>
        </g>
      </g>
    </g>
  </g>

  <!-- phase readout, kept clear of the goal at x416-504 -->
  <g>
    <rect class="fr3" x="512" y="34" width="176" height="62" rx="4"/>
    <text class="lbl" x="528" y="56">PHASE</text>
    <text data-part="phase" class="lbl-ac" x="528" y="82" font-size="19">INSPECTION</text>
  </g>
</svg>
""".replace("__CUBEHOLES__", holes(232, 333, 7, 18, 4.4)).replace(
    "__CUBEWHEELS__", wheel(244, 366, 19) + wheel(330, 366, 19))


# --------------------------------------------------------------------------
# 5. FLL — mission table + block code
# --------------------------------------------------------------------------
MISSION = """
<svg class="rig-svg" viewBox="0 0 760 360" role="img"
     aria-label="A LEGO robot drives a route across the mission table while its block program assembles alongside.">
  <rect class="fr3" x="212" y="28" width="520" height="300" rx="6" opacity=".35"/>
  <text class="lbl" x="472" y="350" text-anchor="middle">MISSION TABLE</text>

  <path data-part="route" class="dim" stroke="var(--ac)" stroke-dasharray="0"
        d="M258 288 C 320 288 320 200 384 200 S 470 96 552 118 S 668 200 690 262"/>

  <g data-part="mission" opacity=".4" transform="translate(384,200)">
    <rect class="ac" x="-17" y="-17" width="34" height="34" rx="3"/>
    <text class="lbl" x="0" y="-28" text-anchor="middle">M1</text>
  </g>
  <g data-part="mission" opacity=".4" transform="translate(552,118)">
    <circle class="ac" cx="0" cy="0" r="18"/>
    <text class="lbl" x="0" y="-28" text-anchor="middle">M2</text>
  </g>
  <g data-part="mission" opacity=".4" transform="translate(690,262)">
    <polygon class="ac" points="0,-20 18,10 -18,10"/>
    <text class="lbl" x="0" y="-30" text-anchor="middle">M3</text>
  </g>

  <g data-part="bot">
    <rect class="fr" x="-19" y="-14" width="38" height="28" rx="4"/>
    <circle class="fr3" cx="-11" cy="15" r="7"/><circle class="fr3" cx="11" cy="15" r="7"/>
    <circle class="acf" cx="14" cy="0" r="4"/>
  </g>

  <!-- block program -->
  <g>
    <text class="lbl" x="20" y="44">PROGRAM</text>
    <g data-part="block" opacity="0">
      <rect class="ac" x="20" y="58" width="150" height="34" rx="5"/>
      <text class="lbl" x="34" y="80" fill="#fff">drive 40 cm</text>
    </g>
    <g data-part="block" opacity="0">
      <rect class="fr2" x="20" y="100" width="150" height="34" rx="5"/>
      <text class="lbl" x="34" y="122">turn 90&deg;</text>
    </g>
    <g data-part="block" opacity="0">
      <rect class="ac" x="20" y="142" width="150" height="34" rx="5"/>
      <text class="lbl" x="34" y="164" fill="#fff">arm down</text>
    </g>
    <g data-part="block" opacity="0">
      <rect class="fr2" x="20" y="184" width="150" height="34" rx="5"/>
      <text class="lbl" x="34" y="206">repeat 3&times;</text>
    </g>
  </g>
  <g>
    <text class="lbl" x="20" y="264">MISSIONS</text>
    <text data-part="count" class="lbl-ac" x="20" y="294" font-size="24">0/3</text>
  </g>
</svg>
"""


# --------------------------------------------------------------------------
# 6. ABOUT — the creed as a gear train
# --------------------------------------------------------------------------
GEARS = """
<svg class="rig-svg" viewBox="0 0 600 300" role="img"
     aria-label="Three interlocking gears labelled Trust, Respect and Commitment turning together.">
  <path data-part="belt" class="dim" d="M132 240 L462 240" stroke="var(--ac)"/>
  <g data-part="g1">__G1__</g>
  <g data-part="g2">__G2__</g>
  <g data-part="g3">__G3__</g>
  <text data-part="gearlbl" class="lbl-b" x="132" y="278" text-anchor="middle" opacity="0">TRUST</text>
  <text data-part="gearlbl" class="lbl-b" x="300" y="278" text-anchor="middle" opacity="0">RESPECT</text>
  <text data-part="gearlbl" class="lbl-b" x="462" y="278" text-anchor="middle" opacity="0">COMMITMENT</text>
</svg>
""".replace("__G1__", gear(132, 168, 58, 14, cls="fr")) \
   .replace("__G2__", gear(300, 168, 52, 12, cls="ac")) \
   .replace("__G3__", gear(462, 168, 58, 14, cls="fr"))


# --------------------------------------------------------------------------
# 7. LEADERSHIP — control hub wiring out to subteams
# --------------------------------------------------------------------------
SIGNAL = """
<svg class="rig-svg" viewBox="0 0 700 330" role="img"
     aria-label="A control hub sending a signal out along wires to each student-led subteam.">
  <g data-part="hub" opacity=".5">
    <rect class="fr" x="292" y="130" width="116" height="70" rx="6"/>
    __HUBHOLES__
    <text class="lbl-b" x="350" y="160" text-anchor="middle">STUDENT</text>
    <text class="lbl-b" x="350" y="180" text-anchor="middle">LEADERSHIP</text>
  </g>

  <path data-part="sigwire" class="wire-ac" d="M292 150 C 220 150 210 74 148 74"/>
  <path data-part="sigwire" class="wire-ac" d="M292 165 C 210 165 200 165 128 165"/>
  <path data-part="sigwire" class="wire-ac" d="M292 182 C 220 182 210 256 148 256"/>
  <path data-part="sigwire" class="wire-ac" d="M408 150 C 480 150 490 74 552 74"/>
  <path data-part="sigwire" class="wire-ac" d="M408 165 C 490 165 500 165 572 165"/>
  <path data-part="sigwire" class="wire-ac" d="M408 182 C 480 182 490 256 552 256"/>

  <g data-part="signode" opacity=".45"><rect class="fr2" x="26" y="54" width="122" height="40" rx="4"/>
    <text class="lbl" x="87" y="79" text-anchor="middle">MECHANICAL</text></g>
  <g data-part="signode" opacity=".45"><rect class="fr2" x="6" y="145" width="122" height="40" rx="4"/>
    <text class="lbl" x="67" y="170" text-anchor="middle">SOFTWARE</text></g>
  <g data-part="signode" opacity=".45"><rect class="fr2" x="26" y="236" width="122" height="40" rx="4"/>
    <text class="lbl" x="87" y="261" text-anchor="middle">ELECTRICAL</text></g>
  <g data-part="signode" opacity=".45"><rect class="fr2" x="552" y="54" width="122" height="40" rx="4"/>
    <text class="lbl" x="613" y="79" text-anchor="middle">STRATEGY</text></g>
  <g data-part="signode" opacity=".45"><rect class="fr2" x="572" y="145" width="122" height="40" rx="4"/>
    <text class="lbl" x="633" y="170" text-anchor="middle">BUSINESS</text></g>
  <g data-part="signode" opacity=".45"><rect class="fr2" x="552" y="236" width="122" height="40" rx="4"/>
    <text class="lbl" x="613" y="261" text-anchor="middle">DRIVE TEAM</text></g>

  <text class="lbl" x="350" y="304" text-anchor="middle">SUBTEAMS REPORTING</text>
  <text data-part="count" class="lbl-ac" x="350" y="326" font-size="18" text-anchor="middle">0/6</text>
</svg>
""".replace("__HUBHOLES__", holes(308, 194, 5, 20, 4))


# --------------------------------------------------------------------------
# 8. RESULTS — alliance scoreboard
# --------------------------------------------------------------------------
BOARD = """
<svg class="rig-svg" viewBox="0 0 700 330" role="img"
     aria-label="A match scoreboard filling in with red and blue alliance scores.">
  <rect class="fr3" x="24" y="20" width="652" height="290" rx="6" opacity=".4"/>
  <text class="lbl" x="350" y="50" text-anchor="middle">QUALIFICATION MATCH</text>

  <text class="lbl" x="60" y="96">BLUE ALLIANCE</text>
  <rect class="fr2" x="60" y="106" width="310" height="26" rx="3" opacity=".5"/>
  <rect data-part="bar-blue" x="60" y="106" width="0" height="26" rx="3" fill="#2f6fa6"/>
  <text data-part="blue" class="lbl-b" x="640" y="128" text-anchor="end" font-size="30">0</text>

  <text class="lbl" x="60" y="178">RED ALLIANCE</text>
  <rect class="fr2" x="60" y="188" width="310" height="26" rx="3" opacity=".5"/>
  <rect data-part="bar-red" x="60" y="188" width="0" height="26" rx="3" fill="var(--ac)"/>
  <text data-part="red" class="lbl-b" x="640" y="210" text-anchor="end" font-size="30">0</text>

  <g data-part="brow" opacity="0"><text class="lbl" x="60" y="248">991 &mdash; BROPHY BRONCOBOTS</text>
    <text class="lbl" x="470" y="248">AUTO 27</text></g>
  <g data-part="brow" opacity="0"><text class="lbl" x="60" y="272">ALLIANCE PARTNER</text>
    <text class="lbl" x="470" y="272">TELEOP 61</text></g>
  <g data-part="brow" opacity="0"><text class="lbl" x="60" y="296">ENDGAME</text>
    <text class="lbl" x="470" y="296">CLIMB 10</text></g>

  <text data-part="winner" class="lbl-ac" x="640" y="70" text-anchor="end" font-size="20" opacity="0">RED WINS</text>
</svg>
"""


# --------------------------------------------------------------------------
# 9. PARENTS — a real 2:30 match clock
# --------------------------------------------------------------------------
MATCHCLOCK = """
<svg class="rig-svg" viewBox="0 0 700 420" role="img"
     aria-label="A two minute thirty second match clock: thirty seconds autonomous, two minutes driver-controlled, then endgame.">
  <!-- clock -->
  <g transform="translate(120,120)">
    <circle class="fr3" r="86" opacity=".35"/>
    <circle r="72" fill="none" stroke="var(--dim-c)" stroke-width="9" opacity=".35"/>
    <circle data-part="ring" r="72" fill="none" stroke="var(--ac)" stroke-width="9"
            stroke-linecap="round" transform="rotate(-90)"/>
    <text data-part="time" class="lbl-b" y="10" font-size="34" text-anchor="middle">2:30</text>
    <text class="lbl" y="34" text-anchor="middle">REMAINING</text>
  </g>
  <text data-part="phase" class="lbl-ac" x="120" y="238" font-size="17" text-anchor="middle">AUTONOMOUS</text>
  <text data-part="note" class="lbl" x="120" y="260" text-anchor="middle">No driver input allowed</text>

  <!-- phase bar -->
  <g transform="translate(256,44)">
    <g data-part="pseg"><rect class="fr2" x="0" y="0" width="76" height="20" rx="3"/>
      <text class="lbl" x="38" y="15" text-anchor="middle">AUTO</text></g>
    <g data-part="pseg"><rect class="fr2" x="82" y="0" width="228" height="20" rx="3"/>
      <text class="lbl" x="196" y="15" text-anchor="middle">DRIVER-CONTROLLED</text></g>
    <g data-part="pseg"><rect class="fr2" x="316" y="0" width="76" height="20" rx="3"/>
      <text class="lbl" x="354" y="15" text-anchor="middle">ENDGAME</text></g>
  </g>

  <!-- field -->
  <line class="floor" x1="256" y1="352" x2="672" y2="352"/>
  <path data-part="auto-path" class="dim" stroke="var(--ac)" d="M300 336 L420 336"/>

  <!-- climb bar -->
  <g data-part="bar-climb" opacity="0">
    <rect class="fr2" x="596" y="196" width="66" height="12" rx="3"/>
    <path class="wire" d="M629 208 L629 352"/>
    <text class="lbl" x="629" y="188" text-anchor="middle">CLIMB</text>
  </g>

  <g data-part="bot" transform="translate(0,0)">
    <g transform="translate(300,0)">
      <rect class="fr" x="-34" y="304" width="68" height="34" rx="4"/>
      __MCHOLES__
      <circle class="fr3" cx="-18" cy="340" r="12"/><circle class="fr3" cx="18" cy="340" r="12"/>
      <circle class="acf" cx="-18" cy="340" r="3.5"/><circle class="acf" cx="18" cy="340" r="3.5"/>
    </g>
  </g>

  <g data-part="driver" opacity="0" transform="translate(286,250)">
    <circle class="fr2" cx="0" cy="0" r="13"/>
    <path class="fr2" d="M-15 40 Q 0 16 15 40 Z"/>
    <rect class="ac" x="-16" y="20" width="32" height="13" rx="3"/>
    <text class="lbl" x="0" y="60" text-anchor="middle">DRIVER</text>
  </g>
</svg>
""".replace("__MCHOLES__", holes(-20, 321, 3, 19, 4))


# --------------------------------------------------------------------------
# 10. SUPPORT — sponsorship as power distribution
# --------------------------------------------------------------------------
POWER = """
<svg class="rig-svg" viewBox="0 0 700 320" role="img"
     aria-label="A battery feeding power out through a distribution panel to each part of the program.">
  <g>
    <rect class="fr" x="30" y="106" width="118" height="100" rx="6"/>
    <text class="lbl" x="89" y="130" text-anchor="middle">SUPPORT</text>
    <g transform="translate(46,142)">
      <rect data-part="cell" class="acf" x="0" y="0" width="17" height="30" opacity=".22"/>
      <rect data-part="cell" class="acf" x="22" y="0" width="17" height="30" opacity=".22"/>
      <rect data-part="cell" class="acf" x="44" y="0" width="17" height="30" opacity=".22"/>
      <rect data-part="cell" class="acf" x="66" y="0" width="17" height="30" opacity=".22"/>
    </g>
    <text data-part="volts" class="lbl-ac" x="89" y="196" text-anchor="middle" font-size="17">0.0V</text>
  </g>

  <rect class="fr2" x="212" y="96" width="52" height="120" rx="5"/>
  <text class="lbl" x="238" y="86" text-anchor="middle">PDP</text>
  <path class="wire-ac" d="M148 156 L212 156"/>

  <path data-part="trace" class="wire-ac" d="M264 116 C 330 116 340 42 410 42"/>
  <path data-part="trace" class="wire-ac" d="M264 140 C 340 140 350 112 424 112"/>
  <path data-part="trace" class="wire-ac" d="M264 172 C 340 172 350 200 424 200"/>
  <path data-part="trace" class="wire-ac" d="M264 196 C 330 196 340 270 410 270"/>

  <g data-part="loadnode" opacity=".42"><rect class="fr2" x="410" y="22" width="252" height="40" rx="4"/>
    <text class="lbl" x="426" y="47">REGISTRATION &amp; EVENT FEES</text></g>
  <g data-part="loadnode" opacity=".42"><rect class="fr2" x="424" y="92" width="238" height="40" rx="4"/>
    <text class="lbl" x="440" y="117">MATERIALS &amp; SPARE PARTS</text></g>
  <g data-part="loadnode" opacity=".42"><rect class="fr2" x="424" y="180" width="238" height="40" rx="4"/>
    <text class="lbl" x="440" y="205">TOOLS &amp; SHOP EQUIPMENT</text></g>
  <g data-part="loadnode" opacity=".42"><rect class="fr2" x="410" y="250" width="252" height="40" rx="4"/>
    <text class="lbl" x="426" y="275">OUTREACH &amp; FLL MENTORING</text></g>
</svg>
"""


# --------------------------------------------------------------------------
# 11. CALENDAR — a robot driving the season
# --------------------------------------------------------------------------
TRACK = """
<svg class="rig-svg" viewBox="0 0 760 220" role="img"
     aria-label="A robot driving along a track marked with the months of the season.">
  <path data-part="rail" class="wire-ac" fill="none"
        d="M40 150 L160 150 L230 122 L330 122 L400 150 L520 150 L590 108 L720 108"/>
  <path class="dim" d="M40 150 L160 150 L230 122 L330 122 L400 150 L520 150 L590 108 L720 108" opacity=".4"/>

  <g data-part="month" opacity=".38"><circle class="fr3" cx="40" cy="150" r="8"/><text class="lbl" x="40" y="178" text-anchor="middle">AUG</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="115" cy="150" r="8"/><text class="lbl" x="115" y="178" text-anchor="middle">SEP</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="196" cy="136" r="8"/><text class="lbl" x="196" y="112" text-anchor="middle">OCT</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="278" cy="122" r="8"/><text class="lbl" x="278" y="100" text-anchor="middle">NOV</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="360" cy="134" r="8"/><text class="lbl" x="360" y="112" text-anchor="middle">DEC</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="440" cy="150" r="8"/><text class="lbl" x="440" y="178" text-anchor="middle">JAN</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="520" cy="150" r="8"/><text class="lbl" x="520" y="178" text-anchor="middle">FEB</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="580" cy="115" r="8"/><text class="lbl" x="580" y="94" text-anchor="middle">MAR</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="650" cy="108" r="8"/><text class="lbl" x="650" y="86" text-anchor="middle">APR</text></g>
  <g data-part="month" opacity=".38"><circle class="fr3" cx="720" cy="108" r="8"/><text class="lbl" x="720" y="86" text-anchor="middle">MAY</text></g>

  <g data-part="bot">
    <rect class="fr" x="-22" y="-30" width="44" height="24" rx="4"/>
    <circle class="fr3" cx="-12" cy="-4" r="8"/><circle class="fr3" cx="12" cy="-4" r="8"/>
    <circle class="acf" cx="16" cy="-20" r="4"/>
  </g>

  <text class="lbl" x="40" y="30">NOW</text>
  <text data-part="now" class="lbl-ac" x="40" y="54" font-size="20">AUG</text>
</svg>
"""


# --------------------------------------------------------------------------
# 12. BULLETIN — diagnostic panel
# --------------------------------------------------------------------------
STATUS = """
<svg class="rig-svg" viewBox="0 0 620 240" role="img"
     aria-label="A diagnostic panel reporting the status of each team this week.">
  <rect class="fr3" x="16" y="14" width="588" height="212" rx="6" opacity=".4"/>
  <text class="lbl" x="34" y="40">SYSTEM CHECK &mdash; WEEK 03</text>
  <text data-part="pct" class="lbl-ac" x="586" y="40" text-anchor="end">0%</text>
  <rect data-part="scan" x="24" y="28" width="572" height="2" fill="var(--ac)" opacity=".35"/>

  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="58" width="9" height="9"/>
    <text class="lbl" x="56" y="67">FRC 991 &mdash; DRIVE PRACTICE SCHEDULED</text></g>
  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="86" width="9" height="9"/>
    <text class="lbl" x="56" y="95">FTC 201 / 202 &mdash; DESIGN REVIEW THURSDAY</text></g>
  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="114" width="9" height="9"/>
    <text class="lbl" x="56" y="123">FTC 23737 / 26983 &mdash; NOTEBOOK DUE FRIDAY</text></g>
  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="142" width="9" height="9"/>
    <text class="lbl" x="56" y="151">FTC 30596 &mdash; TOOL TRAINING IN PROGRESS</text></g>
  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="170" width="9" height="9"/>
    <text class="lbl" x="56" y="179">FLL MENTORING &mdash; VOLUNTEERS NEEDED</text></g>
  <g data-part="srow" opacity=".3"><rect class="acf" x="34" y="198" width="9" height="9"/>
    <text class="lbl" x="56" y="207">SHOP &mdash; SAFETY GLASSES, EVERY TIME</text></g>
</svg>
"""


# --------------------------------------------------------------------------
# 13. DOCUMENTS — inspection checklist
# --------------------------------------------------------------------------
CHECKLIST = """
<svg class="rig-svg" viewBox="0 0 560 260" role="img"
     aria-label="A robot inspection checklist ticking itself off item by item.">
  <rect class="fr3" x="14" y="12" width="532" height="232" rx="6" opacity=".4"/>
  <text class="lbl" x="32" y="40">ROBOT INSPECTION</text>
  <text data-part="count" class="lbl-ac" x="528" y="40" text-anchor="end">0/6</text>

  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="56" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 66 L42 72 L52 58"/>
    <text class="lbl" x="66" y="71">SIZE &mdash; FITS 18&Prime; CUBE</text></g>
  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="86" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 96 L42 102 L52 88"/>
    <text class="lbl" x="66" y="101">BATTERY SECURED</text></g>
  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="116" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 126 L42 132 L52 118"/>
    <text class="lbl" x="66" y="131">NO EXPOSED WIRING</text></g>
  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="146" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 156 L42 162 L52 148"/>
    <text class="lbl" x="66" y="161">TEAM NUMBER VISIBLE</text></g>
  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="176" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 186 L42 192 L52 178"/>
    <text class="lbl" x="66" y="191">SOFTWARE VERSION CURRENT</text></g>
  <g data-part="crow" opacity=".45"><rect class="fr2" x="32" y="206" width="20" height="20" rx="3"/>
    <path data-part="tick" class="wire-ac" d="M36 216 L42 222 L52 208"/>
    <text class="lbl" x="66" y="221">ENGINEERING NOTEBOOK PRESENT</text></g>

  <text data-part="passed" class="lbl-ac" x="528" y="230" text-anchor="end" font-size="17" opacity="0">PASSED</text>
</svg>
"""


# --------------------------------------------------------------------------
# 14. LINKS — PCB traces
# --------------------------------------------------------------------------
TRACES = """
<svg class="rig-svg" viewBox="0 0 620 220" role="img"
     aria-label="Circuit board traces lighting up as they connect to each resource.">
  <rect class="fr3" x="252" y="80" width="110" height="60" rx="4"/>
  <text class="lbl" x="307" y="116" text-anchor="middle">BRONCOBOTS</text>
  __PCBHOLES__

  <path data-part="trace" class="wire-ac" d="M252 96 L180 96 L180 36 L96 36"/>
  <path data-part="trace" class="wire-ac" d="M252 124 L180 124 L180 184 L96 184"/>
  <path data-part="trace" class="wire-ac" d="M362 96 L434 96 L434 36 L524 36"/>
  <path data-part="trace" class="wire-ac" d="M362 124 L434 124 L434 184 L524 184"/>

  <g data-part="pad"><rect class="fr2" x="26" y="20" width="70" height="32" rx="3"/>
    <text class="lbl" x="61" y="41" text-anchor="middle">FIRST</text></g>
  <g data-part="pad"><rect class="fr2" x="26" y="168" width="70" height="32" rx="3"/>
    <text class="lbl" x="61" y="189" text-anchor="middle">TOOLS</text></g>
  <g data-part="pad"><rect class="fr2" x="524" y="20" width="70" height="32" rx="3"/>
    <text class="lbl" x="559" y="41" text-anchor="middle">VENDORS</text></g>
  <g data-part="pad"><rect class="fr2" x="524" y="168" width="70" height="32" rx="3"/>
    <text class="lbl" x="559" y="189" text-anchor="middle">BROPHY</text></g>
</svg>
""".replace("__PCBHOLES__", holes(268, 152, 5, 20, 3.4))


# --------------------------------------------------------------------------
# 15. 404 — a wheel comes off
# --------------------------------------------------------------------------
WHEELOFF = """
<svg class="rig-svg" viewBox="0 0 520 260" role="img" aria-label="A robot that has lost a wheel.">
  <line class="floor" x1="20" y1="222" x2="500" y2="222"/>
  <g data-part="bot">
    <rect class="fr" x="96" y="150" width="150" height="60" rx="5"/>
    __404HOLES__
    <rect class="fr2" x="126" y="118" width="52" height="34" rx="4"/>
    <circle class="fr3" cx="132" cy="212" r="18"/>
    <circle class="acf" cx="132" cy="212" r="5"/>
    <text class="lbl" x="212" y="186" text-anchor="middle">404</text>
  </g>
  <g data-part="spark" opacity="0">
    <path class="wire-ac" d="M228 214 L240 202 M228 214 L244 218 M228 214 L236 228"/>
  </g>
  <g transform="translate(224,212)"><g data-part="wheel">__404WHEEL__</g></g>
</svg>
""".replace("__404HOLES__", holes(116, 180, 7, 18, 4.4)).replace(
    "__404WHEEL__", wheel(0, 0, 18))


# --------------------------------------------------------------------------
# 16. JOIN — pick a subteam, see what you would own
# --------------------------------------------------------------------------
BUILDER = """
<svg class="rig-svg" viewBox="0 0 640 400" role="img"
     aria-label="An exploded robot diagram. Selecting a subteam highlights the part of the robot it owns.">
  <line class="floor" x1="40" y1="352" x2="600" y2="352"/>

  <g data-module="mech">
    <rect class="fr" x="196" y="256" width="248" height="76" rx="6"/>
    " + holes(216, 294, 11, 20, 5) + "
    " + wheel(240, 332, 22) + wheel(320, 332, 22) + wheel(400, 332, 22) + "
    <text class="lbl" x="320" y="300" text-anchor="middle">CHASSIS &amp; DRIVETRAIN</text>
  </g>

  <g data-module="mech">
    <rect class="fr2" x="292" y="150" width="26" height="112" rx="4"/>
    <rect class="fr2" x="284" y="128" width="90" height="26" rx="4"/>
  </g>

  <g data-module="elec">
    <rect class="fr3" x="212" y="196" width="86" height="52" rx="4"/>
    <text class="lbl" x="255" y="226" text-anchor="middle">PDP</text>
    <path class="wire-ac" d="M298 210 L360 210 M298 232 L340 232 L340 264"/>
    <rect class="ac" x="360" y="196" width="46" height="28" rx="3"/>
    <text class="lbl" x="383" y="216" text-anchor="middle" fill="#fff">12V</text>
  </g>

  <g data-module="soft">
    <rect class="fr3" x="424" y="150" width="132" height="80" rx="5"/>
    <text class="lbl" x="490" y="176" text-anchor="middle">CONTROL HUB</text>
    <path class="wire-ac" d="M440 194 L472 194 M440 210 L500 210"/>
    <circle class="acf" cx="432" cy="194" r="4"/><circle class="acf" cx="432" cy="210" r="4"/>
    <path class="dim" d="M424 190 L406 190 L406 210 L424 210" stroke="var(--ac)"/>
  </g>

  <g data-module="strat">
    <rect class="fr2" x="60" y="120" width="120" height="96" rx="5"/>
    <text class="lbl" x="120" y="146" text-anchor="middle">SCOUTING</text>
    <path class="wire" d="M76 164 L164 164 M76 182 L164 182 M76 200 L128 200"/>
  </g>

  <g data-module="biz">
    <rect class="fr2" x="60" y="252" width="120" height="80" rx="5"/>
    <text class="lbl" x="120" y="278" text-anchor="middle">NOTEBOOK</text>
    <path class="wire" d="M76 296 L164 296 M76 312 L140 312"/>
  </g>

  <g data-module="drive">
    <g transform="translate(506,268)">
      <circle class="fr2" cx="0" cy="-24" r="15"/>
      <path class="fr2" d="M-18 34 Q 0 6 18 34 Z"/>
      <rect class="ac" x="-19" y="10" width="38" height="14" rx="3"/>
      <text class="lbl" x="0" y="58" text-anchor="middle">DRIVE TEAM</text>
    </g>
  </g>
</svg>
"""

RIGS = {
    "shooter": SHOOTER,
    "scale": SCALE,
    "lift": LIFT,
    "cube": CUBE,
    "mission": MISSION,
    "gears": GEARS,
    "signal": SIGNAL,
    "board": BOARD,
    "matchclock": MATCHCLOCK,
    "power": POWER,
    "track": TRACK,
    "status": STATUS,
    "checklist": CHECKLIST,
    "traces": TRACES,
    "wheeloff": WHEELOFF,
    "builder": BUILDER,
}
