# coding=utf-8
import ssl, socket
import signal
import sys
import traceback
import tempfile
import os

pem=r"""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDDKMX+j2A1VT1o
9CnqvRScQmnNBgmcQnotT8UID8yYULUfVMontx1m4rTvHEObPWKVQr6jQu7uzeNM
dqR7IjPovFQgF2ofMeMCbe4ZfiK8tmeAbW/vROkopU4Nsx1N3UzICh96dwu2CREF
Aor86vEfy06YNZgyS/Ehkx81lWYCH2TvmRxhgKIta3VcZzlBkQ+80lurgo8yeAMy
so8WVbPGs2El7FQhZBX1EuOb8vcfGh7Y+mxU4D79O0kV1vR8ewr7bzqWzfiRoB2d
Xoaw5zscHC0b3NdsXzoJO7UQUiCa8TKy31qoIe7S5u/yJsdttfK+/r0EYAl04Chm
avk1wc0FAgMBAAECggEActc6c4qhPaEUSv9q7yQmzbDTG3+TBi2kQaewNQc/CN5t
RquZbfd2SMXdXNtP+TkNGvI0xlOr0EC9oZArR/4fd7Pi+SNuIj8z64kO1FeCT3Qy
wcMkXDM71Nw5axxcgSZZeVljnqgQ7yS0rDML4LrL+z6i2DSpg+dmVLCDa/+nEFWr
OoXJu69rNgBrG/CzBMhi/1YqXsFxBANrU7GwOFLSvsPP3YetpwERdyQUF5iVZb4e
4ALUoZPtP+FOhTcmt/D+DITqqGPd2yJd2jWbfA7+YkBoSRAABqXQsRvzOR6J/Mhq
mrkTWdAPKPedYd2RUlXlufBmCK7YQLDbqfAUvvMm3QKBgQDxEN4MiChkkDjCyN+j
xiDhlh99mC8YXGAsn6BGVWqQEYk6ayP7OwyAgGb+n/YR/mIBTwtsOepMfT7Zy2R+
Cq2F4z+yci/rhK/GbEilVm2r2kHXsPfvnNvLMWoR5p7/fT1hTDZC516egeBWSzgw
aCaoU6qhVjqcmzgMCtr/ww/GAwKBgQDPP9wjWUYjn3iCm0+QnPwUos+c0rR4CprF
9xF8+czsFTA24MF9JWm5BYMbsQFsGwv6Q0kpfBszoMgM7F+fwn3KCp4WwvJoKLfN
uamHJK0YX4NzOD5Eggpq2O4KLgXR67wDdVU7jaBpGmicLZLjrfzmOWVGSIfBpiF0
JE7lafXWVwKBgBXjwTYEGx7elbjiQqR9djjlx+BAtG4S3UzQBd69HNsOLJbYacED
YKQ+hJu0bMS/g6i4w8HFFIhziwR92pczYwRYWU1b3wwU1V1AMeyJh5XmULpEQI9K
gA7YYthTR7bNaYhvQjIbDlV4V6WeWPDUVEZOqpzR1qqn0ZQOXEqDLOh/AoGAVdNY
UrsxtKbhvRScSoL4UYNq/sKzQdMCbWD3uQ2ps0rDALbq6eyIb7q8pMcUk7RPrYAX
2Dow+ZxnvBJXN03P0c+70ClDQac7FtMARZsGo8VKJnjwMGa58a2MRmLwvhIldjks
5tCr0VrCX4rv/aGbzauPKR/4OFWYHQS8N3099VkCgYAF9YKLV1YiKt4KxWVrA5rq
gZtbPOdueaDOHMR7SzD08QwOzM7ystNUm8PFm6ttv2rd81gui2bFIBxDhuxs23yn
LqIHYV8YJTsbgfrn5ZFbxwlwT9aAdJaRsFhQ/W1NtLPqcOFj8Rkq+fqsz4xuId79
8cNIEVB2P+meBLgnJZhdlA==
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUKe3RLo0Nbo3sBGOG/cw5B6g3vW0wDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yMTAzMDEyMDI0MzhaFw0yMjAz
MDEyMDI0MzhaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQDDKMX+j2A1VT1o9CnqvRScQmnNBgmcQnotT8UID8yY
ULUfVMontx1m4rTvHEObPWKVQr6jQu7uzeNMdqR7IjPovFQgF2ofMeMCbe4ZfiK8
tmeAbW/vROkopU4Nsx1N3UzICh96dwu2CREFAor86vEfy06YNZgyS/Ehkx81lWYC
H2TvmRxhgKIta3VcZzlBkQ+80lurgo8yeAMyso8WVbPGs2El7FQhZBX1EuOb8vcf
Gh7Y+mxU4D79O0kV1vR8ewr7bzqWzfiRoB2dXoaw5zscHC0b3NdsXzoJO7UQUiCa
8TKy31qoIe7S5u/yJsdttfK+/r0EYAl04Chmavk1wc0FAgMBAAGjUzBRMB0GA1Ud
DgQWBBSZwLJIQXqHULrDbqE6+jNfEaaFpTAfBgNVHSMEGDAWgBSZwLJIQXqHULrD
bqE6+jNfEaaFpTAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQB5
B0pm6IYPym5J+FqmKaVQ164UhiZ90dASOZveXgER4bg3y48aB2d2/hc4FSymrGI4
X+DJ8YrNRrq0oaETV2DLNqUmkMkRG2MVHww0FJWarHx/Ji5gJkv0f6u9f0inUnFW
7vHlcb0sJrle8OFRtPJSu6QI59u+RqAcQr3ZEy56EIrYu/teO5r2n3aWQIQCtc1+
17Qhf41K74kTmyhiM1esckbMBb5Z91sD6CZLdHMScTlXNfeOd0z3Htb64181nqXe
/rW7yEvhEZyWjNP2Qw+EQg9jjaZnMrwG/PTCvjU/rsgfyD0BjL6fgmiKbK9oQ4ib
hzrgde7L+kHuIbiwiipw
-----END CERTIFICATE-----
"""
hopper=r"""<!DOCTYPE>
<html>
<head>
<title>Sky Hopper - Web Application for Sky Navigation</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
</head>
<style>
body { font-size: 5mm ; color:red ; font-family: sans; background-color:black }
a:link {color: red;}
a:visited { color: red; }
a:active { color:red; }
a:hover { color:red; }
button { height:10mm; font-size:5mm ; text-align:center; vertical-align: middle; background-color:black; color:red; border: 2px solid red }
.comp_but, .incdec_but { width: 10mm ; height:10mm; font-size:5mm ; padding: 0 }
.comp_but { float:right }
.only_tiny { display : none }
.only_full { display : inline }
input[type=text], input[type=text]:focus {
	border: 1px solid red;
	color:red;
	background:black;

}
</style>
<body>
<canvas style="position:absolute; left:0; top:0; z-index:-1"  id="myCanvas" width="640" height="480"> </canvas>
<div class="only_full">
<p>
		<button class="incdec_but" onclick="incFOV();">-</button>
		<button class="incdec_but" onclick="decFOV();">+</button>
		&angle;<span id="fov_val">60&deg;</span><span style="font-size:16px" id="rtime"></span>
		<span style="float:right">
			<button class="comp_but" style="color: transparent; text-shadow: 0 0 0 red;" onclick="showConfig('inline');">&#x2699;</button>
		</span>
</p>
<p>
		<button class="incdec_but" onclick="decMAG();">-</button>
		<button class="incdec_but" onclick="incMAG();">+</button>
		<i>m&leq;</i><span id="mag_val">4</span>
		<span style="float:right">
			<button class="incdec_but" onclick="resetAll();">&#x21bb;</button>
		</span>
</p>
</div>
<p>
	<span class="only_full"><button class="ui_but" onclick="align();">Align</button></span>
	<span class="only_tiny"><button class="incdec_but" onclick="align();">&#x25ce;</button></span>
	<span class="only_full" id="alignment"></span> <span id="countdown"></span>
	<button class="comp_but" id="nocompass_button" style="display:none"><strike>&#x238b;</strike></button>
	<button class="comp_but" id="hand_button" style="display:none; color: transparent; text-shadow: 0 0 0 red;" onclick="manualMode();">&#x270B;</button>
	<button class="comp_but" id="compass_button" style="display:none" onclick="compassMode();">&#x238b;</button>
</p>
<p class="only_tiny"><button class="comp_but" style="color: transparent; text-shadow: 0 0 0 red;" onclick="showConfig('inline');">&#x2699;</button>
</p>

<p id="gps">No Geolocation</p>
<div id="object_log" style="display:none">
<p>Sirius:<span id="Sirius_alt"></span>, <span id="Sirius_az"></span></p>
<p>Mars:<span id="Mars_alt"></span>, <span id="Mars_az"></span></p>
<p>Rigel:<span id="Rigel_alt"></span>, <span id="Rigel_az"></span></p>
<p>Jupiter:<span id="Jupiter_alt"></span>, <span id="Jupiter_az"></span></p>
</div>
<p id="orient"></p>
<p id="status"></p>
<div class="config_div" id="allow_orientation" style="display:none; position:absolute; left:10%; top:10%; z-index:3 ; padding: 1% 1% 1% 1%; width: 78%; background:black; border: 1px solid red ; text-align:center ">
<button class="ui_but" style="height:30mm" onclick="iOSOrientation();">Enable Device Orientation</button>
</div>
<div class="config_div" id="config" style="display:none; position:absolute; left:5%; top:5%; z-index:2 ; padding: 1% 1% 1% 1%; width: 88%; background:black; border: 1px solid red ">
<span style="position:absolute; right:1mm; top:1mm">
<button class="incdec_but" onclick="showManual(true)">?</button>
<button class="incdec_but" onclick="showConfig('none');">X</button>
</span>
<p><b>Settings (0.0.28)</b></p>
<p><input class="dso_selector" id="small_screen" type="checkbox" onchange="smallScreen(this.checked)" /><label for="small_screen" >Small Screen Mode</label></p>
<p class="only_tiny">
<button class="incdec_but" onclick="resetAll();">&#x21bb;</button>
 &angle;<button class="incdec_but" onclick="incFOV();">-</button><button class="incdec_but" onclick="decFOV();">+</button>
 &#x2605;<button class="incdec_but" onclick="decMAG();">-</button><button class="incdec_but" onclick="incMAG();">+</button>
</p>
<p>&#x2315; <input type="text" oninput="findTargetByName(this.value)" onfocus="findTargetByName(this.value)" style="width:30%" /> <b><span style="float:right" id="find_status"><span></b></p>
<p><input class="dso_selector" id="NM_checked" type="checkbox" onchange="switchNightMode(this.checked)" /><label for="NM_checked" >Night Mode</label></p>
<p><input class="dso_selector" id="FS_checked" type="checkbox" onchange="toggleFS(this.checked)"        /><label for="FS_checked" >Full Screen</label></p>
<p>
DSO Magnitude &leq;<span id="dso_level_val">5</span><br/>
<input style="width:100%" type="range" id="dso_level" name="dso_level" min="3" max="16" value="5" step="1" onchange="setDSOMag(this.value)" />
</p>
<p><input class="dso_selector" id="P_checked"  type="checkbox" checked="checked" onchange="global_show_obj.P  = this.checked;" /><label for="P_checked" >Planets</label></p>
<p><input class="dso_selector" id="Oc_checked" type="checkbox" checked="checked" onchange="global_show_obj.Oc = this.checked;" /><label for="Oc_checked">Clusters and Clouds</label></p>
<p><input class="dso_selector" id="Gc_checked" type="checkbox" checked="checked" onchange="global_show_obj.Gc = this.checked;" /><label for="Gc_checked">Globular Clusters</label></p>
<p><input class="dso_selector" id="Ga_checked" type="checkbox" checked="checked" onchange="global_show_obj.Ga = this.checked;" /><label for="Ga_checked">Galaxies</label></p>
<p><input class="dso_selector" id="Ne_checked" type="checkbox" checked="checked" onchange="global_show_obj.Ne = this.checked;" /><label for="Ne_checked">Nebulae</label></p>
<p><input class="dso_selector" id="Ca_checked" type="checkbox" checked="checked" onchange="global_show_obj.Ca = this.checked;" /><label for="Ca_checked">Constellations</label></p>
<hr>
<p><button class="incdec_but" onclick="requestGeolocation();">&#x21bb;</button> GPS: <span id="lat">Unknown</span>, <span id="lon">Unknown</span></p>
<p>&#x03B1;=<span id="ang_a"></span> &#x03B2;=<span id="ang_b"></span> &#x03B3;=<span id="ang_g"></span> C=<span id="ang_c"></span></p>
</div>

<div style="position:absolute; left:0; top:0; z-index:5; width:100%; background:black; display:none;" id="manual">
<span style="float:right; margin-right: 2mm; margin-top:2mm">
<button class="incdec_but" onclick="showManual(false);">X</button>
</span>
<h1 id="skyhopper">SkyHopper</h1>
<div class="toc">
<ul>
<li><a href="#skyhopper">SkyHopper</a><ul>
<li><a href="#operation">Operation</a></li>
<li><a href="#notes-for-ios-users">Notes for iOS Users</a></li>
<li><a href="#troubleshooting">Troubleshooting</a></li>
<li><a href="#controls">Controls</a></li>
<li><a href="#constrols-in-small-screen-mode">Constrols in Small Screen Mode</a></li>
<li><a href="#equatorial-mount-users">Equatorial Mount Users</a></li>
<li><a href="#road-map">Road Map</a></li>
<li><a href="#known-issues">Known Issues</a></li>
<li><a href="#serving-skyhopper-of-remote-location">Serving SkyHopper of remote location</a></li>
<li><a href="#notes">Notes</a></li>
</ul>
</li>
</ul>
</div>
<p><a href="https://artyom-beilis.github.io/skyhopper.html">SkyHopper</a> is a web application that helps
to find objects across the night sky by hopping from a well know and easily identifiable 
star to other fainter stars or DSO by measuring changes in angles of the cell phone
using built in gyroscope and gravity sensors. It is similar to Digital Setting Circles 
implemented in a smart phone.</p>
<p>The smart phone has to have gyro, gravity sensors and preferably compass.</p>
<p>It is a web based application that contains a single HTML page and JavaScript objects 
database that will continue working even offline as long as it is cached by a browser.</p>
<h2 id="operation">Operation</h2>
<p>You attach the cellphone to the telescope such that the physical <strong>top</strong> part of the phone 
points towards viewing direction. Note it is different from typical sky observing apps
that simulate camera view of the sky. For this application the screen is parallel to the
viewing direction.</p>
<p>Before you attach the smartphone, open the application and calibrate the compass using "8" like movements. The calibration will significantly improve compass direction accuracy.</p>
<ol>
<li>Align your telescope with an easily identifiable star near the object you want to observe</li>
<li>Click <code>Align</code> button on</li>
<li>Click the star you selected. 3s timer is started to make sure there is no shaping. After 3 seconds the application is aligned on the selected star. "Aligned" message is shown and a cross that represents the direction your telescope is looking to is shown in the center of the screen.</li>
<li>Click on an object you want to observe and you get a line showing a direction you need to move the telescope to and the changes in altitude and azimuth are shown at the right and bottom part of the screen</li>
<li>Move the telescope till these numbers are close to zero - at this point your telescope should point to the requested object</li>
<li>In order to move to next object - repeat the alignment process from the step 1 since the builtin cellphone gyros don't keep the accuracy for a long time/multiple movements</li>
</ol>
<p>Here you can find a demonstration video: <a href="https://youtu.be/3VXCSMidhe0">https://youtu.be/3VXCSMidhe0</a></p>
<h2 id="notes-for-ios-users">Notes for iOS Users</h2>
<ul>
<li>For iOS 13.0 and above you need to allow access to device orientation information by pressing <code>Enable Device Orientation</code> button once application loads</li>
<li>For iOS 12.2 and before 13 you need to allow access via: <em>Settings &gt; Safari &gt; Motion and Orientation access</em></li>
</ul>
<h2 id="troubleshooting">Troubleshooting</h2>
<ul>
<li>
<p><em>The sky in application look different from what I expect?</em></p>
<p>Make sure your browser provided location information. If it is not "No Geolocation" message will be shown. Check the geographica coordinates in settings menu to make sure they match your location</p>
</li>
<li>
<p><em>I move the phone but nothing moves?</em></p>
<p>Make sure your cellphone has working sensors. Does SkyMap like applications work for you?</p>
</li>
<li>
<p><em>I move the application but only Altitude is changing. Azimuth is poining to Polaris/North?</em></p>
<p>Your browser may not support compass heading (for example Firefox) or you don't have such a sensor in the phone.
You can adjust azimuth manually by swipping the screen till you get required azimuth and then align.</p>
</li>
<li>
<p><em>I pointed my telescope to a star but the cell phone seems to point to a different direction?</em></p>
<p>The compass of the cell phone may be significantly misaligned you may to do following:</p>
<ol>
<li>Move your cell phone in compass calibration/waving pattern to increase compass accuracy</li>
<li>Increase application's field of view by pressing <code>+</code> at the top left corner near value <code>∠60°</code> - default FOV.</li>
<li>You may switch to manual azimuth mode by pressing <code>✋</code> icon at the right side and adjust the azimuth manually</li>
</ol>
</li>
<li>
<p><em>The screen becomes dim very fast and I don't have time to align/point the telescope?</em></p>
<p>Modify the "sleeping" settings for the cell phone. It is under "Settings -&gt; Display" in Android</p>
</li>
<li>
<p><em>I start moving the telescope to modify azimuth direction but according to the application it stopped moving, or going back - behaves strangly?</em></p>
<p>It seems that gyro lost accuracy. It happens. Try again. If it still happens all the time and you can't reach the target. Try one of following:</p>
<ol>
<li>Select a start that is closer on its azimuth to target object - altitude has much more accurate tracking.</li>
<li>Correct altitude first and than search for the object on azimuth axis </li>
</ol>
</li>
</ul>
<h2 id="controls">Controls</h2>
<ul>
<li>
<p>Left side, from top to bottom:</p>
<ul>
<li>Field of view - modify with <code>+</code>, <code>-</code> to adjust </li>
<li>Maximal star magnitude to display/align on - adjust with <code>+</code>, <code>-</code> controls</li>
<li>Align button and status - pressing on it starts alignment process - you need to select a star you aligning on to.</li>
</ul>
</li>
<li>
<p>Right side, from top to bottom</p>
<ul>
<li><code>⚙</code> - settings button</li>
<li><code>↻</code> button - reset alignment</li>
<li><code>✋</code> - switch to manual mode,  <code>⎋</code> switch to compass mode, <del><code>⎋</code></del> - no compass available use manual mode only</li>
</ul>
</li>
<li>
<p>Settings Menu:</p>
<ul>
<li>Small Screen Mode - optimize for small screen, move some controls to settings menu</li>
<li>Search target by name field</li>
<li>Night Mode - enable or disable red-night mode screen</li>
<li>Full Screen - switch application to full screen</li>
<li>Maximal apparent magnitude of DSO objects to be displayed</li>
<li>Filtering of the Astronomical objects by type </li>
<li>Status of geolocation and reload geolocation buttom</li>
<li>Sensors information</li>
</ul>
</li>
</ul>
<h2 id="constrols-in-small-screen-mode">Constrols in Small Screen Mode</h2>
<p>On screen controls:</p>
<ul>
<li>Left Top: <code>◎</code> - Align button</li>
<li>
<p>Right:</p>
<ul>
<li>Manual <code>✋</code> or Compass <code>⎋</code> mode</li>
<li>Settings Menu: <code>⚙</code></li>
</ul>
</li>
</ul>
<p>Extra controls in settings menu:</p>
<ul>
<li><code>↻</code> button - reset alignment</li>
<li><code>∠</code> with <code>-</code>/<code>+</code> buttons - change FOV</li>
<li><code>★</code> with <code>-</code>/<code>+</code> - modify stars magnitude</li>
</ul>
<h2 id="equatorial-mount-users">Equatorial Mount Users</h2>
<p>The application assumes you work with alt-azimuth mount. If you are using equatorial mount an additional error may be introduced due to misalignment between the cell phone major axis and the telescope axis.</p>
<p>If the targets are close to poles and significant changes in right ascension are required for the hop any misalignment error between cell phone axis and telescope axis will affect the accuracy. Final error can be calculated as 2e⋅sin(Δα/2)⋅sin(δ), where e - misalignment error between cell phone and telescope, Δα - change in right ascension required for the hop and δ - declination of the target.</p>
<p>So it may not work reliably for equatorial mounts. Alt-Az mounts are recommended.</p>
<h2 id="road-map">Road Map</h2>
<ol>
<li>Add user's object list: so user can add any object by RA, DE</li>
<li>Develop procedure for phone alignment for equatorial mounts.</li>
<li>Implement zoom-via-pinch.</li>
</ol>
<h2 id="known-issues">Known Issues</h2>
<ul>
<li>On some iPad versions (iOS 12.5) the star/target selection does not work</li>
</ul>
<h2 id="serving-skyhopper-of-remote-location">Serving SkyHopper of remote location</h2>
<p>In remote locations internet isn't always present. SkyHopper provides simple web server written in python3 to serve the SkyHopper over LAN. You can setup it on any device that can run python 3.</p>
<p>This is how you can serve it from an Android phone:</p>
<ul>
<li>Install termux</li>
<li>Install python withing termux <code>pkg install python</code></li>
<li>Download a copy of <a href="https://raw.githubusercontent.com/artyom-beilis/artyom-beilis.github.io/master/skyhopper.py">skyhopper.py</a> to a location accessible by termux</li>
<li>Create "hotspot", the typical gateway of android hotspot is <code>192.168.43.1</code></li>
<li>Open termux and <code>cd</code> to the directory you downloaded<code>skyhopper.py</code> to.</li>
<li>Run <code>python skyhopper.py</code></li>
<li>Now you can go to <a href="https://192.168.43.1:8443/">https://192.168.43.1:8443/</a> from any device connected to the hotspot and open skyhopper there. Please note <code>https</code> protocol and <code>8443</code> port</li>
<li>Note since it uses self-signed SSL sertificate you will have to give a security exception when accessing this site</li>
<li>You can close the server by simply pressing <code>Ctrl+C</code></li>
</ul>
<h2 id="notes">Notes</h2>
<p>It is experimental open source web application that would work only with well working sensors. No guarantee so. It is released under GPL license.</p></div>

<script>
//VSOP87-Multilang http://www.astrogreg.com/vsop87-multilang/index.html
//Greg Miller (gmiller@gregmiller.net) 2019.  Released as Public Domain



class vsop87a_xsmall {
   static getEarth(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.earth_x(t));
      temp.push(vsop87a_xsmall.earth_y(t));
      temp.push(vsop87a_xsmall.earth_z(t));
      return temp;
   }

   static getEmb(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.emb_x(t));
      temp.push(vsop87a_xsmall.emb_y(t));
      temp.push(vsop87a_xsmall.emb_z(t));
      return temp;
   }

   static getJupiter(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.jupiter_x(t));
      temp.push(vsop87a_xsmall.jupiter_y(t));
      temp.push(vsop87a_xsmall.jupiter_z(t));
      return temp;
   }

   static getMars(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.mars_x(t));
      temp.push(vsop87a_xsmall.mars_y(t));
      temp.push(vsop87a_xsmall.mars_z(t));
      return temp;
   }

   static getMercury(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.mercury_x(t));
      temp.push(vsop87a_xsmall.mercury_y(t));
      temp.push(vsop87a_xsmall.mercury_z(t));
      return temp;
   }

   static getNeptune(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.neptune_x(t));
      temp.push(vsop87a_xsmall.neptune_y(t));
      temp.push(vsop87a_xsmall.neptune_z(t));
      return temp;
   }

   static getSaturn(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.saturn_x(t));
      temp.push(vsop87a_xsmall.saturn_y(t));
      temp.push(vsop87a_xsmall.saturn_z(t));
      return temp;
   }

   static getUranus(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.uranus_x(t));
      temp.push(vsop87a_xsmall.uranus_y(t));
      temp.push(vsop87a_xsmall.uranus_z(t));
      return temp;
   }

   static getVenus(t){
      const temp=new Array();
      temp.push(vsop87a_xsmall.venus_x(t));
      temp.push(vsop87a_xsmall.venus_y(t));
      temp.push(vsop87a_xsmall.venus_z(t));
      return temp;
   }

   static getMoon(earth, emb){
      const temp=new Array();
      temp.push((emb[0]-earth[0])*(1 + 1 / 0.01230073677));
      temp.push((emb[1]-earth[1])*(1 + 1 / 0.01230073677));
      temp.push((emb[2]-earth[2])*(1 + 1 / 0.01230073677));
      temp[0]=temp[0]+earth[0];
      temp[1]=temp[1]+earth[1];
      temp[2]=temp[2]+earth[2];
      return temp;
   }

   static earth_x(t){
      let earth_x_0=0.0;
      earth_x_0+=     0.99982928844 * Math.cos( 1.75348568475 +     6283.07584999140*t);
      earth_x_0+=     0.00835257300 * Math.cos( 1.71034539450 +    12566.15169998280*t);
      earth_x_0+=     0.00561144206 * Math.cos( 0.00000000000 +        0.00000000000*t);
      earth_x_0+=     0.00010466628 * Math.cos( 1.66722645223 +    18849.22754997420*t);
      earth_x_0+=     0.00003110838 * Math.cos( 0.66875185215 +    83996.84731811189*t);
      earth_x_0+=     0.00002552498 * Math.cos( 0.58310207301 +      529.69096509460*t);
      earth_x_0+=     0.00002137256 * Math.cos( 1.09235189672 +     1577.34354244780*t);
      earth_x_0+=     0.00001709103 * Math.cos( 0.49540223397 +     6279.55273164240*t);
      earth_x_0+=     0.00001707882 * Math.cos( 6.15315547484 +     6286.59896834040*t);
      earth_x_0+=     0.00001445242 * Math.cos( 3.47272783760 +     2352.86615377180*t);
      earth_x_0+=     0.00001091006 * Math.cos( 3.68984782465 +     5223.69391980220*t);
      earth_x_0+=     0.00000934429 * Math.cos( 6.07389922585 +    12036.46073488820*t);
      earth_x_0+=     0.00000899144 * Math.cos( 3.17571950523 +    10213.28554621100*t);
      earth_x_0+=     0.00000566514 * Math.cos( 2.15262034016 +     1059.38193018920*t);
      earth_x_0+=     0.00000684416 * Math.cos( 1.30699021227 +     5753.38488489680*t);
      earth_x_0+=     0.00000734455 * Math.cos( 4.35500196530 +      398.14900340820*t);
      earth_x_0+=     0.00000681437 * Math.cos( 2.21821534685 +     4705.73230754360*t);
      earth_x_0+=     0.00000611238 * Math.cos( 5.38479234323 +     6812.76681508600*t);
      earth_x_0+=     0.00000451836 * Math.cos( 6.08768280868 +     5884.92684658320*t);
      earth_x_0+=     0.00000451953 * Math.cos( 1.27933728354 +     6256.77753019160*t);
      earth_x_0+=     0.00000449517 * Math.cos( 5.36923831714 +     6309.37416979120*t);
      earth_x_0+=     0.00000406248 * Math.cos( 0.54361367084 +     6681.22485339960*t);
      earth_x_0+=     0.00000540957 * Math.cos( 0.78677364655 +      775.52261132400*t);
      earth_x_0+=     0.00000547004 * Math.cos( 1.46146650376 +    14143.49524243060*t);
      earth_x_0+=     0.00000520484 * Math.cos( 4.43295799975 +     7860.41939243920*t);
      earth_x_0+=     0.00000214960 * Math.cos( 4.50213844573 +    11506.76976979360*t);
      earth_x_0+=     0.00000227892 * Math.cos( 1.23941482802 +     7058.59846131540*t);
      earth_x_0+=     0.00000225878 * Math.cos( 3.27244306207 +     4694.00295470760*t);
      earth_x_0+=     0.00000255820 * Math.cos( 2.26556277246 +    12168.00269657460*t);
      earth_x_0+=     0.00000256182 * Math.cos( 1.45474116190 +      709.93304855830*t);
      earth_x_0+=     0.00000178120 * Math.cos( 2.96205424204 +      796.29800681640*t);
      earth_x_0+=     0.00000161205 * Math.cos( 1.47337718956 +     5486.77784317500*t);
      earth_x_0+=     0.00000178325 * Math.cos( 6.24374704602 +     6283.14316029419*t);
      earth_x_0+=     0.00000178325 * Math.cos( 0.40466470869 +     6283.00853968860*t);
      earth_x_0+=     0.00000155487 * Math.cos( 1.62409309523 +    25132.30339996560*t);
      earth_x_0+=     0.00000209024 * Math.cos( 5.85207528073 +    11790.62908865880*t);
      earth_x_0+=     0.00000199971 * Math.cos( 4.07209938245 +    17789.84561978500*t);
      earth_x_0+=     0.00000128933 * Math.cos( 5.21693314150 +     7079.37385680780*t);
      earth_x_0+=     0.00000128099 * Math.cos( 4.80182882228 +     3738.76143010800*t);
      earth_x_0+=     0.00000151691 * Math.cos( 0.86921639327 +      213.29909543800*t);

      let earth_x_1=0.0;
      earth_x_1+=     0.00123403056 * Math.cos( 0.00000000000 +        0.00000000000*t);
      earth_x_1+=     0.00051500156 * Math.cos( 6.00266267204 +    12566.15169998280*t);
      earth_x_1+=     0.00001290726 * Math.cos( 5.95943124583 +    18849.22754997420*t);
      earth_x_1+=     0.00001068627 * Math.cos( 2.01554176551 +     6283.07584999140*t);
      earth_x_1+=     0.00000212689 * Math.cos( 1.73380190491 +     6279.55273164240*t);
      earth_x_1+=     0.00000212515 * Math.cos( 4.91489371033 +     6286.59896834040*t);
      earth_x_1=earth_x_1 * t;

      let earth_x_2=0.0;
      earth_x_2+=     0.00004143217 * Math.cos( 3.14159265359 +        0.00000000000*t);
      earth_x_2+=     0.00002175695 * Math.cos( 4.39999849572 +    12566.15169998280*t);
      earth_x_2+=     0.00000995233 * Math.cos( 0.20790847155 +     6283.07584999140*t);
      earth_x_2=earth_x_2 * t * t;

      let earth_x_3=0.0;
      earth_x_3+=     0.00000175213 * Math.cos( 3.14159265359 +        0.00000000000*t);
      earth_x_3=earth_x_3 * t * t * t;

      return earth_x_0+earth_x_1+earth_x_2+earth_x_3;
   }

   static earth_y(t){
      let earth_y_0=0.0;
      earth_y_0+=     0.99989211030 * Math.cos( 0.18265890456 +     6283.07584999140*t);
      earth_y_0+=     0.02442699036 * Math.cos( 3.14159265359 +        0.00000000000*t);
      earth_y_0+=     0.00835292314 * Math.cos( 0.13952878991 +    12566.15169998280*t);
      earth_y_0+=     0.00010466965 * Math.cos( 0.09641690558 +    18849.22754997420*t);
      earth_y_0+=     0.00003110838 * Math.cos( 5.38114091484 +    83996.84731811189*t);
      earth_y_0+=     0.00002570338 * Math.cos( 5.30103973360 +      529.69096509460*t);
      earth_y_0+=     0.00002147473 * Math.cos( 2.66253538905 +     1577.34354244780*t);
      earth_y_0+=     0.00001709219 * Math.cos( 5.20780401071 +     6279.55273164240*t);
      earth_y_0+=     0.00001707987 * Math.cos( 4.58232858766 +     6286.59896834040*t);
      earth_y_0+=     0.00001440265 * Math.cos( 1.90068164664 +     2352.86615377180*t);
      earth_y_0+=     0.00001135092 * Math.cos( 5.27313415220 +     5223.69391980220*t);
      earth_y_0+=     0.00000934539 * Math.cos( 4.50301201844 +    12036.46073488820*t);
      earth_y_0+=     0.00000900565 * Math.cos( 1.60563288120 +    10213.28554621100*t);
      earth_y_0+=     0.00000567126 * Math.cos( 0.58142248753 +     1059.38193018920*t);
      earth_y_0+=     0.00000744932 * Math.cos( 2.80728871886 +      398.14900340820*t);
      earth_y_0+=     0.00000639316 * Math.cos( 6.02923915017 +     5753.38488489680*t);
      earth_y_0+=     0.00000681324 * Math.cos( 0.64729627497 +     4705.73230754360*t);
      earth_y_0+=     0.00000611347 * Math.cos( 3.81381495286 +     6812.76681508600*t);
      earth_y_0+=     0.00000450435 * Math.cos( 4.52785572489 +     5884.92684658320*t);
      earth_y_0+=     0.00000452018 * Math.cos( 5.99167242707 +     6256.77753019160*t);
      earth_y_0+=     0.00000449968 * Math.cos( 3.79880375595 +     6309.37416979120*t);
      earth_y_0+=     0.00000551390 * Math.cos( 3.96125249369 +     5507.55323866740*t);
      earth_y_0+=     0.00000406334 * Math.cos( 5.25616268027 +     6681.22485339960*t);
      earth_y_0+=     0.00000541273 * Math.cos( 5.49902805917 +      775.52261132400*t);
      earth_y_0+=     0.00000546360 * Math.cos( 6.17311131785 +    14143.49524243060*t);
      earth_y_0+=     0.00000507084 * Math.cos( 2.87025193381 +     7860.41939243920*t);
      earth_y_0+=     0.00000219504 * Math.cos( 2.95216139568 +    11506.76976979360*t);
      earth_y_0+=     0.00000227937 * Math.cos( 5.95179248814 +     7058.59846131540*t);
      earth_y_0+=     0.00000227792 * Math.cos( 4.84547074733 +     4694.00295470760*t);
      earth_y_0+=     0.00000255845 * Math.cos( 0.69454231563 +    12168.00269657460*t);
      earth_y_0+=     0.00000256132 * Math.cos( 6.16722512388 +      709.93304855830*t);
      earth_y_0+=     0.00000179242 * Math.cos( 1.40003446021 +      796.29800681640*t);
      earth_y_0+=     0.00000178280 * Math.cos( 5.11717552231 +     6283.00853968860*t);
      earth_y_0+=     0.00000178280 * Math.cos( 4.67307255246 +     6283.14316029419*t);
      earth_y_0+=     0.00000155454 * Math.cos( 0.05340525434 +    25132.30339996560*t);
      earth_y_0+=     0.00000206257 * Math.cos( 4.28366728882 +    11790.62908865880*t);
      earth_y_0+=     0.00000149769 * Math.cos( 6.07429023278 +     5486.77784317500*t);
      earth_y_0+=     0.00000200005 * Math.cos( 2.50144088120 +    17789.84561978500*t);
      earth_y_0+=     0.00000129006 * Math.cos( 3.64623708634 +     7079.37385680780*t);
      earth_y_0+=     0.00000128211 * Math.cos( 3.23254821381 +     3738.76143010800*t);
      earth_y_0+=     0.00000152790 * Math.cos( 5.58120800450 +      213.29909543800*t);
      earth_y_0+=     0.00000118725 * Math.cos( 5.45361490488 +     9437.76293488700*t);

      let earth_y_1=0.0;
      earth_y_1+=     0.00093046324 * Math.cos( 0.00000000000 +        0.00000000000*t);
      earth_y_1+=     0.00051506609 * Math.cos( 4.43180499286 +    12566.15169998280*t);
      earth_y_1+=     0.00001290800 * Math.cos( 4.38860548540 +    18849.22754997420*t);
      earth_y_1+=     0.00000464550 * Math.cos( 5.82729912952 +     6283.07584999140*t);
      earth_y_1+=     0.00000212689 * Math.cos( 0.16300556918 +     6279.55273164240*t);
      earth_y_1+=     0.00000212533 * Math.cos( 3.34400595407 +     6286.59896834040*t);
      earth_y_1=earth_y_1 * t;

      let earth_y_2=0.0;
      earth_y_2+=     0.00005080208 * Math.cos( 0.00000000000 +        0.00000000000*t);
      earth_y_2+=     0.00002178016 * Math.cos( 2.82957544235 +    12566.15169998280*t);
      earth_y_2+=     0.00001020487 * Math.cos( 4.63746718598 +     6283.07584999140*t);
      earth_y_2=earth_y_2 * t * t;

      let earth_y_3=0.0;
      earth_y_3+=     0.00000128116 * Math.cos( 3.14159265359 +        0.00000000000*t);
      earth_y_3=earth_y_3 * t * t * t;

      return earth_y_0+earth_y_1+earth_y_2+earth_y_3;
   }

   static earth_z(t){
      let earth_z_0=0.0;
      earth_z_0+=     0.00000279620 * Math.cos( 3.19870156017 +    84334.66158130829*t);
      earth_z_0+=     0.00000101625 * Math.cos( 5.42248110597 +     5507.55323866740*t);

      let earth_z_1=0.0;
      earth_z_1+=     0.00227822442 * Math.cos( 3.41372504278 +     6283.07584999140*t);
      earth_z_1+=     0.00005429282 * Math.cos( 0.00000000000 +        0.00000000000*t);
      earth_z_1+=     0.00001903183 * Math.cos( 3.37061270964 +    12566.15169998280*t);
      earth_z_1=earth_z_1 * t;

      let earth_z_2=0.0;
      earth_z_2+=     0.00009721989 * Math.cos( 5.15233725915 +     6283.07584999140*t);
      earth_z_2+=     0.00000349501 * Math.cos( 3.14159265359 +        0.00000000000*t);
      earth_z_2=earth_z_2 * t * t;

      let earth_z_3=0.0;
      earth_z_3+=     0.00000276077 * Math.cos( 0.59413258730 +     6283.07584999140*t);
      earth_z_3=earth_z_3 * t * t * t;

      return earth_z_0+earth_z_1+earth_z_2+earth_z_3;
   }

   static emb_x(t){
      let emb_x_0=0.0;
      emb_x_0+=     0.99982927460 * Math.cos( 1.75348568475 +     6283.07584999140*t);
      emb_x_0+=     0.00835257300 * Math.cos( 1.71034539450 +    12566.15169998280*t);
      emb_x_0+=     0.00561144161 * Math.cos( 0.00000000000 +        0.00000000000*t);
      emb_x_0+=     0.00010466628 * Math.cos( 1.66722645223 +    18849.22754997420*t);
      emb_x_0+=     0.00002552498 * Math.cos( 0.58310207301 +      529.69096509460*t);
      emb_x_0+=     0.00002137256 * Math.cos( 1.09235189672 +     1577.34354244780*t);
      emb_x_0+=     0.00001709103 * Math.cos( 0.49540223397 +     6279.55273164240*t);
      emb_x_0+=     0.00001707882 * Math.cos( 6.15315547484 +     6286.59896834040*t);
      emb_x_0+=     0.00001445242 * Math.cos( 3.47272783760 +     2352.86615377180*t);
      emb_x_0+=     0.00001091006 * Math.cos( 3.68984782465 +     5223.69391980220*t);
      emb_x_0+=     0.00000934429 * Math.cos( 6.07389922585 +    12036.46073488820*t);
      emb_x_0+=     0.00000899144 * Math.cos( 3.17571950523 +    10213.28554621100*t);
      emb_x_0+=     0.00000566514 * Math.cos( 2.15262034016 +     1059.38193018920*t);
      emb_x_0+=     0.00000684416 * Math.cos( 1.30699021227 +     5753.38488489680*t);
      emb_x_0+=     0.00000734455 * Math.cos( 4.35500196530 +      398.14900340820*t);
      emb_x_0+=     0.00000681437 * Math.cos( 2.21821534685 +     4705.73230754360*t);
      emb_x_0+=     0.00000611238 * Math.cos( 5.38479234323 +     6812.76681508600*t);
      emb_x_0+=     0.00000451836 * Math.cos( 6.08768280868 +     5884.92684658320*t);
      emb_x_0+=     0.00000451953 * Math.cos( 1.27933728354 +     6256.77753019160*t);
      emb_x_0+=     0.00000449517 * Math.cos( 5.36923831714 +     6309.37416979120*t);
      emb_x_0+=     0.00000406248 * Math.cos( 0.54361367084 +     6681.22485339960*t);
      emb_x_0+=     0.00000540957 * Math.cos( 0.78677364655 +      775.52261132400*t);
      emb_x_0+=     0.00000547004 * Math.cos( 1.46146650376 +    14143.49524243060*t);
      emb_x_0+=     0.00000520484 * Math.cos( 4.43295799975 +     7860.41939243920*t);
      emb_x_0+=     0.00000214960 * Math.cos( 4.50213844573 +    11506.76976979360*t);
      emb_x_0+=     0.00000227892 * Math.cos( 1.23941482802 +     7058.59846131540*t);
      emb_x_0+=     0.00000225878 * Math.cos( 3.27244306207 +     4694.00295470760*t);
      emb_x_0+=     0.00000255820 * Math.cos( 2.26556277246 +    12168.00269657460*t);
      emb_x_0+=     0.00000178120 * Math.cos( 2.96205424204 +      796.29800681640*t);
      emb_x_0+=     0.00000161205 * Math.cos( 1.47337718956 +     5486.77784317500*t);
      emb_x_0+=     0.00000178325 * Math.cos( 6.24374704602 +     6283.14316029419*t);
      emb_x_0+=     0.00000178325 * Math.cos( 0.40466470869 +     6283.00853968860*t);
      emb_x_0+=     0.00000155487 * Math.cos( 1.62409309523 +    25132.30339996560*t);
      emb_x_0+=     0.00000209024 * Math.cos( 5.85207528073 +    11790.62908865880*t);
      emb_x_0+=     0.00000199971 * Math.cos( 4.07209938245 +    17789.84561978500*t);
      emb_x_0+=     0.00000128933 * Math.cos( 5.21693314150 +     7079.37385680780*t);
      emb_x_0+=     0.00000128099 * Math.cos( 4.80182882228 +     3738.76143010800*t);
      emb_x_0+=     0.00000151691 * Math.cos( 0.86921639327 +      213.29909543800*t);

      let emb_x_1=0.0;
      emb_x_1+=     0.00123403046 * Math.cos( 0.00000000000 +        0.00000000000*t);
      emb_x_1+=     0.00051500156 * Math.cos( 6.00266267204 +    12566.15169998280*t);
      emb_x_1+=     0.00001290726 * Math.cos( 5.95943124583 +    18849.22754997420*t);
      emb_x_1+=     0.00001068627 * Math.cos( 2.01554176551 +     6283.07584999140*t);
      emb_x_1+=     0.00000212689 * Math.cos( 1.73380190491 +     6279.55273164240*t);
      emb_x_1+=     0.00000212515 * Math.cos( 4.91489371033 +     6286.59896834040*t);
      emb_x_1=emb_x_1 * t;

      let emb_x_2=0.0;
      emb_x_2+=     0.00004143217 * Math.cos( 3.14159265359 +        0.00000000000*t);
      emb_x_2+=     0.00002175695 * Math.cos( 4.39999849572 +    12566.15169998280*t);
      emb_x_2+=     0.00000995233 * Math.cos( 0.20790847155 +     6283.07584999140*t);
      emb_x_2=emb_x_2 * t * t;

      let emb_x_3=0.0;
      emb_x_3+=     0.00000175213 * Math.cos( 3.14159265359 +        0.00000000000*t);
      emb_x_3=emb_x_3 * t * t * t;

      return emb_x_0+emb_x_1+emb_x_2+emb_x_3;
   }

   static emb_y(t){
      let emb_y_0=0.0;
      emb_y_0+=     0.99989209645 * Math.cos( 0.18265890456 +     6283.07584999140*t);
      emb_y_0+=     0.02442698841 * Math.cos( 3.14159265359 +        0.00000000000*t);
      emb_y_0+=     0.00835292314 * Math.cos( 0.13952878991 +    12566.15169998280*t);
      emb_y_0+=     0.00010466965 * Math.cos( 0.09641690558 +    18849.22754997420*t);
      emb_y_0+=     0.00002570338 * Math.cos( 5.30103973360 +      529.69096509460*t);
      emb_y_0+=     0.00002147473 * Math.cos( 2.66253538905 +     1577.34354244780*t);
      emb_y_0+=     0.00001709219 * Math.cos( 5.20780401071 +     6279.55273164240*t);
      emb_y_0+=     0.00001707987 * Math.cos( 4.58232858766 +     6286.59896834040*t);
      emb_y_0+=     0.00001440265 * Math.cos( 1.90068164664 +     2352.86615377180*t);
      emb_y_0+=     0.00001135092 * Math.cos( 5.27313415220 +     5223.69391980220*t);
      emb_y_0+=     0.00000934539 * Math.cos( 4.50301201844 +    12036.46073488820*t);
      emb_y_0+=     0.00000900565 * Math.cos( 1.60563288120 +    10213.28554621100*t);
      emb_y_0+=     0.00000567126 * Math.cos( 0.58142248753 +     1059.38193018920*t);
      emb_y_0+=     0.00000744932 * Math.cos( 2.80728871886 +      398.14900340820*t);
      emb_y_0+=     0.00000639316 * Math.cos( 6.02923915017 +     5753.38488489680*t);
      emb_y_0+=     0.00000681324 * Math.cos( 0.64729627497 +     4705.73230754360*t);
      emb_y_0+=     0.00000611347 * Math.cos( 3.81381495286 +     6812.76681508600*t);
      emb_y_0+=     0.00000450435 * Math.cos( 4.52785572489 +     5884.92684658320*t);
      emb_y_0+=     0.00000452018 * Math.cos( 5.99167242707 +     6256.77753019160*t);
      emb_y_0+=     0.00000449968 * Math.cos( 3.79880375595 +     6309.37416979120*t);
      emb_y_0+=     0.00000551390 * Math.cos( 3.96125249369 +     5507.55323866740*t);
      emb_y_0+=     0.00000406334 * Math.cos( 5.25616268027 +     6681.22485339960*t);
      emb_y_0+=     0.00000541273 * Math.cos( 5.49902805917 +      775.52261132400*t);
      emb_y_0+=     0.00000546360 * Math.cos( 6.17311131785 +    14143.49524243060*t);
      emb_y_0+=     0.00000507084 * Math.cos( 2.87025193381 +     7860.41939243920*t);
      emb_y_0+=     0.00000219504 * Math.cos( 2.95216139568 +    11506.76976979360*t);
      emb_y_0+=     0.00000227937 * Math.cos( 5.95179248814 +     7058.59846131540*t);
      emb_y_0+=     0.00000227792 * Math.cos( 4.84547074733 +     4694.00295470760*t);
      emb_y_0+=     0.00000255845 * Math.cos( 0.69454231563 +    12168.00269657460*t);
      emb_y_0+=     0.00000179242 * Math.cos( 1.40003446021 +      796.29800681640*t);
      emb_y_0+=     0.00000178280 * Math.cos( 5.11717552231 +     6283.00853968860*t);
      emb_y_0+=     0.00000178280 * Math.cos( 4.67307255246 +     6283.14316029419*t);
      emb_y_0+=     0.00000155454 * Math.cos( 0.05340525434 +    25132.30339996560*t);
      emb_y_0+=     0.00000206257 * Math.cos( 4.28366728882 +    11790.62908865880*t);
      emb_y_0+=     0.00000149769 * Math.cos( 6.07429023278 +     5486.77784317500*t);
      emb_y_0+=     0.00000200005 * Math.cos( 2.50144088120 +    17789.84561978500*t);
      emb_y_0+=     0.00000129006 * Math.cos( 3.64623708634 +     7079.37385680780*t);
      emb_y_0+=     0.00000128211 * Math.cos( 3.23254821381 +     3738.76143010800*t);
      emb_y_0+=     0.00000152790 * Math.cos( 5.58120800450 +      213.29909543800*t);
      emb_y_0+=     0.00000118725 * Math.cos( 5.45361490488 +     9437.76293488700*t);

      let emb_y_1=0.0;
      emb_y_1+=     0.00093046317 * Math.cos( 0.00000000000 +        0.00000000000*t);
      emb_y_1+=     0.00051506609 * Math.cos( 4.43180499286 +    12566.15169998280*t);
      emb_y_1+=     0.00001290800 * Math.cos( 4.38860548540 +    18849.22754997420*t);
      emb_y_1+=     0.00000464550 * Math.cos( 5.82729912952 +     6283.07584999140*t);
      emb_y_1+=     0.00000212689 * Math.cos( 0.16300556918 +     6279.55273164240*t);
      emb_y_1+=     0.00000212533 * Math.cos( 3.34400595407 +     6286.59896834040*t);
      emb_y_1=emb_y_1 * t;

      let emb_y_2=0.0;
      emb_y_2+=     0.00005080208 * Math.cos( 0.00000000000 +        0.00000000000*t);
      emb_y_2+=     0.00002178016 * Math.cos( 2.82957544235 +    12566.15169998280*t);
      emb_y_2+=     0.00001020487 * Math.cos( 4.63746718598 +     6283.07584999140*t);
      emb_y_2=emb_y_2 * t * t;

      let emb_y_3=0.0;
      emb_y_3+=     0.00000128116 * Math.cos( 3.14159265359 +        0.00000000000*t);
      emb_y_3=emb_y_3 * t * t * t;

      return emb_y_0+emb_y_1+emb_y_2+emb_y_3;
   }

   static emb_z(t){
      let emb_z_0=0.0;
      emb_z_0+=     0.00000101625 * Math.cos( 5.42248110597 +     5507.55323866740*t);

      let emb_z_1=0.0;
      emb_z_1+=     0.00227822442 * Math.cos( 3.41372504278 +     6283.07584999140*t);
      emb_z_1+=     0.00005429282 * Math.cos( 0.00000000000 +        0.00000000000*t);
      emb_z_1+=     0.00001903183 * Math.cos( 3.37061270964 +    12566.15169998280*t);
      emb_z_1=emb_z_1 * t;

      let emb_z_2=0.0;
      emb_z_2+=     0.00009721989 * Math.cos( 5.15233725915 +     6283.07584999140*t);
      emb_z_2+=     0.00000349501 * Math.cos( 3.14159265359 +        0.00000000000*t);
      emb_z_2=emb_z_2 * t * t;

      let emb_z_3=0.0;
      emb_z_3+=     0.00000276077 * Math.cos( 0.59413258730 +     6283.07584999140*t);
      emb_z_3=emb_z_3 * t * t * t;

      return emb_z_0+emb_z_1+emb_z_2+emb_z_3;
   }

   static jupiter_x(t){
      let jupiter_x_0=0.0;
      jupiter_x_0+=     5.19663470114 * Math.cos( 0.59945082355 +      529.69096509460*t);
      jupiter_x_0+=     0.36662642320 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_x_0+=     0.12593937922 * Math.cos( 0.94911583701 +     1059.38193018920*t);
      jupiter_x_0+=     0.01500672056 * Math.cos( 0.73175134610 +      522.57741809380*t);
      jupiter_x_0+=     0.01476224578 * Math.cos( 3.61736921122 +      536.80451209540*t);
      jupiter_x_0+=     0.00457752736 * Math.cos( 1.29883700755 +     1589.07289528380*t);
      jupiter_x_0+=     0.00301689798 * Math.cos( 5.17372551148 +        7.11354700080*t);
      jupiter_x_0+=     0.00385975375 * Math.cos( 2.01229910687 +      103.09277421860*t);
      jupiter_x_0+=     0.00194025405 * Math.cos( 5.02580363996 +      426.59819087600*t);
      jupiter_x_0+=     0.00150678793 * Math.cos( 6.12003027739 +      110.20632121940*t);
      jupiter_x_0+=     0.00144867641 * Math.cos( 5.55980577080 +      632.78373931320*t);
      jupiter_x_0+=     0.00134226996 * Math.cos( 0.87648567011 +      213.29909543800*t);
      jupiter_x_0+=     0.00103494641 * Math.cos( 6.19324769120 +     1052.26838318840*t);
      jupiter_x_0+=     0.00114201562 * Math.cos( 0.01567084269 +     1162.47470440780*t);
      jupiter_x_0+=     0.00072095575 * Math.cos( 3.96117430643 +     1066.49547719000*t);
      jupiter_x_0+=     0.00059486083 * Math.cos( 4.45769374358 +      949.17560896980*t);
      jupiter_x_0+=     0.00068284021 * Math.cos( 3.44051122631 +      846.08283475120*t);
      jupiter_x_0+=     0.00047092251 * Math.cos( 1.44612636451 +      419.48464387520*t);
      jupiter_x_0+=     0.00030623417 * Math.cos( 2.99132321427 +      206.18554843720*t);
      jupiter_x_0+=     0.00026613459 * Math.cos( 4.85169906494 +      323.50541665740*t);
      jupiter_x_0+=     0.00019727457 * Math.cos( 1.64891626213 +     2118.76386037840*t);
      jupiter_x_0+=     0.00016481594 * Math.cos( 1.95150056568 +      316.39186965660*t);
      jupiter_x_0+=     0.00016101974 * Math.cos( 0.87973155980 +      515.46387109300*t);
      jupiter_x_0+=     0.00014209487 * Math.cos( 2.07769621413 +      742.99006053260*t);
      jupiter_x_0+=     0.00015192516 * Math.cos( 6.25820127906 +      735.87651353180*t);
      jupiter_x_0+=     0.00011423199 * Math.cos( 3.48146108929 +      543.91805909620*t);
      jupiter_x_0+=     0.00012155285 * Math.cos( 3.75229924999 +      525.75881183150*t);
      jupiter_x_0+=     0.00011996271 * Math.cos( 0.58568573729 +      533.62311835770*t);
      jupiter_x_0+=     0.00008468556 * Math.cos( 3.47248751739 +      639.89728631400*t);
      jupiter_x_0+=     0.00008223302 * Math.cos( 5.56680447143 +     1478.86657406440*t);
      jupiter_x_0+=     0.00008694124 * Math.cos( 0.38262009411 +     1692.16566950240*t);
      jupiter_x_0+=     0.00007427517 * Math.cos( 5.98380751196 +      956.28915597060*t);
      jupiter_x_0+=     0.00007516470 * Math.cos( 0.92896448412 +     1265.56747862640*t);
      jupiter_x_0+=     0.00007655867 * Math.cos( 0.14178789086 +     1581.95934828300*t);
      jupiter_x_0+=     0.00005318791 * Math.cos( 1.10494016349 +      526.50957135690*t);
      jupiter_x_0+=     0.00005218492 * Math.cos( 3.23235129224 +      532.87235883230*t);
      jupiter_x_0+=     0.00005777311 * Math.cos( 5.03726165628 +       14.22709400160*t);
      jupiter_x_0+=     0.00004622685 * Math.cos( 3.75817086099 +     1375.77379984580*t);
      jupiter_x_0+=     0.00003939864 * Math.cos( 4.30892687511 +     1596.18644228460*t);
      jupiter_x_0+=     0.00004569444 * Math.cos( 2.15087281710 +       95.97922721780*t);
      jupiter_x_0+=     0.00002952712 * Math.cos( 3.85988483947 +      309.27832265580*t);
      jupiter_x_0+=     0.00002857935 * Math.cos( 6.01118473739 +      117.31986822020*t);
      jupiter_x_0+=     0.00002440094 * Math.cos( 4.23995765702 +      433.71173787680*t);
      jupiter_x_0+=     0.00002438257 * Math.cos( 3.88808463822 +      220.41264243880*t);
      jupiter_x_0+=     0.00002675112 * Math.cos( 3.18723449094 +     1169.58825140860*t);
      jupiter_x_0+=     0.00002386425 * Math.cos( 5.96354994324 +     1045.15483618760*t);
      jupiter_x_0+=     0.00001870097 * Math.cos( 0.52019313301 +     1155.36115740700*t);
      jupiter_x_0+=     0.00001939060 * Math.cos( 5.91883412864 +      625.67019231240*t);
      jupiter_x_0+=     0.00001631500 * Math.cos( 4.41910383466 +      942.06206196900*t);
      jupiter_x_0+=     0.00001451667 * Math.cos( 5.76112706040 +      853.19638175200*t);
      jupiter_x_0+=     0.00001361286 * Math.cos( 1.34792748837 +     1368.66025284500*t);
      jupiter_x_0+=     0.00001663331 * Math.cos( 1.94010629194 +      838.96928775040*t);
      jupiter_x_0+=     0.00001611229 * Math.cos( 5.49324974845 +       74.78159856730*t);
      jupiter_x_0+=     0.00001033570 * Math.cos( 0.08907208789 +     1795.25844372100*t);
      jupiter_x_0+=     0.00000991481 * Math.cos( 3.08609505814 +     1272.68102562720*t);
      jupiter_x_0+=     0.00000934789 * Math.cos( 3.11151341633 +      199.07200143640*t);
      jupiter_x_0+=     0.00000934504 * Math.cos( 1.99938801336 +     2648.45482547300*t);
      jupiter_x_0+=     0.00000858829 * Math.cos( 3.71316879557 +      529.64278098480*t);
      jupiter_x_0+=     0.00000858734 * Math.cos( 0.62779464690 +      529.73914920440*t);
      jupiter_x_0+=     0.00001088284 * Math.cos( 1.13406104190 +      527.24328453980*t);
      jupiter_x_0+=     0.00001080643 * Math.cos( 3.20528362573 +      532.13864564940*t);
      jupiter_x_0+=     0.00000959188 * Math.cos( 1.34789494210 +      149.56319713460*t);
      jupiter_x_0+=     0.00000840045 * Math.cos( 4.14390924077 +        3.93215326310*t);
      jupiter_x_0+=     0.00000941997 * Math.cos( 1.57612902656 +      412.37109687440*t);
      jupiter_x_0+=     0.00000932600 * Math.cos( 5.34596782982 +      380.12776796000*t);
      jupiter_x_0+=     0.00000665711 * Math.cos( 6.08446262481 +     2008.55753915900*t);
      jupiter_x_0+=     0.00000747735 * Math.cos( 4.70954561325 +      330.61896365820*t);
      jupiter_x_0+=     0.00000693311 * Math.cos( 1.33754289320 +     1063.31408345230*t);
      jupiter_x_0+=     0.00000606761 * Math.cos( 0.11410967423 +     2111.65031337760*t);
      jupiter_x_0+=     0.00000680707 * Math.cos( 0.29377240207 +      528.72775724810*t);
      jupiter_x_0+=     0.00000678819 * Math.cos( 4.04669903131 +      530.65417294110*t);
      jupiter_x_0+=     0.00000572943 * Math.cos( 0.74312663770 +     2221.85663459700*t);
      jupiter_x_0+=     0.00000564304 * Math.cos( 4.06331341841 +     1055.44977692610*t);
      jupiter_x_0+=     0.00000647982 * Math.cos( 5.12508099382 +      984.60033162190*t);
      jupiter_x_0+=     0.00000460191 * Math.cos( 3.82640277755 +     1073.60902419080*t);
      jupiter_x_0+=     0.00000537627 * Math.cos( 0.67272668191 +     1685.05212250160*t);
      jupiter_x_0+=     0.00000508303 * Math.cos( 6.24505797644 +      728.76296653100*t);
      jupiter_x_0+=     0.00000539580 * Math.cos( 5.31458333755 +       38.13303563780*t);
      jupiter_x_0+=     0.00000405304 * Math.cos( 2.98797353644 +      909.81873305460*t);
      jupiter_x_0+=     0.00000303114 * Math.cos( 4.07249746397 +     1905.46476494040*t);
      jupiter_x_0+=     0.00000413310 * Math.cos( 4.52689012732 +      454.90936652730*t);
      jupiter_x_0+=     0.00000334675 * Math.cos( 0.95326265644 +       76.26607127560*t);
      jupiter_x_0+=     0.00000389470 * Math.cos( 6.05999515231 +      604.47256366190*t);
      jupiter_x_0+=     0.00000277679 * Math.cos( 0.65883071471 +     1485.98012106520*t);
      jupiter_x_0+=     0.00000303217 * Math.cos( 5.06489637072 +      529.16970023280*t);
      jupiter_x_0+=     0.00000302826 * Math.cos( 5.56013117831 +      530.21222995640*t);
      jupiter_x_0+=     0.00000385508 * Math.cos( 4.91137191483 +        3.18139373770*t);
      jupiter_x_0+=     0.00000254458 * Math.cos( 3.58455210274 +     1062.56332392690*t);
      jupiter_x_0+=     0.00000244844 * Math.cos( 1.59298253869 +     1258.45393162560*t);
      jupiter_x_0+=     0.00000227064 * Math.cos( 4.65765215856 +     2125.87740737920*t);
      jupiter_x_0+=     0.00000304105 * Math.cos( 1.75376741282 +     6283.07584999140*t);
      jupiter_x_0+=     0.00000287288 * Math.cos( 2.95635370067 +      305.34616939270*t);
      jupiter_x_0+=     0.00000224854 * Math.cos( 3.50099765253 +     1699.27921650320*t);
      jupiter_x_0+=     0.00000206026 * Math.cos( 1.03192385893 +     1898.35121793960*t);
      jupiter_x_0+=     0.00000189685 * Math.cos( 1.04124698047 +      508.35032409220*t);
      jupiter_x_0+=     0.00000235578 * Math.cos( 0.92416895439 +     1056.20053645150*t);
      jupiter_x_0+=     0.00000210609 * Math.cos( 4.02134591862 +      490.33408917940*t);
      jupiter_x_0+=     0.00000188745 * Math.cos( 5.71463346844 +       99.16062095550*t);
      jupiter_x_0+=     0.00000179082 * Math.cos( 6.10222002951 +      526.77020378780*t);
      jupiter_x_0+=     0.00000177005 * Math.cos( 4.52323052516 +      532.61172640140*t);
      jupiter_x_0+=     0.00000164689 * Math.cos( 3.47714842774 +      528.94020556920*t);
      jupiter_x_0+=     0.00000164585 * Math.cos( 0.86380555242 +      530.44172462000*t);
      jupiter_x_0+=     0.00000192018 * Math.cos( 0.31042772808 +      569.04784100980*t);
      jupiter_x_0+=     0.00000217613 * Math.cos( 5.68326814925 +      453.42489381900*t);
      jupiter_x_0+=     0.00000154626 * Math.cos( 1.26242501430 +      519.39602435610*t);
      jupiter_x_0+=     0.00000153593 * Math.cos( 2.20032240084 +       11.04570026390*t);
      jupiter_x_0+=     0.00000208311 * Math.cos( 3.39287059113 +     1439.50969814920*t);
      jupiter_x_0+=     0.00000158046 * Math.cos( 4.32805014383 +      525.49817940060*t);
      jupiter_x_0+=     0.00000155478 * Math.cos( 0.01448243696 +      533.88375078860*t);
      jupiter_x_0+=     0.00000165564 * Math.cos( 3.66344459446 +      224.34479570190*t);
      jupiter_x_0+=     0.00000139735 * Math.cos( 3.35517923192 +      647.01083331480*t);
      jupiter_x_0+=     0.00000194856 * Math.cos( 5.30459820962 +     1021.24889455140*t);
      jupiter_x_0+=     0.00000174847 * Math.cos( 1.21550279097 +     1471.75302706360*t);
      jupiter_x_0+=     0.00000145297 * Math.cos( 4.02621175684 +      302.16477565500*t);
      jupiter_x_0+=     0.00000162930 * Math.cos( 0.49071349850 +     2001.44399215820*t);
      jupiter_x_0+=     0.00000142463 * Math.cos( 3.75545249652 +      227.52618943960*t);
      jupiter_x_0+=     0.00000144173 * Math.cos( 1.33176686779 +     1788.14489672020*t);
      jupiter_x_0+=     0.00000162873 * Math.cos( 0.56256179898 +      835.03713448730*t);
      jupiter_x_0+=     0.00000176861 * Math.cos( 3.17525918893 +    10213.28554621100*t);
      jupiter_x_0+=     0.00000120578 * Math.cos( 3.08300146416 +      539.98590583310*t);
      jupiter_x_0+=     0.00000135670 * Math.cos( 3.80012923478 +      540.73666535850*t);
      jupiter_x_0+=     0.00000153089 * Math.cos( 2.02297606024 +        1.48447270830*t);
      jupiter_x_0+=     0.00000121815 * Math.cos( 3.78870221205 +      524.06189080210*t);
      jupiter_x_0+=     0.00000120032 * Math.cos( 0.55319601436 +      535.32003938710*t);
      jupiter_x_0+=     0.00000124049 * Math.cos( 3.38834311016 +      983.11585891360*t);
      jupiter_x_0+=     0.00000123795 * Math.cos( 3.34199482893 +      525.02509864860*t);
      jupiter_x_0+=     0.00000104430 * Math.cos( 3.76551699050 +      529.53090640020*t);
      jupiter_x_0+=     0.00000104430 * Math.cos( 0.57516865787 +      529.85102378900*t);
      jupiter_x_0+=     0.00000134226 * Math.cos( 0.10239699641 +     1574.84580128220*t);
      jupiter_x_0+=     0.00000104654 * Math.cos( 3.32893024304 +      551.03160609700*t);
      jupiter_x_0+=     0.00000114344 * Math.cos( 3.33978613495 +      750.10360753340*t);
      jupiter_x_0+=     0.00000116158 * Math.cos( 0.99764796582 +      534.35683154060*t);
      jupiter_x_0+=     0.00000122805 * Math.cos( 4.90630340295 +      524.27433912320*t);
      jupiter_x_0+=     0.00000103070 * Math.cos( 4.41455753031 +      963.40270297140*t);
      jupiter_x_0+=     0.00000120897 * Math.cos( 5.71565359127 +      535.10759106600*t);
      jupiter_x_0+=     0.00000110642 * Math.cos( 0.32527165996 +     2324.94940881560*t);

      let jupiter_x_1=0.0;
      jupiter_x_1+=     0.00882389251 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_x_1+=     0.00635297172 * Math.cos( 0.10662156868 +     1059.38193018920*t);
      jupiter_x_1+=     0.00599720482 * Math.cos( 2.42996678275 +      522.57741809380*t);
      jupiter_x_1+=     0.00589157060 * Math.cos( 1.91556314637 +      536.80451209540*t);
      jupiter_x_1+=     0.00081697204 * Math.cos( 3.46668108797 +        7.11354700080*t);
      jupiter_x_1+=     0.00046201898 * Math.cos( 0.45714214032 +     1589.07289528380*t);
      jupiter_x_1+=     0.00032508590 * Math.cos( 1.74648849928 +     1052.26838318840*t);
      jupiter_x_1+=     0.00033891193 * Math.cos( 4.10113482752 +      529.69096509460*t);
      jupiter_x_1+=     0.00031234303 * Math.cos( 2.34698051502 +     1066.49547719000*t);
      jupiter_x_1+=     0.00021244363 * Math.cos( 4.36576178953 +      110.20632121940*t);
      jupiter_x_1+=     0.00018156701 * Math.cos( 4.00572238779 +      426.59819087600*t);
      jupiter_x_1+=     0.00013577576 * Math.cos( 0.30008010246 +      632.78373931320*t);
      jupiter_x_1+=     0.00012889505 * Math.cos( 2.57489294062 +      515.46387109300*t);
      jupiter_x_1+=     0.00009125875 * Math.cos( 1.78082469962 +      543.91805909620*t);
      jupiter_x_1+=     0.00008085991 * Math.cos( 6.16136518902 +      949.17560896980*t);
      jupiter_x_1+=     0.00007142547 * Math.cos( 3.17267801203 +      323.50541665740*t);
      jupiter_x_1+=     0.00004292240 * Math.cos( 4.74970626655 +      206.18554843720*t);
      jupiter_x_1+=     0.00004393977 * Math.cos( 1.14770788063 +      735.87651353180*t);
      jupiter_x_1+=     0.00003399164 * Math.cos( 2.90091450747 +      526.50957135690*t);
      jupiter_x_1+=     0.00003333344 * Math.cos( 1.43691652967 +      532.87235883230*t);
      jupiter_x_1+=     0.00003873467 * Math.cos( 3.33648870101 +       14.22709400160*t);
      jupiter_x_1+=     0.00003044408 * Math.cos( 1.65428048669 +      525.75881183150*t);
      jupiter_x_1+=     0.00003001874 * Math.cos( 2.68376982746 +      533.62311835770*t);
      jupiter_x_1+=     0.00002933359 * Math.cos( 2.61899855005 +      419.48464387520*t);
      jupiter_x_1+=     0.00002438199 * Math.cos( 3.60655644537 +      316.39186965660*t);
      jupiter_x_1+=     0.00002804218 * Math.cos( 4.89742591320 +      103.09277421860*t);
      jupiter_x_1+=     0.00002990245 * Math.cos( 0.80692155639 +     2118.76386037840*t);
      jupiter_x_1+=     0.00001977572 * Math.cos( 5.08915489088 +      956.28915597060*t);
      jupiter_x_1+=     0.00001853679 * Math.cos( 2.76941001747 +     1596.18644228460*t);
      jupiter_x_1+=     0.00001772800 * Math.cos( 0.72631739446 +      742.99006053260*t);
      jupiter_x_1+=     0.00001812965 * Math.cos( 3.84602148747 +       95.97922721780*t);
      jupiter_x_1+=     0.00001532945 * Math.cos( 4.31556714501 +      117.31986822020*t);
      jupiter_x_1+=     0.00001904067 * Math.cos( 1.85937873703 +     1581.95934828300*t);
      jupiter_x_1+=     0.00001539212 * Math.cos( 1.47899172821 +      639.89728631400*t);
      jupiter_x_1+=     0.00001632362 * Math.cos( 1.41504212408 +     1045.15483618760*t);
      jupiter_x_1+=     0.00001023812 * Math.cos( 2.57182697715 +      433.71173787680*t);
      jupiter_x_1+=     0.00001055422 * Math.cos( 2.50844222977 +     1265.56747862640*t);
      jupiter_x_1+=     0.00000981775 * Math.cos( 2.18800022614 +      220.41264243880*t);
      jupiter_x_1+=     0.00000940094 * Math.cos( 1.34873014473 +      625.67019231240*t);
      jupiter_x_1+=     0.00000839712 * Math.cos( 6.20534871612 +      942.06206196900*t);
      jupiter_x_1+=     0.00000985733 * Math.cos( 1.42746834265 +     1169.58825140860*t);
      jupiter_x_1+=     0.00000778939 * Math.cos( 5.49323533683 +      309.27832265580*t);
      jupiter_x_1+=     0.00000765192 * Math.cos( 1.96892067856 +     1155.36115740700*t);
      jupiter_x_1+=     0.00000643975 * Math.cos( 4.25838784988 +      213.29909543800*t);
      jupiter_x_1+=     0.00000734378 * Math.cos( 0.11449859192 +     1162.47470440780*t);
      jupiter_x_1+=     0.00000538315 * Math.cos( 4.24575280150 +      853.19638175200*t);
      jupiter_x_1+=     0.00000501903 * Math.cos( 4.81386721508 +      199.07200143640*t);
      jupiter_x_1+=     0.00000471426 * Math.cos( 5.91213180419 +     1692.16566950240*t);
      jupiter_x_1+=     0.00000499873 * Math.cos( 3.02041735659 +      330.61896365820*t);
      jupiter_x_1+=     0.00000383793 * Math.cos( 2.17143854666 +     1073.60902419080*t);
      jupiter_x_1+=     0.00000428181 * Math.cos( 3.20065784490 +      412.37109687440*t);
      jupiter_x_1+=     0.00000392314 * Math.cos( 6.21042734222 +     1478.86657406440*t);
      jupiter_x_1+=     0.00000312829 * Math.cos( 2.92313613250 +      838.96928775040*t);
      jupiter_x_1+=     0.00000349351 * Math.cos( 1.49898400680 +      728.76296653100*t);
      jupiter_x_1+=     0.00000227200 * Math.cos( 2.73839039509 +      508.35032409220*t);
      jupiter_x_1+=     0.00000244600 * Math.cos( 1.76024889748 +     1272.68102562720*t);
      jupiter_x_1+=     0.00000228732 * Math.cos( 2.84901766497 +     1375.77379984580*t);
      jupiter_x_1+=     0.00000221540 * Math.cos( 3.09819260401 +        3.18139373770*t);
      jupiter_x_1+=     0.00000180779 * Math.cos( 3.64990601644 +     1368.66025284500*t);
      jupiter_x_1+=     0.00000189492 * Math.cos( 1.15742270920 +     2648.45482547300*t);
      jupiter_x_1+=     0.00000173940 * Math.cos( 1.85326390850 +     1062.56332392690*t);
      jupiter_x_1+=     0.00000160856 * Math.cos( 3.02744600090 +      519.39602435610*t);
      jupiter_x_1+=     0.00000144310 * Math.cos( 2.08463794343 +     1055.44977692610*t);
      jupiter_x_1+=     0.00000131314 * Math.cos( 2.97898157385 +     1258.45393162560*t);
      jupiter_x_1+=     0.00000125629 * Math.cos( 3.31850855112 +     1063.31408345230*t);
      jupiter_x_1+=     0.00000124852 * Math.cos( 1.62031036516 +      551.03160609700*t);
      jupiter_x_1+=     0.00000125162 * Math.cos( 1.31558469253 +      539.98590583310*t);
      jupiter_x_1+=     0.00000146706 * Math.cos( 2.72430580528 +     1056.20053645150*t);
      jupiter_x_1+=     0.00000115911 * Math.cos( 3.18147754305 +     2125.87740737920*t);
      jupiter_x_1+=     0.00000114220 * Math.cos( 2.05698914179 +      227.52618943960*t);
      jupiter_x_1+=     0.00000145330 * Math.cos( 6.08208734754 +     1485.98012106520*t);
      jupiter_x_1+=     0.00000118500 * Math.cos( 5.96270592372 +        3.93215326310*t);
      jupiter_x_1+=     0.00000103412 * Math.cos( 2.02926761934 +     2111.65031337760*t);
      jupiter_x_1+=     0.00000106938 * Math.cos( 1.67885758408 +     1574.84580128220*t);
      jupiter_x_1+=     0.00000102548 * Math.cos( 3.17928973305 +       21.34064100240*t);
      jupiter_x_1=jupiter_x_1 * t;

      let jupiter_x_2=0.0;
      jupiter_x_2+=     0.00123864644 * Math.cos( 4.13563277513 +      522.57741809380*t);
      jupiter_x_2+=     0.00121521296 * Math.cos( 0.21155109275 +      536.80451209540*t);
      jupiter_x_2+=     0.00085355503 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_x_2+=     0.00077685547 * Math.cos( 5.29776154458 +      529.69096509460*t);
      jupiter_x_2+=     0.00041410887 * Math.cos( 5.12291589939 +     1059.38193018920*t);
      jupiter_x_2+=     0.00011423070 * Math.cos( 1.72917878238 +        7.11354700080*t);
      jupiter_x_2+=     0.00007051587 * Math.cos( 0.74163703419 +     1066.49547719000*t);
      jupiter_x_2+=     0.00005711029 * Math.cos( 3.63172846494 +     1052.26838318840*t);
      jupiter_x_2+=     0.00005242644 * Math.cos( 4.27482379441 +      515.46387109300*t);
      jupiter_x_2+=     0.00004039540 * Math.cos( 5.58417732117 +     1589.07289528380*t);
      jupiter_x_2+=     0.00003706457 * Math.cos( 0.07769981349 +      543.91805909620*t);
      jupiter_x_2+=     0.00001698817 * Math.cos( 2.44284418066 +      110.20632121940*t);
      jupiter_x_2+=     0.00001134598 * Math.cos( 2.35807061809 +      426.59819087600*t);
      jupiter_x_2+=     0.00001322673 * Math.cos( 1.63142549980 +       14.22709400160*t);
      jupiter_x_2+=     0.00000888203 * Math.cos( 4.66627290244 +      526.50957135690*t);
      jupiter_x_2+=     0.00000865547 * Math.cos( 5.95596888539 +      532.87235883230*t);
      jupiter_x_2+=     0.00000822579 * Math.cos( 1.96473995078 +      632.78373931320*t);
      jupiter_x_2+=     0.00000994008 * Math.cos( 1.46985522253 +      323.50541665740*t);
      jupiter_x_2+=     0.00000574066 * Math.cos( 1.66926588148 +      949.17560896980*t);
      jupiter_x_2+=     0.00000733386 * Math.cos( 0.37132887987 +      103.09277421860*t);
      jupiter_x_2+=     0.00000571711 * Math.cos( 3.16912095909 +     1045.15483618760*t);
      jupiter_x_2+=     0.00000514256 * Math.cos( 5.97103330686 +      525.75881183150*t);
      jupiter_x_2+=     0.00000512225 * Math.cos( 4.65535000010 +      533.62311835770*t);
      jupiter_x_2+=     0.00000595930 * Math.cos( 2.85993171505 +      735.87651353180*t);
      jupiter_x_2+=     0.00000458533 * Math.cos( 1.24450068286 +     1596.18644228460*t);
      jupiter_x_2+=     0.00000419126 * Math.cos( 2.61042238424 +      117.31986822020*t);
      jupiter_x_2+=     0.00000374840 * Math.cos( 5.55821526471 +       95.97922721780*t);
      jupiter_x_2+=     0.00000341765 * Math.cos( 0.39491407125 +      206.18554843720*t);
      jupiter_x_2+=     0.00000332926 * Math.cos( 6.00008752152 +     2118.76386037840*t);
      jupiter_x_2+=     0.00000294743 * Math.cos( 4.41871274898 +      419.48464387520*t);
      jupiter_x_2+=     0.00000282018 * Math.cos( 3.71098262370 +     1581.95934828300*t);
      jupiter_x_2+=     0.00000264464 * Math.cos( 3.68007673744 +      956.28915597060*t);
      jupiter_x_2+=     0.00000225624 * Math.cos( 1.67501674489 +      942.06206196900*t);
      jupiter_x_2+=     0.00000221808 * Math.cos( 0.88408008289 +      433.71173787680*t);
      jupiter_x_2+=     0.00000225587 * Math.cos( 3.03530345980 +      625.67019231240*t);
      jupiter_x_2+=     0.00000204420 * Math.cos( 0.47807959065 +      220.41264243880*t);
      jupiter_x_2+=     0.00000196750 * Math.cos( 6.00388890575 +     1169.58825140860*t);
      jupiter_x_2+=     0.00000196048 * Math.cos( 5.98648295745 +      639.89728631400*t);
      jupiter_x_2+=     0.00000164833 * Math.cos( 5.35422849201 +      316.39186965660*t);
      jupiter_x_2+=     0.00000163628 * Math.cos( 0.52534435976 +     1073.60902419080*t);
      jupiter_x_2+=     0.00000160814 * Math.cos( 3.59856351339 +     1155.36115740700*t);
      jupiter_x_2+=     0.00000137153 * Math.cos( 4.44130584150 +      508.35032409220*t);
      jupiter_x_2+=     0.00000137429 * Math.cos( 0.24727364545 +      199.07200143640*t);
      jupiter_x_2+=     0.00000170296 * Math.cos( 1.32514412307 +      330.61896365820*t);
      jupiter_x_2+=     0.00000116446 * Math.cos( 5.49080485025 +      742.99006053260*t);
      jupiter_x_2+=     0.00000105301 * Math.cos( 2.68783089944 +      853.19638175200*t);
      jupiter_x_2+=     0.00000104117 * Math.cos( 0.79163400573 +      309.27832265580*t);
      jupiter_x_2+=     0.00000121829 * Math.cos( 3.11437651993 +      728.76296653100*t);
      jupiter_x_2+=     0.00000118326 * Math.cos( 2.48566246801 +      213.29909543800*t);
      jupiter_x_2+=     0.00000107997 * Math.cos( 4.63298682919 +     1162.47470440780*t);
      jupiter_x_2+=     0.00000103302 * Math.cos( 4.83833077255 +      412.37109687440*t);
      jupiter_x_2=jupiter_x_2 * t * t;

      let jupiter_x_3=0.0;
      jupiter_x_3+=     0.00017071323 * Math.cos( 5.86133022278 +      522.57741809380*t);
      jupiter_x_3+=     0.00016713548 * Math.cos( 4.77458794485 +      536.80451209540*t);
      jupiter_x_3+=     0.00003348610 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_x_3+=     0.00001787838 * Math.cos( 3.56550298031 +     1059.38193018920*t);
      jupiter_x_3+=     0.00001435449 * Math.cos( 5.98502036587 +      515.46387109300*t);
      jupiter_x_3+=     0.00001080194 * Math.cos( 5.42530305914 +     1066.49547719000*t);
      jupiter_x_3+=     0.00001014206 * Math.cos( 4.64773902077 +      543.91805909620*t);
      jupiter_x_3+=     0.00001073175 * Math.cos( 6.22314467964 +        7.11354700080*t);
      jupiter_x_3+=     0.00000711065 * Math.cos( 5.50680515205 +     1052.26838318840*t);
      jupiter_x_3+=     0.00000261089 * Math.cos( 4.28269834394 +     1589.07289528380*t);
      jupiter_x_3+=     0.00000301054 * Math.cos( 6.19841321090 +       14.22709400160*t);
      jupiter_x_3+=     0.00000134738 * Math.cos( 4.94746197927 +     1045.15483618760*t);
      jupiter_x_3+=     0.00000124290 * Math.cos( 0.37523072266 +      110.20632121940*t);
      jupiter_x_3=jupiter_x_3 * t * t * t;

      let jupiter_x_4=0.0;
      jupiter_x_4+=     0.00001762402 * Math.cos( 1.32863039757 +      522.57741809380*t);
      jupiter_x_4+=     0.00001717846 * Math.cos( 3.03331531843 +      536.80451209540*t);
      jupiter_x_4+=     0.00000304063 * Math.cos( 1.43144096257 +      515.46387109300*t);
      jupiter_x_4+=     0.00000216508 * Math.cos( 2.91205595526 +      543.91805909620*t);
      jupiter_x_4+=     0.00000128193 * Math.cos( 3.83022265336 +     1066.49547719000*t);
      jupiter_x_4+=     0.00000160571 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_x_4=jupiter_x_4 * t * t * t * t;

      let jupiter_x_5=0.0;
      jupiter_x_5+=     0.00000131471 * Math.cos( 3.21284928867 +      522.57741809380*t);
      jupiter_x_5+=     0.00000126748 * Math.cos( 1.16307002134 +      536.80451209540*t);
      jupiter_x_5=jupiter_x_5 * t * t * t * t * t;

      return jupiter_x_0+jupiter_x_1+jupiter_x_2+jupiter_x_3+jupiter_x_4+jupiter_x_5;
   }

   static jupiter_y(t){
      let jupiter_y_0=0.0;
      jupiter_y_0+=     5.19520046589 * Math.cos( 5.31203162731 +      529.69096509460*t);
      jupiter_y_0+=     0.12592862602 * Math.cos( 5.66160227728 +     1059.38193018920*t);
      jupiter_y_0+=     0.09363670616 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_y_0+=     0.01508275299 * Math.cos( 5.43934968102 +      522.57741809380*t);
      jupiter_y_0+=     0.01475809370 * Math.cos( 2.04679566495 +      536.80451209540*t);
      jupiter_y_0+=     0.00457750806 * Math.cos( 6.01129093501 +     1589.07289528380*t);
      jupiter_y_0+=     0.00300686679 * Math.cos( 3.60948050740 +        7.11354700080*t);
      jupiter_y_0+=     0.00378285578 * Math.cos( 3.53006782383 +      103.09277421860*t);
      jupiter_y_0+=     0.00192333128 * Math.cos( 3.45690564771 +      426.59819087600*t);
      jupiter_y_0+=     0.00146104656 * Math.cos( 4.62267224431 +      110.20632121940*t);
      jupiter_y_0+=     0.00139480058 * Math.cos( 4.00075307706 +      632.78373931320*t);
      jupiter_y_0+=     0.00132696764 * Math.cos( 5.62184581859 +      213.29909543800*t);
      jupiter_y_0+=     0.00101999807 * Math.cos( 4.57594598884 +     1052.26838318840*t);
      jupiter_y_0+=     0.00114043110 * Math.cos( 4.72982262969 +     1162.47470440780*t);
      jupiter_y_0+=     0.00072091178 * Math.cos( 2.39048659148 +     1066.49547719000*t);
      jupiter_y_0+=     0.00059051769 * Math.cos( 2.89529070968 +      949.17560896980*t);
      jupiter_y_0+=     0.00068374489 * Math.cos( 1.86537074374 +      846.08283475120*t);
      jupiter_y_0+=     0.00029807369 * Math.cos( 4.52105772740 +      206.18554843720*t);
      jupiter_y_0+=     0.00026933579 * Math.cos( 3.86233956827 +      419.48464387520*t);
      jupiter_y_0+=     0.00026619714 * Math.cos( 3.28203174951 +      323.50541665740*t);
      jupiter_y_0+=     0.00020873780 * Math.cos( 3.79369881757 +      735.87651353180*t);
      jupiter_y_0+=     0.00019727397 * Math.cos( 0.07818534532 +     2118.76386037840*t);
      jupiter_y_0+=     0.00018639846 * Math.cos( 0.38751972138 +      316.39186965660*t);
      jupiter_y_0+=     0.00016355726 * Math.cos( 5.56997881604 +      515.46387109300*t);
      jupiter_y_0+=     0.00014606858 * Math.cos( 0.47759399145 +      742.99006053260*t);
      jupiter_y_0+=     0.00011419853 * Math.cos( 1.91089341468 +      543.91805909620*t);
      jupiter_y_0+=     0.00012153427 * Math.cos( 2.18151972499 +      525.75881183150*t);
      jupiter_y_0+=     0.00011988875 * Math.cos( 5.29687602089 +      533.62311835770*t);
      jupiter_y_0+=     0.00008443107 * Math.cos( 1.91435801697 +      639.89728631400*t);
      jupiter_y_0+=     0.00008163163 * Math.cos( 4.00303742375 +     1478.86657406440*t);
      jupiter_y_0+=     0.00008732789 * Math.cos( 5.09607066097 +     1692.16566950240*t);
      jupiter_y_0+=     0.00007414115 * Math.cos( 4.41141990461 +      956.28915597060*t);
      jupiter_y_0+=     0.00007619486 * Math.cos( 5.59554151997 +     1265.56747862640*t);
      jupiter_y_0+=     0.00007779184 * Math.cos( 4.83346300662 +     1581.95934828300*t);
      jupiter_y_0+=     0.00005322882 * Math.cos( 5.81740472645 +      526.50957135690*t);
      jupiter_y_0+=     0.00005217025 * Math.cos( 1.66178643542 +      532.87235883230*t);
      jupiter_y_0+=     0.00005772132 * Math.cos( 3.46915716927 +       14.22709400160*t);
      jupiter_y_0+=     0.00004528355 * Math.cos( 2.18377558038 +     1375.77379984580*t);
      jupiter_y_0+=     0.00003939875 * Math.cos( 2.73830531054 +     1596.18644228460*t);
      jupiter_y_0+=     0.00004567181 * Math.cos( 3.71300776935 +       95.97922721780*t);
      jupiter_y_0+=     0.00003235419 * Math.cos( 4.76600347062 +      625.67019231240*t);
      jupiter_y_0+=     0.00003140740 * Math.cos( 5.59566796922 +      309.27832265580*t);
      jupiter_y_0+=     0.00002855423 * Math.cos( 4.44478286006 +      117.31986822020*t);
      jupiter_y_0+=     0.00002445625 * Math.cos( 2.67036952230 +      433.71173787680*t);
      jupiter_y_0+=     0.00002253545 * Math.cos( 4.28462825722 +      838.96928775040*t);
      jupiter_y_0+=     0.00002672262 * Math.cos( 1.61857897069 +     1169.58825140860*t);
      jupiter_y_0+=     0.00002423639 * Math.cos( 2.32942339839 +      220.41264243880*t);
      jupiter_y_0+=     0.00002362662 * Math.cos( 4.60417580207 +     1155.36115740700*t);
      jupiter_y_0+=     0.00002409581 * Math.cos( 4.33196301609 +     1045.15483618760*t);
      jupiter_y_0+=     0.00001458169 * Math.cos( 4.18761881277 +      853.19638175200*t);
      jupiter_y_0+=     0.00001432195 * Math.cos( 3.24824554500 +      942.06206196900*t);
      jupiter_y_0+=     0.00001646568 * Math.cos( 3.91965876562 +       74.78159856730*t);
      jupiter_y_0+=     0.00001050270 * Math.cos( 4.83706014327 +     1795.25844372100*t);
      jupiter_y_0+=     0.00001002355 * Math.cos( 1.50931939870 +     1272.68102562720*t);
      jupiter_y_0+=     0.00000922972 * Math.cos( 4.68727792575 +      199.07200143640*t);
      jupiter_y_0+=     0.00000934476 * Math.cos( 0.42886055430 +     2648.45482547300*t);
      jupiter_y_0+=     0.00000858322 * Math.cos( 2.14237489817 +      529.64278098480*t);
      jupiter_y_0+=     0.00000858227 * Math.cos( 5.34018602564 +      529.73914920440*t);
      jupiter_y_0+=     0.00001087727 * Math.cos( 5.84673086939 +      527.24328453980*t);
      jupiter_y_0+=     0.00001079512 * Math.cos( 1.63448507346 +      532.13864564940*t);
      jupiter_y_0+=     0.00000806006 * Math.cos( 1.68267639334 +     1368.66025284500*t);
      jupiter_y_0+=     0.00000957270 * Math.cos( 6.06002229163 +      149.56319713460*t);
      jupiter_y_0+=     0.00000847127 * Math.cos( 5.93043140082 +        3.93215326310*t);
      jupiter_y_0+=     0.00000980751 * Math.cos( 0.62999941324 +      380.12776796000*t);
      jupiter_y_0+=     0.00000682080 * Math.cos( 4.52942528324 +     2008.55753915900*t);
      jupiter_y_0+=     0.00000669757 * Math.cos( 4.03016406200 +      728.76296653100*t);
      jupiter_y_0+=     0.00000747759 * Math.cos( 3.13980492033 +      330.61896365820*t);
      jupiter_y_0+=     0.00000623272 * Math.cos( 4.84897478374 +     2111.65031337760*t);
      jupiter_y_0+=     0.00000693931 * Math.cos( 6.05213927263 +     1063.31408345230*t);
      jupiter_y_0+=     0.00000679997 * Math.cos( 5.00632204302 +      528.72775724810*t);
      jupiter_y_0+=     0.00000678365 * Math.cos( 2.47630881775 +      530.65417294110*t);
      jupiter_y_0+=     0.00000575319 * Math.cos( 5.46049674365 +     2221.85663459700*t);
      jupiter_y_0+=     0.00000562901 * Math.cos( 2.49305547670 +     1055.44977692610*t);
      jupiter_y_0+=     0.00000518936 * Math.cos( 4.17355493103 +      412.37109687440*t);
      jupiter_y_0+=     0.00000647097 * Math.cos( 3.55496391590 +      984.60033162190*t);
      jupiter_y_0+=     0.00000456078 * Math.cos( 3.65466665401 +     1471.75302706360*t);
      jupiter_y_0+=     0.00000459952 * Math.cos( 2.25589512899 +     1073.60902419080*t);
      jupiter_y_0+=     0.00000540076 * Math.cos( 3.74723115522 +       38.13303563780*t);
      jupiter_y_0+=     0.00000410344 * Math.cos( 1.41779899532 +      909.81873305460*t);
      jupiter_y_0+=     0.00000357023 * Math.cos( 5.38580302034 +     1258.45393162560*t);
      jupiter_y_0+=     0.00000299281 * Math.cos( 2.48546398700 +     1905.46476494040*t);
      jupiter_y_0+=     0.00000333647 * Math.cos( 5.66593038440 +       76.26607127560*t);
      jupiter_y_0+=     0.00000388450 * Math.cos( 4.49029761988 +      604.47256366190*t);
      jupiter_y_0+=     0.00000381037 * Math.cos( 3.30799287543 +        3.18139373770*t);
      jupiter_y_0+=     0.00000303843 * Math.cos( 3.49297492409 +      529.16970023280*t);
      jupiter_y_0+=     0.00000303451 * Math.cos( 3.98820790955 +      530.21222995640*t);
      jupiter_y_0+=     0.00000275733 * Math.cos( 5.36302088998 +     1485.98012106520*t);
      jupiter_y_0+=     0.00000360736 * Math.cos( 2.95686029502 +      454.90936652730*t);
      jupiter_y_0+=     0.00000254327 * Math.cos( 2.01404147058 +     1062.56332392690*t);
      jupiter_y_0+=     0.00000263791 * Math.cos( 4.57708545504 +     1574.84580128220*t);
      jupiter_y_0+=     0.00000226963 * Math.cos( 3.08749062400 +     2125.87740737920*t);
      jupiter_y_0+=     0.00000304142 * Math.cos( 0.18267926862 +     6283.07584999140*t);
      jupiter_y_0+=     0.00000291946 * Math.cos( 4.55436664519 +      305.34616939270*t);
      jupiter_y_0+=     0.00000225580 * Math.cos( 1.93114465962 +     1699.27921650320*t);
      jupiter_y_0+=     0.00000195868 * Math.cos( 5.71186875574 +      508.35032409220*t);
      jupiter_y_0+=     0.00000233285 * Math.cos( 5.63548319924 +     1056.20053645150*t);
      jupiter_y_0+=     0.00000210214 * Math.cos( 2.44863388631 +      490.33408917940*t);
      jupiter_y_0+=     0.00000178839 * Math.cos( 4.53006992902 +      526.77020378780*t);
      jupiter_y_0+=     0.00000177005 * Math.cos( 2.95243321654 +      532.61172640140*t);
      jupiter_y_0+=     0.00000172351 * Math.cos( 5.18722712249 +     1898.35121793960*t);
      jupiter_y_0+=     0.00000165053 * Math.cos( 1.90578907085 +      528.94020556920*t);
      jupiter_y_0+=     0.00000164585 * Math.cos( 5.57619428876 +      530.44172462000*t);
      jupiter_y_0+=     0.00000191497 * Math.cos( 5.01693056182 +      569.04784100980*t);
      jupiter_y_0+=     0.00000155401 * Math.cos( 5.96579992385 +      519.39602435610*t);
      jupiter_y_0+=     0.00000215233 * Math.cos( 0.97247023787 +      453.42489381900*t);
      jupiter_y_0+=     0.00000208229 * Math.cos( 1.82281614022 +     1439.50969814920*t);
      jupiter_y_0+=     0.00000157996 * Math.cos( 2.75766580241 +      525.49817940060*t);
      jupiter_y_0+=     0.00000155479 * Math.cos( 4.72686997635 +      533.88375078860*t);
      jupiter_y_0+=     0.00000166712 * Math.cos( 2.08631169849 +      224.34479570190*t);
      jupiter_y_0+=     0.00000139402 * Math.cos( 1.78553934341 +      647.01083331480*t);
      jupiter_y_0+=     0.00000194580 * Math.cos( 3.73461183144 +     1021.24889455140*t);
      jupiter_y_0+=     0.00000152633 * Math.cos( 5.70470310157 +      302.16477565500*t);
      jupiter_y_0+=     0.00000136386 * Math.cos( 0.96879673890 +       11.04570026390*t);
      jupiter_y_0+=     0.00000142502 * Math.cos( 2.18746053267 +      227.52618943960*t);
      jupiter_y_0+=     0.00000176907 * Math.cos( 1.60589176438 +    10213.28554621100*t);
      jupiter_y_0+=     0.00000124507 * Math.cos( 3.45933363747 +     1788.14489672020*t);
      jupiter_y_0+=     0.00000174817 * Math.cos( 0.43249591548 +        1.48447270830*t);
      jupiter_y_0+=     0.00000133665 * Math.cos( 4.63491612092 +      831.85574074960*t);
      jupiter_y_0+=     0.00000120579 * Math.cos( 1.51220177525 +      539.98590583310*t);
      jupiter_y_0+=     0.00000134336 * Math.cos( 2.22677523856 +      540.73666535850*t);
      jupiter_y_0+=     0.00000121877 * Math.cos( 2.21859738997 +      524.06189080210*t);
      jupiter_y_0+=     0.00000120032 * Math.cos( 5.26558291500 +      535.32003938710*t);
      jupiter_y_0+=     0.00000124427 * Math.cos( 1.81779375202 +      983.11585891360*t);
      jupiter_y_0+=     0.00000147154 * Math.cos( 2.17687114643 +     1685.05212250160*t);
      jupiter_y_0+=     0.00000123569 * Math.cos( 1.77578705200 +      525.02509864860*t);
      jupiter_y_0+=     0.00000117660 * Math.cos( 1.79992315819 +      750.10360753340*t);
      jupiter_y_0+=     0.00000104430 * Math.cos( 2.19472066370 +      529.53090640020*t);
      jupiter_y_0+=     0.00000104430 * Math.cos( 5.28755763826 +      529.85102378900*t);
      jupiter_y_0+=     0.00000104807 * Math.cos( 1.75473051914 +      551.03160609700*t);
      jupiter_y_0+=     0.00000119646 * Math.cos( 5.02394125709 +     2324.94940881560*t);
      jupiter_y_0+=     0.00000116159 * Math.cos( 5.71003552223 +      534.35683154060*t);
      jupiter_y_0+=     0.00000122805 * Math.cos( 3.33550927204 +      524.27433912320*t);
      jupiter_y_0+=     0.00000103138 * Math.cos( 2.84304085733 +      963.40270297140*t);
      jupiter_y_0+=     0.00000120958 * Math.cos( 4.14524856046 +      535.10759106600*t);
      jupiter_y_0+=     0.00000106645 * Math.cos( 4.96153948786 +       99.16062095550*t);
      jupiter_y_0+=     0.00000125536 * Math.cos( 5.60866656844 +      618.55664531160*t);
      jupiter_y_0+=     0.00000111205 * Math.cos( 1.86928344986 +     2001.44399215820*t);

      let jupiter_y_1=0.0;
      jupiter_y_1+=     0.01694798253 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_y_1+=     0.00634859798 * Math.cos( 4.81903199650 +     1059.38193018920*t);
      jupiter_y_1+=     0.00601160431 * Math.cos( 0.85811249940 +      522.57741809380*t);
      jupiter_y_1+=     0.00588928504 * Math.cos( 0.34491576890 +      536.80451209540*t);
      jupiter_y_1+=     0.00081187145 * Math.cos( 1.90914316532 +        7.11354700080*t);
      jupiter_y_1+=     0.00046888090 * Math.cos( 1.91294535618 +      529.69096509460*t);
      jupiter_y_1+=     0.00046194129 * Math.cos( 5.16955994561 +     1589.07289528380*t);
      jupiter_y_1+=     0.00032503453 * Math.cos( 0.17640743623 +     1052.26838318840*t);
      jupiter_y_1+=     0.00031231694 * Math.cos( 0.77623645597 +     1066.49547719000*t);
      jupiter_y_1+=     0.00019462096 * Math.cos( 3.00957119470 +      110.20632121940*t);
      jupiter_y_1+=     0.00017738615 * Math.cos( 2.46531787101 +      426.59819087600*t);
      jupiter_y_1+=     0.00013701692 * Math.cos( 5.02070197804 +      632.78373931320*t);
      jupiter_y_1+=     0.00013034616 * Math.cos( 0.98979834442 +      515.46387109300*t);
      jupiter_y_1+=     0.00009122660 * Math.cos( 0.21022587969 +      543.91805909620*t);
      jupiter_y_1+=     0.00008109050 * Math.cos( 4.58123811601 +      949.17560896980*t);
      jupiter_y_1+=     0.00007145229 * Math.cos( 1.60381236094 +      323.50541665740*t);
      jupiter_y_1+=     0.00003957592 * Math.cos( 6.18550697817 +      206.18554843720*t);
      jupiter_y_1+=     0.00004347346 * Math.cos( 5.85522835488 +      735.87651353180*t);
      jupiter_y_1+=     0.00003401735 * Math.cos( 1.33033225252 +      526.50957135690*t);
      jupiter_y_1+=     0.00003331887 * Math.cos( 6.14951835712 +      532.87235883230*t);
      jupiter_y_1+=     0.00003866147 * Math.cos( 1.76877582038 +       14.22709400160*t);
      jupiter_y_1+=     0.00003094257 * Math.cos( 1.00670454701 +      419.48464387520*t);
      jupiter_y_1+=     0.00003044205 * Math.cos( 0.08329779827 +      525.75881183150*t);
      jupiter_y_1+=     0.00003001484 * Math.cos( 1.11280606283 +      533.62311835770*t);
      jupiter_y_1+=     0.00002977284 * Math.cos( 3.35507028507 +      103.09277421860*t);
      jupiter_y_1+=     0.00002347100 * Math.cos( 2.06781775390 +      316.39186965660*t);
      jupiter_y_1+=     0.00002990192 * Math.cos( 5.51944830506 +     2118.76386037840*t);
      jupiter_y_1+=     0.00001875464 * Math.cos( 5.32657356489 +      742.99006053260*t);
      jupiter_y_1+=     0.00001854067 * Math.cos( 1.19908734197 +     1596.18644228460*t);
      jupiter_y_1+=     0.00001968401 * Math.cos( 3.51896739844 +      956.28915597060*t);
      jupiter_y_1+=     0.00001808627 * Math.cos( 5.40287543026 +       95.97922721780*t);
      jupiter_y_1+=     0.00001530472 * Math.cos( 2.75094722237 +      117.31986822020*t);
      jupiter_y_1+=     0.00001885393 * Math.cos( 0.29905973710 +     1581.95934828300*t);
      jupiter_y_1+=     0.00001516541 * Math.cos( 6.21684203571 +      639.89728631400*t);
      jupiter_y_1+=     0.00001636913 * Math.cos( 6.09270756447 +     1045.15483618760*t);
      jupiter_y_1+=     0.00001260123 * Math.cos( 0.07143173954 +      625.67019231240*t);
      jupiter_y_1+=     0.00001028165 * Math.cos( 1.00301485824 +      433.71173787680*t);
      jupiter_y_1+=     0.00001035933 * Math.cos( 0.98273794152 +     1265.56747862640*t);
      jupiter_y_1+=     0.00000972507 * Math.cos( 0.63832646360 +      220.41264243880*t);
      jupiter_y_1+=     0.00000983542 * Math.cos( 6.14294208089 +     1169.58825140860*t);
      jupiter_y_1+=     0.00000778705 * Math.cos( 4.83558543631 +      942.06206196900*t);
      jupiter_y_1+=     0.00000886143 * Math.cos( 1.10269264426 +      309.27832265580*t);
      jupiter_y_1+=     0.00000841776 * Math.cos( 0.18391927728 +     1155.36115740700*t);
      jupiter_y_1+=     0.00000767993 * Math.cos( 4.84778769533 +     1162.47470440780*t);
      jupiter_y_1+=     0.00000541536 * Math.cos( 2.66914118638 +      853.19638175200*t);
      jupiter_y_1+=     0.00000492134 * Math.cos( 0.10409782456 +      199.07200143640*t);
      jupiter_y_1+=     0.00000482717 * Math.cos( 4.31776421398 +     1692.16566950240*t);
      jupiter_y_1+=     0.00000551952 * Math.cos( 5.72755176773 +      213.29909543800*t);
      jupiter_y_1+=     0.00000474411 * Math.cos( 0.05053932644 +      838.96928775040*t);
      jupiter_y_1+=     0.00000499533 * Math.cos( 1.45057427365 +      330.61896365820*t);
      jupiter_y_1+=     0.00000383799 * Math.cos( 0.60154705725 +     1073.60902419080*t);
      jupiter_y_1+=     0.00000411804 * Math.cos( 5.82478065965 +      728.76296653100*t);
      jupiter_y_1+=     0.00000411901 * Math.cos( 4.63999690546 +     1478.86657406440*t);
      jupiter_y_1+=     0.00000233099 * Math.cos( 1.13630657752 +      508.35032409220*t);
      jupiter_y_1+=     0.00000249127 * Math.cos( 0.16936457581 +     1272.68102562720*t);
      jupiter_y_1+=     0.00000198812 * Math.cos( 1.38931486346 +     1375.77379984580*t);
      jupiter_y_1+=     0.00000203327 * Math.cos( 1.40700481195 +        3.18139373770*t);
      jupiter_y_1+=     0.00000213809 * Math.cos( 6.16969757489 +      412.37109687440*t);
      jupiter_y_1+=     0.00000181689 * Math.cos( 2.07919238257 +     1368.66025284500*t);
      jupiter_y_1+=     0.00000174422 * Math.cos( 0.28157513496 +     1062.56332392690*t);
      jupiter_y_1+=     0.00000189289 * Math.cos( 5.86994869354 +     2648.45482547300*t);
      jupiter_y_1+=     0.00000167410 * Math.cos( 0.94422476456 +     1258.45393162560*t);
      jupiter_y_1+=     0.00000155276 * Math.cos( 2.11664870228 +        3.93215326310*t);
      jupiter_y_1+=     0.00000161385 * Math.cos( 1.44976282992 +      519.39602435610*t);
      jupiter_y_1+=     0.00000144101 * Math.cos( 0.51310291971 +     1055.44977692610*t);
      jupiter_y_1+=     0.00000126747 * Math.cos( 1.74459905872 +     1063.31408345230*t);
      jupiter_y_1+=     0.00000124724 * Math.cos( 0.04994633125 +      551.03160609700*t);
      jupiter_y_1+=     0.00000125496 * Math.cos( 6.02560740802 +      539.98590583310*t);
      jupiter_y_1+=     0.00000146632 * Math.cos( 1.15160857972 +     1056.20053645150*t);
      jupiter_y_1+=     0.00000115875 * Math.cos( 1.61097972819 +     2125.87740737920*t);
      jupiter_y_1+=     0.00000117096 * Math.cos( 5.45594228337 +     1471.75302706360*t);
      jupiter_y_1+=     0.00000142963 * Math.cos( 0.02661259114 +     1574.84580128220*t);
      jupiter_y_1+=     0.00000114195 * Math.cos( 0.48862834603 +      227.52618943960*t);
      jupiter_y_1+=     0.00000143564 * Math.cos( 4.51347077218 +     1485.98012106520*t);
      jupiter_y_1+=     0.00000103165 * Math.cos( 1.14841399801 +      302.16477565500*t);
      jupiter_y_1+=     0.00000102127 * Math.cos( 1.62710552101 +       21.34064100240*t);
      jupiter_y_1=jupiter_y_1 * t;

      let jupiter_y_2=0.0;
      jupiter_y_2+=     0.00124032509 * Math.cos( 2.56495576833 +      522.57741809380*t);
      jupiter_y_2+=     0.00121455991 * Math.cos( 4.92398766380 +      536.80451209540*t);
      jupiter_y_2+=     0.00076523263 * Math.cos( 3.75913371793 +      529.69096509460*t);
      jupiter_y_2+=     0.00076943042 * Math.cos( 3.14159265359 +        0.00000000000*t);
      jupiter_y_2+=     0.00041357600 * Math.cos( 3.55228440457 +     1059.38193018920*t);
      jupiter_y_2+=     0.00011277667 * Math.cos( 0.18559902389 +        7.11354700080*t);
      jupiter_y_2+=     0.00007051103 * Math.cos( 5.45404368570 +     1066.49547719000*t);
      jupiter_y_2+=     0.00005719440 * Math.cos( 2.05970000230 +     1052.26838318840*t);
      jupiter_y_2+=     0.00005286157 * Math.cos( 2.69490465064 +      515.46387109300*t);
      jupiter_y_2+=     0.00004039038 * Math.cos( 4.01341034637 +     1589.07289528380*t);
      jupiter_y_2+=     0.00003704528 * Math.cos( 4.79029292271 +      543.91805909620*t);
      jupiter_y_2+=     0.00001280283 * Math.cos( 1.47574006861 +      110.20632121940*t);
      jupiter_y_2+=     0.00001059783 * Math.cos( 0.89610748176 +      426.59819087600*t);
      jupiter_y_2+=     0.00001320627 * Math.cos( 0.05786048417 +       14.22709400160*t);
      jupiter_y_2+=     0.00000888144 * Math.cos( 3.09675195621 +      526.50957135690*t);
      jupiter_y_2+=     0.00000864544 * Math.cos( 4.38537588795 +      532.87235883230*t);
      jupiter_y_2+=     0.00000820223 * Math.cos( 0.37911850134 +      632.78373931320*t);
      jupiter_y_2+=     0.00000993728 * Math.cos( 6.18613980226 +      323.50541665740*t);
      jupiter_y_2+=     0.00000573001 * Math.cos( 0.10744491970 +      949.17560896980*t);
      jupiter_y_2+=     0.00000571480 * Math.cos( 1.57855126864 +     1045.15483618760*t);
      jupiter_y_2+=     0.00000624115 * Math.cos( 1.29414272655 +      735.87651353180*t);
      jupiter_y_2+=     0.00000513863 * Math.cos( 4.40000698225 +      525.75881183150*t);
      jupiter_y_2+=     0.00000511927 * Math.cos( 3.08494935962 +      533.62311835770*t);
      jupiter_y_2+=     0.00000458314 * Math.cos( 5.95712671606 +     1596.18644228460*t);
      jupiter_y_2+=     0.00000417651 * Math.cos( 1.04909922555 +      117.31986822020*t);
      jupiter_y_2+=     0.00000357612 * Math.cos( 2.57817679198 +      419.48464387520*t);
      jupiter_y_2+=     0.00000372789 * Math.cos( 0.82429067684 +       95.97922721780*t);
      jupiter_y_2+=     0.00000332599 * Math.cos( 4.43064686875 +     2118.76386037840*t);
      jupiter_y_2+=     0.00000263411 * Math.cos( 1.67577905079 +      625.67019231240*t);
      jupiter_y_2+=     0.00000261838 * Math.cos( 1.57658925499 +      206.18554843720*t);
      jupiter_y_2+=     0.00000283280 * Math.cos( 2.13607070848 +     1581.95934828300*t);
      jupiter_y_2+=     0.00000261886 * Math.cos( 2.11384561317 +      956.28915597060*t);
      jupiter_y_2+=     0.00000224038 * Math.cos( 5.60156218944 +      433.71173787680*t);
      jupiter_y_2+=     0.00000215118 * Math.cos( 0.20709824197 +      942.06206196900*t);
      jupiter_y_2+=     0.00000200755 * Math.cos( 5.22220831536 +      220.41264243880*t);
      jupiter_y_2+=     0.00000195809 * Math.cos( 4.43848073387 +     1169.58825140860*t);
      jupiter_y_2+=     0.00000169410 * Math.cos( 3.75773944755 +      316.39186965660*t);
      jupiter_y_2+=     0.00000189827 * Math.cos( 4.45615781736 +      639.89728631400*t);
      jupiter_y_2+=     0.00000164118 * Math.cos( 5.23637716488 +     1073.60902419080*t);
      jupiter_y_2+=     0.00000169721 * Math.cos( 1.95956186861 +     1155.36115740700*t);
      jupiter_y_2+=     0.00000139915 * Math.cos( 2.84757472476 +      508.35032409220*t);
      jupiter_y_2+=     0.00000135907 * Math.cos( 3.57562359102 +      742.99006053260*t);
      jupiter_y_2+=     0.00000133577 * Math.cos( 1.81432948760 +      199.07200143640*t);
      jupiter_y_2+=     0.00000170272 * Math.cos( 6.03731209243 +      330.61896365820*t);
      jupiter_y_2+=     0.00000136502 * Math.cos( 2.96677322881 +      309.27832265580*t);
      jupiter_y_2+=     0.00000106637 * Math.cos( 1.10269205617 +      853.19638175200*t);
      jupiter_y_2+=     0.00000134907 * Math.cos( 1.31002677390 +      728.76296653100*t);
      jupiter_y_2+=     0.00000112559 * Math.cos( 3.07810031314 +     1162.47470440780*t);
      jupiter_y_2=jupiter_y_2 * t * t;

      let jupiter_y_3=0.0;
      jupiter_y_3+=     0.00017085516 * Math.cos( 4.29096904063 +      522.57741809380*t);
      jupiter_y_3+=     0.00016701353 * Math.cos( 3.20365737109 +      536.80451209540*t);
      jupiter_y_3+=     0.00004006038 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_y_3+=     0.00001782451 * Math.cos( 1.99283071153 +     1059.38193018920*t);
      jupiter_y_3+=     0.00001443816 * Math.cos( 4.40866555269 +      515.46387109300*t);
      jupiter_y_3+=     0.00001079405 * Math.cos( 3.85450799252 +     1066.49547719000*t);
      jupiter_y_3+=     0.00001013157 * Math.cos( 3.07729621279 +      543.91805909620*t);
      jupiter_y_3+=     0.00001055565 * Math.cos( 4.70184773789 +        7.11354700080*t);
      jupiter_y_3+=     0.00000710385 * Math.cos( 3.93734062697 +     1052.26838318840*t);
      jupiter_y_3+=     0.00000259601 * Math.cos( 2.71566478390 +     1589.07289528380*t);
      jupiter_y_3+=     0.00000300599 * Math.cos( 4.62156117661 +       14.22709400160*t);
      jupiter_y_3+=     0.00000134826 * Math.cos( 3.36277253898 +     1045.15483618760*t);
      jupiter_y_3+=     0.00000142837 * Math.cos( 5.28814307330 +      529.69096509460*t);
      jupiter_y_3=jupiter_y_3 * t * t * t;

      let jupiter_y_4=0.0;
      jupiter_y_4+=     0.00001762645 * Math.cos( 6.04159386554 +      522.57741809380*t);
      jupiter_y_4+=     0.00001716045 * Math.cos( 1.46206285710 +      536.80451209540*t);
      jupiter_y_4+=     0.00000305036 * Math.cos( 6.14052786819 +      515.46387109300*t);
      jupiter_y_4+=     0.00000216203 * Math.cos( 1.34301856666 +      543.91805909620*t);
      jupiter_y_4+=     0.00000127895 * Math.cos( 2.25941664796 +     1066.49547719000*t);
      jupiter_y_4=jupiter_y_4 * t * t * t * t;

      let jupiter_y_5=0.0;
      jupiter_y_5+=     0.00000131471 * Math.cos( 1.64205554066 +      522.57741809380*t);
      jupiter_y_5+=     0.00000126634 * Math.cos( 5.87372673584 +      536.80451209540*t);
      jupiter_y_5=jupiter_y_5 * t * t * t * t * t;

      return jupiter_y_0+jupiter_y_1+jupiter_y_2+jupiter_y_3+jupiter_y_4+jupiter_y_5;
   }

   static jupiter_z(t){
      let jupiter_z_0=0.0;
      jupiter_z_0+=     0.11823100489 * Math.cos( 3.55844646343 +      529.69096509460*t);
      jupiter_z_0+=     0.00859031952 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_z_0+=     0.00286562094 * Math.cos( 3.90812238338 +     1059.38193018920*t);
      jupiter_z_0+=     0.00042388592 * Math.cos( 3.60144191032 +      522.57741809380*t);
      jupiter_z_0+=     0.00033295491 * Math.cos( 0.30297050585 +      536.80451209540*t);
      jupiter_z_0+=     0.00010416160 * Math.cos( 4.25764593061 +     1589.07289528380*t);
      jupiter_z_0+=     0.00007449294 * Math.cos( 5.24213104150 +      103.09277421860*t);
      jupiter_z_0+=     0.00006910102 * Math.cos( 1.75032945752 +        7.11354700080*t);
      jupiter_z_0+=     0.00005292012 * Math.cos( 1.68231447192 +      426.59819087600*t);
      jupiter_z_0+=     0.00004313598 * Math.cos( 3.70673689841 +      213.29909543800*t);
      jupiter_z_0+=     0.00003784265 * Math.cos( 2.71522544491 +      110.20632121940*t);
      jupiter_z_0+=     0.00003798016 * Math.cos( 2.16715743175 +      632.78373931320*t);
      jupiter_z_0+=     0.00002455385 * Math.cos( 2.96904135659 +     1052.26838318840*t);
      jupiter_z_0+=     0.00002461547 * Math.cos( 2.99889460411 +     1162.47470440780*t);
      jupiter_z_0+=     0.00002001451 * Math.cos( 2.68535838309 +      419.48464387520*t);
      jupiter_z_0+=     0.00002163471 * Math.cos( 6.26718259854 +      846.08283475120*t);
      jupiter_z_0+=     0.00001633653 * Math.cos( 0.64194743493 +     1066.49547719000*t);
      jupiter_z_0+=     0.00001450672 * Math.cos( 1.17108416193 +      949.17560896980*t);
      jupiter_z_0+=     0.00000693095 * Math.cos( 5.14278041161 +      316.39186965660*t);
      jupiter_z_0+=     0.00000715042 * Math.cos( 1.41211197820 +      323.50541665740*t);
      jupiter_z_0+=     0.00000549720 * Math.cos( 4.84164274378 +      742.99006053260*t);
      jupiter_z_0+=     0.00000447831 * Math.cos( 4.60746588621 +     2118.76386037840*t);
      jupiter_z_0+=     0.00000543619 * Math.cos( 3.69636561822 +      515.46387109300*t);
      jupiter_z_0+=     0.00000483852 * Math.cos( 4.71796110160 +      735.87651353180*t);
      jupiter_z_0+=     0.00000365100 * Math.cos( 6.06065925437 +      206.18554843720*t);
      jupiter_z_0+=     0.00000288980 * Math.cos( 0.40266293090 +      525.75881183150*t);
      jupiter_z_0+=     0.00000254938 * Math.cos( 0.17978560944 +      543.91805909620*t);
      jupiter_z_0+=     0.00000195137 * Math.cos( 3.35374802237 +     1692.16566950240*t);
      jupiter_z_0+=     0.00000253254 * Math.cos( 3.57485315487 +      533.62311835770*t);
      jupiter_z_0+=     0.00000196691 * Math.cos( 2.65526923569 +      956.28915597060*t);
      jupiter_z_0+=     0.00000154379 * Math.cos( 1.47050669470 +      625.67019231240*t);
      jupiter_z_0+=     0.00000145972 * Math.cos( 5.96112903396 +      838.96928775040*t);
      jupiter_z_0+=     0.00000162371 * Math.cos( 3.12160596807 +     1581.95934828300*t);
      jupiter_z_0+=     0.00000135954 * Math.cos( 2.23721600610 +     1478.86657406440*t);
      jupiter_z_0+=     0.00000135376 * Math.cos( 4.03180075278 +     1265.56747862640*t);
      jupiter_z_0+=     0.00000118734 * Math.cos( 6.19132554294 +      532.87235883230*t);
      jupiter_z_0+=     0.00000121147 * Math.cos( 4.06252466827 +      526.50957135690*t);
      jupiter_z_0+=     0.00000113963 * Math.cos( 0.34443034869 +     1375.77379984580*t);
      jupiter_z_0+=     0.00000133095 * Math.cos( 1.61283648080 +       14.22709400160*t);

      let jupiter_z_1=0.0;
      jupiter_z_1+=     0.00407072175 * Math.cos( 1.52699353482 +      529.69096509460*t);
      jupiter_z_1+=     0.00020307341 * Math.cos( 2.59878269248 +     1059.38193018920*t);
      jupiter_z_1+=     0.00014424953 * Math.cos( 4.85400155025 +      536.80451209540*t);
      jupiter_z_1+=     0.00015474611 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_z_1+=     0.00012730364 * Math.cos( 5.45536715732 +      522.57741809380*t);
      jupiter_z_1+=     0.00002100882 * Math.cos( 0.09538864287 +        7.11354700080*t);
      jupiter_z_1+=     0.00001230425 * Math.cos( 3.14222500244 +     1589.07289528380*t);
      jupiter_z_1+=     0.00000760633 * Math.cos( 5.27867348162 +     1066.49547719000*t);
      jupiter_z_1+=     0.00000678832 * Math.cos( 4.74895422783 +     1052.26838318840*t);
      jupiter_z_1+=     0.00000597018 * Math.cos( 1.04748050782 +      110.20632121940*t);
      jupiter_z_1+=     0.00000570024 * Math.cos( 1.09418619361 +      103.09277421860*t);
      jupiter_z_1+=     0.00000473035 * Math.cos( 0.50552897171 +      426.59819087600*t);
      jupiter_z_1+=     0.00000435228 * Math.cos( 0.65531261911 +      419.48464387520*t);
      jupiter_z_1+=     0.00000351616 * Math.cos( 5.47690288047 +      515.46387109300*t);
      jupiter_z_1+=     0.00000345870 * Math.cos( 2.81172002142 +      632.78373931320*t);
      jupiter_z_1+=     0.00000211350 * Math.cos( 4.74646123972 +      543.91805909620*t);
      jupiter_z_1+=     0.00000180278 * Math.cos( 3.91041109061 +      735.87651353180*t);
      jupiter_z_1+=     0.00000164770 * Math.cos( 2.83487029931 +      949.17560896980*t);
      jupiter_z_1+=     0.00000196365 * Math.cos( 6.05289642814 +      323.50541665740*t);
      jupiter_z_1+=     0.00000129775 * Math.cos( 1.73448235766 +      206.18554843720*t);
      jupiter_z_1+=     0.00000167599 * Math.cos( 5.97044048706 +      316.39186965660*t);
      jupiter_z_1+=     0.00000104351 * Math.cos( 1.13016427121 +     1162.47470440780*t);
      jupiter_z_1=jupiter_z_1 * t;

      let jupiter_z_2=0.0;
      jupiter_z_2+=     0.00028635326 * Math.cos( 3.01374166973 +      529.69096509460*t);
      jupiter_z_2+=     0.00003114752 * Math.cos( 3.13228646176 +      536.80451209540*t);
      jupiter_z_2+=     0.00002379765 * Math.cos( 0.95574345340 +      522.57741809380*t);
      jupiter_z_2+=     0.00001310111 * Math.cos( 2.05263704913 +     1059.38193018920*t);
      jupiter_z_2+=     0.00000898757 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_z_2+=     0.00000305635 * Math.cos( 4.64213318439 +        7.11354700080*t);
      jupiter_z_2+=     0.00000178905 * Math.cos( 3.65482666103 +     1066.49547719000*t);
      jupiter_z_2+=     0.00000123283 * Math.cos( 0.96219015812 +      515.46387109300*t);
      jupiter_z_2+=     0.00000111363 * Math.cos( 0.51687136283 +     1052.26838318840*t);
      jupiter_z_2+=     0.00000116670 * Math.cos( 2.23097397584 +     1589.07289528380*t);
      jupiter_z_2=jupiter_z_2 * t * t;

      let jupiter_z_3=0.0;
      jupiter_z_3+=     0.00000964355 * Math.cos( 4.79228412032 +      529.69096509460*t);
      jupiter_z_3+=     0.00000443244 * Math.cos( 1.39969952998 +      536.80451209540*t);
      jupiter_z_3+=     0.00000295600 * Math.cos( 2.81281406373 +      522.57741809380*t);
      jupiter_z_3+=     0.00000112952 * Math.cos( 0.00000000000 +        0.00000000000*t);
      jupiter_z_3=jupiter_z_3 * t * t * t;

      return jupiter_z_0+jupiter_z_1+jupiter_z_2+jupiter_z_3;
   }

   static mars_x(t){
      let mars_x_0=0.0;
      mars_x_0+=     1.51769936383 * Math.cos( 6.20403346548 +     3340.61242669980*t);
      mars_x_0+=     0.19502945246 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_x_0+=     0.07070919655 * Math.cos( 0.25870338558 +     6681.22485339960*t);
      mars_x_0+=     0.00494196914 * Math.cos( 0.59669127768 +    10021.83728009940*t);
      mars_x_0+=     0.00040938237 * Math.cos( 0.93473307419 +    13362.44970679920*t);
      mars_x_0+=     0.00021067199 * Math.cos( 1.80435656154 +     3337.08930835080*t);
      mars_x_0+=     0.00021041626 * Math.cos( 1.17895619474 +     3344.13554504880*t);
      mars_x_0+=     0.00011370375 * Math.cos( 4.83265211109 +     1059.38193018920*t);
      mars_x_0+=     0.00013527976 * Math.cos( 0.63010765169 +      529.69096509460*t);
      mars_x_0+=     0.00006774107 * Math.cos( 3.61785048282 +     3340.59517304760*t);
      mars_x_0+=     0.00006774060 * Math.cos( 5.64862211431 +     3340.62968035200*t);
      mars_x_0+=     0.00008226069 * Math.cos( 1.86843519535 +     2281.23049651060*t);
      mars_x_0+=     0.00005469046 * Math.cos( 1.13324429003 +     2942.46342329160*t);
      mars_x_0+=     0.00004817134 * Math.cos( 1.85091045536 +     3738.76143010800*t);
      mars_x_0+=     0.00004937579 * Math.cos( 4.43241440654 +     5621.84292321040*t);
      mars_x_0+=     0.00005276260 * Math.cos( 2.33148083116 +     6151.53388830500*t);
      mars_x_0+=     0.00003636667 * Math.cos( 6.11397592106 +      796.29800681640*t);
      mars_x_0+=     0.00003725823 * Math.cos( 1.27280182943 +    16703.06213349900*t);
      mars_x_0+=     0.00003729746 * Math.cos( 1.21398323637 +      398.14900340820*t);
      mars_x_0+=     0.00002368513 * Math.cos( 2.96841895360 +     2544.31441988340*t);
      mars_x_0+=     0.00002397865 * Math.cos( 0.63553674054 +     3149.16416058820*t);
      mars_x_0+=     0.00002274646 * Math.cos( 2.35708328853 +     3532.06069281140*t);
      mars_x_0+=     0.00001977579 * Math.cos( 2.14087826110 +     6677.70173505060*t);
      mars_x_0+=     0.00002229176 * Math.cos( 1.69588962513 +     3340.54511639700*t);
      mars_x_0+=     0.00002229117 * Math.cos( 1.28739323821 +     3340.67973700260*t);
      mars_x_0+=     0.00002182206 * Math.cos( 1.69655112969 +     6283.07584999140*t);
      mars_x_0+=     0.00002241010 * Math.cos( 4.82218655311 +     8962.45534991020*t);
      mars_x_0+=     0.00001677693 * Math.cos( 3.14442612046 +     5884.92684658320*t);
      mars_x_0+=     0.00001630482 * Math.cos( 0.24117974845 +     4136.91043351620*t);
      mars_x_0+=     0.00001958162 * Math.cos( 1.51914544555 +     6684.74797174860*t);
      mars_x_0+=     0.00001378470 * Math.cos( 2.18011900021 +     1751.53953141600*t);
      mars_x_0+=     0.00001289804 * Math.cos( 4.70970778621 +     1194.44701022460*t);
      mars_x_0+=     0.00001468124 * Math.cos( 1.87869730543 +     3870.30339179440*t);
      mars_x_0+=     0.00001290170 * Math.cos( 0.43596325296 +     2810.92146160520*t);
      mars_x_0+=     0.00001572540 * Math.cos( 4.84809921789 +     1589.07289528380*t);
      mars_x_0+=     0.00000956752 * Math.cos( 5.36994227392 +      426.59819087600*t);
      mars_x_0+=     0.00000819458 * Math.cos( 5.15884167649 +     4399.99435688900*t);
      mars_x_0+=     0.00000708712 * Math.cos( 4.69562713369 +     5486.77784317500*t);
      mars_x_0+=     0.00000719048 * Math.cos( 2.91145340412 +      191.44826611160*t);
      mars_x_0+=     0.00000702848 * Math.cos( 4.67590003722 +     2146.16541647520*t);
      mars_x_0+=     0.00000720121 * Math.cos( 2.65539067862 +     9492.14631500480*t);
      mars_x_0+=     0.00000631186 * Math.cos( 3.95569679737 +     6681.20759974740*t);
      mars_x_0+=     0.00000631186 * Math.cos( 5.98646842887 +     6681.24210705180*t);
      mars_x_0+=     0.00000582287 * Math.cos( 3.95295967777 +     3185.19202726560*t);
      mars_x_0+=     0.00000709131 * Math.cos( 0.92869188035 +      213.29909543800*t);
      mars_x_0+=     0.00000555568 * Math.cos( 5.32014604077 +     3496.03282613400*t);
      mars_x_0+=     0.00000492190 * Math.cos( 2.17606530808 +     7079.37385680780*t);
      mars_x_0+=     0.00000535122 * Math.cos( 3.30310120139 +     1592.59601363280*t);
      mars_x_0+=     0.00000417652 * Math.cos( 5.30163601083 +     3341.59274776800*t);
      mars_x_0+=     0.00000417769 * Math.cos( 3.96482796919 +     3339.63210563160*t);
      mars_x_0+=     0.00000370752 * Math.cos( 5.08127148188 +     8432.76438481560*t);
      mars_x_0+=     0.00000360028 * Math.cos( 1.61089122901 +    20043.67456019880*t);
      mars_x_0+=     0.00000353036 * Math.cos( 3.88678429649 +     6254.62666252360*t);
      mars_x_0+=     0.00000352079 * Math.cos( 5.17043717929 +    12303.06777661000*t);
      mars_x_0+=     0.00000321578 * Math.cos( 1.94644283196 +     3553.91152213780*t);
      mars_x_0+=     0.00000346042 * Math.cos( 6.16404119331 +     5088.62883976680*t);
      mars_x_0+=     0.00000301924 * Math.cos( 0.98460899560 +     3127.31333126180*t);
      mars_x_0+=     0.00000287211 * Math.cos( 2.07531303415 +        7.11354700080*t);
      mars_x_0+=     0.00000307060 * Math.cos( 0.00966130243 +     1748.01641306700*t);
      mars_x_0+=     0.00000260116 * Math.cos( 1.89587348902 +     1990.74501704100*t);
      mars_x_0+=     0.00000313875 * Math.cos( 5.10651966600 +     4535.05943692440*t);
      mars_x_0+=     0.00000271815 * Math.cos( 1.94925691995 +     6467.92575796160*t);
      mars_x_0+=     0.00000223359 * Math.cos( 3.55354563068 +     3319.83703120740*t);
      mars_x_0+=     0.00000221615 * Math.cos( 5.71282076784 +     3361.38782219220*t);
      mars_x_0+=     0.00000234058 * Math.cos( 2.03750130921 +     9623.68827669120*t);
      mars_x_0+=     0.00000207708 * Math.cos( 2.03373205181 +     6681.15754309680*t);
      mars_x_0+=     0.00000205217 * Math.cos( 1.85790835685 +    10025.36039844840*t);
      mars_x_0+=     0.00000207851 * Math.cos( 2.47841996435 +    10018.31416175040*t);
      mars_x_0+=     0.00000253068 * Math.cos( 1.39828863887 +     2914.01423582380*t);
      mars_x_0+=     0.00000193257 * Math.cos( 4.93224646907 +     2118.76386037840*t);
      mars_x_0+=     0.00000218718 * Math.cos( 0.97547090194 +     6489.77658728800*t);
      mars_x_0+=     0.00000190381 * Math.cos( 1.28527355998 +     4690.47983635860*t);
      mars_x_0+=     0.00000207708 * Math.cos( 1.62523566496 +     6681.29216370240*t);
      mars_x_0+=     0.00000178814 * Math.cos( 2.54776084181 +     1221.84856632140*t);
      mars_x_0+=     0.00000157307 * Math.cos( 0.48852895157 +     2388.89402044920*t);
      mars_x_0+=     0.00000177177 * Math.cos( 4.27081023055 +     2957.71589447660*t);
      mars_x_0+=     0.00000147711 * Math.cos( 2.47588653124 +     7210.91581849420*t);
      mars_x_0+=     0.00000164710 * Math.cos( 0.57591122272 +     7477.52286021600*t);
      mars_x_0+=     0.00000153944 * Math.cos( 4.44473119432 +      639.89728631400*t);
      mars_x_0+=     0.00000168450 * Math.cos( 5.06929034077 +     3723.50895892300*t);
      mars_x_0+=     0.00000126166 * Math.cos( 2.64309008334 +     4292.33083295040*t);
      mars_x_0+=     0.00000161231 * Math.cos( 1.53118234358 +     1349.86740965880*t);
      mars_x_0+=     0.00000135146 * Math.cos( 0.12922395244 +     7903.07341972100*t);
      mars_x_0+=     0.00000146849 * Math.cos( 4.41614407590 +     3337.02199804800*t);
      mars_x_0+=     0.00000146211 * Math.cos( 4.84723563341 +     3344.20285535160*t);
      mars_x_0+=     0.00000166323 * Math.cos( 3.16905368032 +    10213.28554621100*t);
      mars_x_0+=     0.00000119425 * Math.cos( 4.65545643220 +    11773.37681151540*t);
      mars_x_0+=     0.00000144098 * Math.cos( 5.36305248386 +     2787.04302385740*t);
      mars_x_0+=     0.00000112328 * Math.cos( 0.07498207309 +     3205.54734666440*t);
      mars_x_0+=     0.00000118125 * Math.cos( 5.18570866097 +     4929.68532198360*t);
      mars_x_0+=     0.00000112305 * Math.cos( 3.45701462628 +     3333.49887969900*t);
      mars_x_0+=     0.00000106788 * Math.cos( 2.91050878748 +     3475.67750673520*t);
      mars_x_0+=     0.00000125116 * Math.cos( 3.97421380472 +     3894.18182954220*t);
      mars_x_0+=     0.00000120319 * Math.cos( 3.40966066157 +     9225.53927328300*t);
      mars_x_0+=     0.00000106515 * Math.cos( 5.50162815365 +      382.89653222320*t);
      mars_x_0+=     0.00000115240 * Math.cos( 5.86554297015 +      155.42039943420*t);

      let mars_x_1=0.0;
      mars_x_1+=     0.00861441374 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_x_1+=     0.00552437949 * Math.cos( 5.09565872891 +     6681.22485339960*t);
      mars_x_1+=     0.00077184977 * Math.cos( 5.43315636209 +    10021.83728009940*t);
      mars_x_1+=     0.00020467294 * Math.cos( 5.57051812369 +     3340.61242669980*t);
      mars_x_1+=     0.00009589581 * Math.cos( 5.77107234791 +    13362.44970679920*t);
      mars_x_1+=     0.00002620610 * Math.cos( 6.22441295122 +     3344.13554504880*t);
      mars_x_1+=     0.00002620537 * Math.cos( 3.04172154436 +     3337.08930835080*t);
      mars_x_1+=     0.00001163612 * Math.cos( 6.10909257097 +    16703.06213349900*t);
      mars_x_1+=     0.00000901178 * Math.cos( 3.31585548194 +     1059.38193018920*t);
      mars_x_1+=     0.00000427058 * Math.cos( 2.74008980166 +     2942.46342329160*t);
      mars_x_1+=     0.00000381428 * Math.cos( 0.22342431378 +     3738.76143010800*t);
      mars_x_1+=     0.00000386916 * Math.cos( 5.94232552612 +     5621.84292321040*t);
      mars_x_1+=     0.00000395001 * Math.cos( 0.20042939555 +     6684.74797174860*t);
      mars_x_1+=     0.00000337356 * Math.cos( 5.21417361076 +     3149.16416058820*t);
      mars_x_1+=     0.00000334209 * Math.cos( 2.45910275965 +     3185.19202726560*t);
      mars_x_1+=     0.00000318463 * Math.cos( 4.05140251894 +     3532.06069281140*t);
      mars_x_1+=     0.00000318426 * Math.cos( 0.52909208916 +     3496.03282613400*t);
      mars_x_1+=     0.00000312605 * Math.cos( 4.22912280613 +     2544.31441988340*t);
      mars_x_1+=     0.00000289251 * Math.cos( 4.61759345454 +      796.29800681640*t);
      mars_x_1+=     0.00000260308 * Math.cos( 5.02630754856 +     4136.91043351620*t);
      mars_x_1+=     0.00000206733 * Math.cos( 3.21083229673 +     1194.44701022460*t);
      mars_x_1+=     0.00000140570 * Math.cos( 0.16405101702 +    20043.67456019880*t);
      mars_x_1+=     0.00000159366 * Math.cos( 3.57762977582 +     1589.07289528380*t);
      mars_x_1+=     0.00000133819 * Math.cos( 4.64351814551 +     5884.92684658320*t);
      mars_x_1+=     0.00000132323 * Math.cos( 3.70094513425 +     4399.99435688900*t);
      mars_x_1+=     0.00000127123 * Math.cos( 2.81806076447 +     6677.70173505060*t);
      mars_x_1+=     0.00000102796 * Math.cos( 6.05672047566 +     5486.77784317500*t);
      mars_x_1+=     0.00000112591 * Math.cos( 5.89047647024 +     2146.16541647520*t);
      mars_x_1+=     0.00000129469 * Math.cos( 1.80477637958 +     1592.59601363280*t);
      mars_x_1+=     0.00000101457 * Math.cos( 3.72531913828 +     3341.59274776800*t);
      mars_x_1+=     0.00000101429 * Math.cos( 5.54115874275 +     3339.63210563160*t);
      mars_x_1=mars_x_1 * t;

      let mars_x_2=0.0;
      mars_x_2+=     0.00056323939 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_x_2+=     0.00022122528 * Math.cos( 3.54372113272 +     6681.22485339960*t);
      mars_x_2+=     0.00006091409 * Math.cos( 3.93272649649 +    10021.83728009940*t);
      mars_x_2+=     0.00001451998 * Math.cos( 3.64655666460 +     3340.61242669980*t);
      mars_x_2+=     0.00001130613 * Math.cos( 4.28827023222 +    13362.44970679920*t);
      mars_x_2+=     0.00000182610 * Math.cos( 4.63522660125 +    16703.06213349900*t);
      mars_x_2+=     0.00000168904 * Math.cos( 4.68797825494 +     3344.13554504880*t);
      mars_x_2+=     0.00000168384 * Math.cos( 4.57974326642 +     3337.08930835080*t);
      mars_x_2=mars_x_2 * t * t;

      let mars_x_3=0.0;
      mars_x_3+=     0.00000849999 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_x_3+=     0.00000560133 * Math.cos( 1.94007552058 +     6681.22485339960*t);
      mars_x_3+=     0.00000318062 * Math.cos( 2.39391695789 +    10021.83728009940*t);
      mars_x_3+=     0.00000113458 * Math.cos( 2.75680104109 +     3340.61242669980*t);
      mars_x_3=mars_x_3 * t * t * t;

      return mars_x_0+mars_x_1+mars_x_2+mars_x_3;
   }

   static mars_y(t){
      let mars_y_0=0.0;
      mars_y_0+=     1.51558976277 * Math.cos( 4.63212206588 +     3340.61242669980*t);
      mars_y_0+=     0.07064550239 * Math.cos( 4.97051892902 +     6681.22485339960*t);
      mars_y_0+=     0.08655481102 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_y_0+=     0.00493872848 * Math.cos( 5.30877806694 +    10021.83728009940*t);
      mars_y_0+=     0.00040917422 * Math.cos( 5.64698263703 +    13362.44970679920*t);
      mars_y_0+=     0.00021036784 * Math.cos( 0.23240270955 +     3337.08930835080*t);
      mars_y_0+=     0.00021012921 * Math.cos( 5.89022773653 +     3344.13554504880*t);
      mars_y_0+=     0.00011370034 * Math.cos( 3.26131408801 +     1059.38193018920*t);
      mars_y_0+=     0.00013324177 * Math.cos( 5.34259389724 +      529.69096509460*t);
      mars_y_0+=     0.00006764653 * Math.cos( 4.07671230062 +     3340.62968035200*t);
      mars_y_0+=     0.00006764700 * Math.cos( 2.04594066912 +     3340.59517304760*t);
      mars_y_0+=     0.00008346220 * Math.cos( 3.42464704002 +     2281.23049651060*t);
      mars_y_0+=     0.00005400042 * Math.cos( 5.81507793194 +     2942.46342329160*t);
      mars_y_0+=     0.00004809528 * Math.cos( 0.27875310553 +     3738.76143010800*t);
      mars_y_0+=     0.00004849523 * Math.cos( 2.85190987550 +     5621.84292321040*t);
      mars_y_0+=     0.00005263268 * Math.cos( 0.75811089992 +     6151.53388830500*t);
      mars_y_0+=     0.00003609527 * Math.cos( 4.53244488294 +      796.29800681640*t);
      mars_y_0+=     0.00003724293 * Math.cos( 5.98516013322 +    16703.06213349900*t);
      mars_y_0+=     0.00003805073 * Math.cos( 5.94234296399 +      398.14900340820*t);
      mars_y_0+=     0.00002394490 * Math.cos( 5.34678816191 +     3149.16416058820*t);
      mars_y_0+=     0.00002251027 * Math.cos( 0.76938193892 +     3532.06069281140*t);
      mars_y_0+=     0.00001975769 * Math.cos( 0.56949816579 +     6677.70173505060*t);
      mars_y_0+=     0.00002226030 * Math.cos( 5.99867316288 +     3340.67973700260*t);
      mars_y_0+=     0.00002226089 * Math.cos( 0.12398424247 +     3340.54511639700*t);
      mars_y_0+=     0.00002177591 * Math.cos( 0.12334436516 +     6283.07584999140*t);
      mars_y_0+=     0.00001690439 * Math.cos( 1.58331163985 +     5884.92684658320*t);
      mars_y_0+=     0.00002234121 * Math.cos( 3.24909113765 +     8962.45534991020*t);
      mars_y_0+=     0.00001628395 * Math.cos( 4.95250906888 +     4136.91043351620*t);
      mars_y_0+=     0.00001956411 * Math.cos( 6.23095843554 +     6684.74797174860*t);
      mars_y_0+=     0.00001697214 * Math.cos( 0.81869636263 +     2544.31441988340*t);
      mars_y_0+=     0.00001385946 * Math.cos( 3.73437191158 +     1751.53953141600*t);
      mars_y_0+=     0.00001439619 * Math.cos( 5.19505958438 +     2810.92146160520*t);
      mars_y_0+=     0.00001281890 * Math.cos( 3.13035275682 +     1194.44701022460*t);
      mars_y_0+=     0.00001469783 * Math.cos( 0.30415060688 +     3870.30339179440*t);
      mars_y_0+=     0.00001571880 * Math.cos( 3.27679498650 +     1589.07289528380*t);
      mars_y_0+=     0.00001575854 * Math.cos( 2.78266835243 +     5092.15195811580*t);
      mars_y_0+=     0.00000955007 * Math.cos( 3.80044052913 +      426.59819087600*t);
      mars_y_0+=     0.00000819149 * Math.cos( 3.58786440540 +     4399.99435688900*t);
      mars_y_0+=     0.00000709907 * Math.cos( 4.50556127152 +      191.44826611160*t);
      mars_y_0+=     0.00000719204 * Math.cos( 1.08354735050 +     9492.14631500480*t);
      mars_y_0+=     0.00000630626 * Math.cos( 2.38434217274 +     6681.20759974740*t);
      mars_y_0+=     0.00000630626 * Math.cos( 4.41511380423 +     6681.24210705180*t);
      mars_y_0+=     0.00000699407 * Math.cos( 5.71737497910 +      213.29909543800*t);
      mars_y_0+=     0.00000592563 * Math.cos( 2.82214112368 +     5486.77784317500*t);
      mars_y_0+=     0.00000581408 * Math.cos( 2.38087976114 +     3185.19202726560*t);
      mars_y_0+=     0.00000551361 * Math.cos( 3.73720813913 +     3496.03282613400*t);
      mars_y_0+=     0.00000491736 * Math.cos( 0.60462673907 +     7079.37385680780*t);
      mars_y_0+=     0.00000403176 * Math.cos( 3.49532014869 +     8432.76438481560*t);
      mars_y_0+=     0.00000532702 * Math.cos( 1.72629618682 +     1592.59601363280*t);
      mars_y_0+=     0.00000417187 * Math.cos( 2.39288855164 +     3339.63210563160*t);
      mars_y_0+=     0.00000417083 * Math.cos( 3.72975291794 +     3341.59274776800*t);
      mars_y_0+=     0.00000392731 * Math.cos( 1.39110771836 +     2146.16541647520*t);
      mars_y_0+=     0.00000359894 * Math.cos( 0.04010740278 +    20043.67456019880*t);
      mars_y_0+=     0.00000352248 * Math.cos( 2.32029465959 +     6254.62666252360*t);
      mars_y_0+=     0.00000351559 * Math.cos( 3.59860692655 +    12303.06777661000*t);
      mars_y_0+=     0.00000321064 * Math.cos( 0.37146017150 +     3553.91152213780*t);
      mars_y_0+=     0.00000313108 * Math.cos( 5.61766202779 +     3127.31333126180*t);
      mars_y_0+=     0.00000266755 * Math.cos( 2.88006209994 +     4562.46099302120*t);
      mars_y_0+=     0.00000281855 * Math.cos( 0.42150291554 +        7.11354700080*t);
      mars_y_0+=     0.00000259253 * Math.cos( 0.32102915510 +     1990.74501704100*t);
      mars_y_0+=     0.00000313501 * Math.cos( 3.53468286874 +     4535.05943692440*t);
      mars_y_0+=     0.00000265807 * Math.cos( 4.13657205734 +     5088.62883976680*t);
      mars_y_0+=     0.00000271152 * Math.cos( 0.37550883198 +     6467.92575796160*t);
      mars_y_0+=     0.00000223029 * Math.cos( 1.98134328602 +     3319.83703120740*t);
      mars_y_0+=     0.00000221308 * Math.cos( 4.14094711258 +     3361.38782219220*t);
      mars_y_0+=     0.00000233740 * Math.cos( 0.46548637345 +     9623.68827669120*t);
      mars_y_0+=     0.00000212622 * Math.cos( 2.22578594563 +     1748.01641306700*t);
      mars_y_0+=     0.00000207526 * Math.cos( 0.46238962685 +     6681.15754309680*t);
      mars_y_0+=     0.00000205079 * Math.cos( 0.28680735926 +    10025.36039844840*t);
      mars_y_0+=     0.00000207717 * Math.cos( 0.90733952000 +    10018.31416175040*t);
      mars_y_0+=     0.00000193140 * Math.cos( 3.36083067358 +     2118.76386037840*t);
      mars_y_0+=     0.00000244575 * Math.cos( 2.80556071941 +     2914.01423582380*t);
      mars_y_0+=     0.00000218542 * Math.cos( 5.68744233165 +     6489.77658728800*t);
      mars_y_0+=     0.00000207526 * Math.cos( 0.05389324000 +     6681.29216370240*t);
      mars_y_0+=     0.00000178369 * Math.cos( 4.10543898205 +     1221.84856632140*t);
      mars_y_0+=     0.00000156876 * Math.cos( 5.19786609301 +     2388.89402044920*t);
      mars_y_0+=     0.00000146513 * Math.cos( 5.54868179527 +     4690.47983635860*t);
      mars_y_0+=     0.00000176877 * Math.cos( 2.69854646339 +     2957.71589447660*t);
      mars_y_0+=     0.00000147659 * Math.cos( 0.90344856519 +     7210.91581849420*t);
      mars_y_0+=     0.00000164583 * Math.cos( 5.28781848597 +     7477.52286021600*t);
      mars_y_0+=     0.00000153824 * Math.cos( 2.87500720379 +      639.89728631400*t);
      mars_y_0+=     0.00000148488 * Math.cos( 3.34244341315 +     3723.50895892300*t);
      mars_y_0+=     0.00000146666 * Math.cos( 2.84397856099 +     3337.02199804800*t);
      mars_y_0+=     0.00000166545 * Math.cos( 1.59865996295 +    10213.28554621100*t);
      mars_y_0+=     0.00000146054 * Math.cos( 3.27515242640 +     3344.20285535160*t);
      mars_y_0+=     0.00000123680 * Math.cos( 2.52811225465 +     7903.07341972100*t);
      mars_y_0+=     0.00000120116 * Math.cos( 3.09142091867 +    11773.37681151540*t);
      mars_y_0+=     0.00000132007 * Math.cos( 3.42890155754 +     1349.86740965880*t);
      mars_y_0+=     0.00000143810 * Math.cos( 3.78998571160 +     2787.04302385740*t);
      mars_y_0+=     0.00000115489 * Math.cos( 1.95561523091 +     3333.49887969900*t);
      mars_y_0+=     0.00000111935 * Math.cos( 4.78148495483 +     3205.54734666440*t);
      mars_y_0+=     0.00000118091 * Math.cos( 3.61471499659 +     4929.68532198360*t);
      mars_y_0+=     0.00000106593 * Math.cos( 1.33768476661 +     3475.67750673520*t);
      mars_y_0+=     0.00000120156 * Math.cos( 1.83813184657 +     9225.53927328300*t);
      mars_y_0+=     0.00000104155 * Math.cos( 0.75138682237 +     4292.33083295040*t);
      mars_y_0+=     0.00000103341 * Math.cos( 0.82609816627 +      382.89653222320*t);
      mars_y_0+=     0.00000110471 * Math.cos( 1.21942577303 +      155.42039943420*t);
      mars_y_0+=     0.00000114691 * Math.cos( 2.26053594900 +     3894.18182954220*t);

      let mars_y_1=0.0;
      mars_y_1+=     0.01427324210 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_y_1+=     0.00551063753 * Math.cos( 3.52128320402 +     6681.22485339960*t);
      mars_y_1+=     0.00077091913 * Math.cos( 3.86082685753 +    10021.83728009940*t);
      mars_y_1+=     0.00037310491 * Math.cos( 1.16016958445 +     3340.61242669980*t);
      mars_y_1+=     0.00009582122 * Math.cos( 4.19942354479 +    13362.44970679920*t);
      mars_y_1+=     0.00002617695 * Math.cos( 1.47284555520 +     3337.08930835080*t);
      mars_y_1+=     0.00002611572 * Math.cos( 4.65030772498 +     3344.13554504880*t);
      mars_y_1+=     0.00001162955 * Math.cos( 4.53778503576 +    16703.06213349900*t);
      mars_y_1+=     0.00000900678 * Math.cos( 1.74256260709 +     1059.38193018920*t);
      mars_y_1+=     0.00000431990 * Math.cos( 1.20122419783 +     2942.46342329160*t);
      mars_y_1+=     0.00000389982 * Math.cos( 4.38779713561 +     5621.84292321040*t);
      mars_y_1+=     0.00000380122 * Math.cos( 4.93073729444 +     3738.76143010800*t);
      mars_y_1+=     0.00000394355 * Math.cos( 4.91119397796 +     6684.74797174860*t);
      mars_y_1+=     0.00000336661 * Math.cos( 3.63990879619 +     3149.16416058820*t);
      mars_y_1+=     0.00000333604 * Math.cos( 0.88647104051 +     3185.19202726560*t);
      mars_y_1+=     0.00000318324 * Math.cos( 2.48122345477 +     3532.06069281140*t);
      mars_y_1+=     0.00000316743 * Math.cos( 5.23316524269 +     3496.03282613400*t);
      mars_y_1+=     0.00000311468 * Math.cos( 2.66149474204 +     2544.31441988340*t);
      mars_y_1+=     0.00000283006 * Math.cos( 3.01270555394 +      796.29800681640*t);
      mars_y_1+=     0.00000259715 * Math.cos( 3.45285007540 +     4136.91043351620*t);
      mars_y_1+=     0.00000204277 * Math.cos( 1.62196956205 +     1194.44701022460*t);
      mars_y_1+=     0.00000140506 * Math.cos( 4.87611060370 +    20043.67456019880*t);
      mars_y_1+=     0.00000159094 * Math.cos( 2.00474963161 +     1589.07289528380*t);
      mars_y_1+=     0.00000133054 * Math.cos( 3.06497749499 +     5884.92684658320*t);
      mars_y_1+=     0.00000132221 * Math.cos( 2.12903733409 +     4399.99435688900*t);
      mars_y_1+=     0.00000126748 * Math.cos( 1.25031299906 +     6677.70173505060*t);
      mars_y_1+=     0.00000103023 * Math.cos( 4.48653117588 +     5486.77784317500*t);
      mars_y_1+=     0.00000128526 * Math.cos( 0.22328095820 +     1592.59601363280*t);
      mars_y_1+=     0.00000101352 * Math.cos( 3.97061208738 +     3339.63210563160*t);
      mars_y_1+=     0.00000101253 * Math.cos( 2.15203295056 +     3341.59274776800*t);
      mars_y_1=mars_y_1 * t;

      let mars_y_2=0.0;
      mars_y_2+=     0.00035396765 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_y_2+=     0.00021950759 * Math.cos( 1.96291594946 +     6681.22485339960*t);
      mars_y_2+=     0.00006075990 * Math.cos( 2.35864321001 +    10021.83728009940*t);
      mars_y_2+=     0.00002571425 * Math.cos( 5.64795745327 +     3340.61242669980*t);
      mars_y_2+=     0.00001129099 * Math.cos( 2.71576248963 +    13362.44970679920*t);
      mars_y_2+=     0.00000182443 * Math.cos( 3.06335050462 +    16703.06213349900*t);
      mars_y_2+=     0.00000168357 * Math.cos( 3.01017878073 +     3337.08930835080*t);
      mars_y_2+=     0.00000167747 * Math.cos( 3.10922702911 +     3344.13554504880*t);
      mars_y_2=mars_y_2 * t * t;

      let mars_y_3=0.0;
      mars_y_3+=     0.00001448778 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_y_3+=     0.00000548277 * Math.cos( 0.33360423382 +     6681.22485339960*t);
      mars_y_3+=     0.00000316422 * Math.cos( 0.81609547752 +    10021.83728009940*t);
      mars_y_3+=     0.00000121864 * Math.cos( 4.21281448757 +     3340.61242669980*t);
      mars_y_3=mars_y_3 * t * t * t;

      return mars_y_0+mars_y_1+mars_y_2+mars_y_3;
   }

   static mars_z(t){
      let mars_z_0=0.0;
      mars_z_0+=     0.04901207220 * Math.cos( 3.76712324286 +     3340.61242669980*t);
      mars_z_0+=     0.00660669541 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_z_0+=     0.00228333904 * Math.cos( 4.10544022266 +     6681.22485339960*t);
      mars_z_0+=     0.00015958402 * Math.cos( 4.44367058261 +    10021.83728009940*t);
      mars_z_0+=     0.00001321976 * Math.cos( 4.78186604114 +    13362.44970679920*t);
      mars_z_0+=     0.00000679660 * Math.cos( 5.65109977813 +     3337.08930835080*t);
      mars_z_0+=     0.00000679219 * Math.cos( 5.02527030899 +     3344.13554504880*t);
      mars_z_0+=     0.00000531140 * Math.cos( 3.86748390045 +     2281.23049651060*t);
      mars_z_0+=     0.00000374993 * Math.cos( 4.33338216773 +      529.69096509460*t);
      mars_z_0+=     0.00000325315 * Math.cos( 2.24562508217 +     1059.38193018920*t);
      mars_z_0+=     0.00000218762 * Math.cos( 1.18094849702 +     3340.59517304760*t);
      mars_z_0+=     0.00000218761 * Math.cos( 3.21172012852 +     3340.62968035200*t);
      mars_z_0+=     0.00000152333 * Math.cos( 6.08109566130 +     6151.53388830500*t);
      mars_z_0+=     0.00000146631 * Math.cos( 5.09927022855 +      398.14900340820*t);
      mars_z_0+=     0.00000152443 * Math.cos( 2.13254535850 +     5621.84292321040*t);
      mars_z_0+=     0.00000120328 * Math.cos( 5.12010663983 +    16703.06213349900*t);
      mars_z_0+=     0.00000126016 * Math.cos( 3.67803475473 +      796.29800681640*t);
      mars_z_0+=     0.00000116766 * Math.cos( 4.86913583010 +     2942.46342329160*t);
      mars_z_0+=     0.00000112925 * Math.cos( 5.76548397681 +     3738.76143010800*t);

      let mars_z_1=0.0;
      mars_z_1+=     0.00331842958 * Math.cos( 6.05027773492 +     3340.61242669980*t);
      mars_z_1+=     0.00047930411 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_z_1+=     0.00009896501 * Math.cos( 1.61155844715 +     6681.22485339960*t);
      mars_z_1+=     0.00001700147 * Math.cos( 2.63703242065 +    10021.83728009940*t);
      mars_z_1+=     0.00000240176 * Math.cos( 3.12712303414 +    13362.44970679920*t);
      mars_z_1+=     0.00000114908 * Math.cos( 0.95987621952 +     3337.08930835080*t);
      mars_z_1=mars_z_1 * t;

      let mars_z_2=0.0;
      mars_z_2+=     0.00013705360 * Math.cos( 1.04212852598 +     3340.61242669980*t);
      mars_z_2+=     0.00005931596 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mars_z_2+=     0.00000716728 * Math.cos( 0.12154825255 +     6681.22485339960*t);
      mars_z_2+=     0.00000138514 * Math.cos( 0.78090653399 +    10021.83728009940*t);
      mars_z_2=mars_z_2 * t * t;

      let mars_z_3=0.0;
      mars_z_3+=     0.00000489822 * Math.cos( 2.06392886831 +     3340.61242669980*t);
      mars_z_3+=     0.00000212575 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mars_z_3=mars_z_3 * t * t * t;

      return mars_z_0+mars_z_1+mars_z_2+mars_z_3;
   }

   static mercury_x(t){
      let mercury_x_0=0.0;
      mercury_x_0+=     0.37546291728 * Math.cos( 4.39651506942 +    26087.90314157420*t);
      mercury_x_0+=     0.03825746672 * Math.cos( 1.16485604339 +    52175.80628314840*t);
      mercury_x_0+=     0.02625615963 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mercury_x_0+=     0.00584261333 * Math.cos( 4.21599394757 +    78263.70942472259*t);
      mercury_x_0+=     0.00105716695 * Math.cos( 0.98379033182 +   104351.61256629678*t);
      mercury_x_0+=     0.00021011730 * Math.cos( 4.03469353923 +   130439.51570787099*t);
      mercury_x_0+=     0.00004433373 * Math.cos( 0.80236674527 +   156527.41884944518*t);
      mercury_x_0+=     0.00000974967 * Math.cos( 3.85319674536 +   182615.32199101939*t);
      mercury_x_0+=     0.00000700327 * Math.cos( 4.45478725367 +    24978.52458948080*t);
      mercury_x_0+=     0.00000626468 * Math.cos( 1.18563492001 +    27197.28169366760*t);
      mercury_x_0+=     0.00000446989 * Math.cos( 2.97507181503 +     1059.38193018920*t);
      mercury_x_0+=     0.00000398401 * Math.cos( 1.86487895049 +    20426.57109242200*t);
      mercury_x_0+=     0.00000277216 * Math.cos( 3.77909548342 +    31749.23519072640*t);
      mercury_x_0+=     0.00000190657 * Math.cos( 4.27201801941 +    53285.18483524180*t);
      mercury_x_0+=     0.00000181790 * Math.cos( 4.94857138217 +     1109.37855209340*t);
      mercury_x_0+=     0.00000194418 * Math.cos( 0.67806013045 +     4551.95349705880*t);
      mercury_x_0+=     0.00000221028 * Math.cos( 0.62082250658 +   208703.22513259358*t);
      mercury_x_0+=     0.00000190713 * Math.cos( 1.17385212686 +     5661.33204915220*t);
      mercury_x_0+=     0.00000138492 * Math.cos( 1.22446421973 +    51066.42773105500*t);
      mercury_x_0+=     0.00000151693 * Math.cos( 2.67604566886 +    51116.42435295920*t);
      mercury_x_0+=     0.00000114338 * Math.cos( 0.56002737806 +    57837.13833230060*t);

      let mercury_x_1=0.0;
      mercury_x_1+=     0.00318848034 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mercury_x_1+=     0.00105289019 * Math.cos( 5.91600475006 +    52175.80628314840*t);
      mercury_x_1+=     0.00032316001 * Math.cos( 2.68247273347 +    78263.70942472259*t);
      mercury_x_1+=     0.00011992889 * Math.cos( 5.81575112963 +    26087.90314157420*t);
      mercury_x_1+=     0.00008783200 * Math.cos( 5.73285747425 +   104351.61256629678*t);
      mercury_x_1+=     0.00002329042 * Math.cos( 2.50023793407 +   130439.51570787099*t);
      mercury_x_1+=     0.00000614473 * Math.cos( 5.55087602844 +   156527.41884944518*t);
      mercury_x_1+=     0.00000162192 * Math.cos( 2.31836529248 +   182615.32199101939*t);
      mercury_x_1=mercury_x_1 * t;

      let mercury_x_2=0.0;
      mercury_x_2+=     0.00001484185 * Math.cos( 4.35401210269 +    52175.80628314840*t);
      mercury_x_2+=     0.00000907467 * Math.cos( 1.13216343018 +    78263.70942472259*t);
      mercury_x_2+=     0.00001214995 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mercury_x_2+=     0.00000368809 * Math.cos( 4.18705944126 +   104351.61256629678*t);
      mercury_x_2+=     0.00000254306 * Math.cos( 4.12817377140 +    26087.90314157420*t);
      mercury_x_2+=     0.00000130149 * Math.cos( 0.95681684789 +   130439.51570787099*t);
      mercury_x_2=mercury_x_2 * t * t;

      return mercury_x_0+mercury_x_1+mercury_x_2;
   }

   static mercury_y(t){
      let mercury_y_0=0.0;
      mercury_y_0+=     0.37953642888 * Math.cos( 2.83780617820 +    26087.90314157420*t);
      mercury_y_0+=     0.11626131831 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mercury_y_0+=     0.03854668215 * Math.cos( 5.88780608966 +    52175.80628314840*t);
      mercury_y_0+=     0.00587711268 * Math.cos( 2.65498896201 +    78263.70942472259*t);
      mercury_y_0+=     0.00106235493 * Math.cos( 5.70550616735 +   104351.61256629678*t);
      mercury_y_0+=     0.00021100828 * Math.cos( 2.47291315849 +   130439.51570787099*t);
      mercury_y_0+=     0.00004450056 * Math.cos( 5.52354907071 +   156527.41884944518*t);
      mercury_y_0+=     0.00000978286 * Math.cos( 2.29102643026 +   182615.32199101939*t);
      mercury_y_0+=     0.00000707500 * Math.cos( 2.89516591531 +    24978.52458948080*t);
      mercury_y_0+=     0.00000654742 * Math.cos( 5.92892123881 +    27197.28169366760*t);
      mercury_y_0+=     0.00000448561 * Math.cos( 1.40595042211 +     1059.38193018920*t);
      mercury_y_0+=     0.00000402168 * Math.cos( 0.30317998006 +    20426.57109242200*t);
      mercury_y_0+=     0.00000290604 * Math.cos( 2.23645868392 +    31749.23519072640*t);
      mercury_y_0+=     0.00000191358 * Math.cos( 2.70792842547 +    53285.18483524180*t);
      mercury_y_0+=     0.00000181119 * Math.cos( 0.23941291054 +     1109.37855209340*t);
      mercury_y_0+=     0.00000193372 * Math.cos( 5.38698781997 +     4551.95349705880*t);
      mercury_y_0+=     0.00000221718 * Math.cos( 5.34170676570 +   208703.22513259358*t);
      mercury_y_0+=     0.00000139514 * Math.cos( 5.94698662319 +    51066.42773105500*t);
      mercury_y_0+=     0.00000154924 * Math.cos( 1.12201865761 +    51116.42435295920*t);
      mercury_y_0+=     0.00000177242 * Math.cos( 2.78855813429 +     5661.33204915220*t);
      mercury_y_0+=     0.00000116072 * Math.cos( 5.28608170116 +    57837.13833230060*t);

      let mercury_y_1=0.0;
      mercury_y_1+=     0.00107803852 * Math.cos( 4.34964793883 +    52175.80628314840*t);
      mercury_y_1+=     0.00080651544 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mercury_y_1+=     0.00032715354 * Math.cos( 1.11763734425 +    78263.70942472259*t);
      mercury_y_1+=     0.00008858158 * Math.cos( 4.16852401867 +   104351.61256629678*t);
      mercury_y_1+=     0.00011914709 * Math.cos( 1.22139986340 +    26087.90314157420*t);
      mercury_y_1+=     0.00002344469 * Math.cos( 0.93615372641 +   130439.51570787099*t);
      mercury_y_1+=     0.00000617838 * Math.cos( 3.98693992284 +   156527.41884944518*t);
      mercury_y_1+=     0.00000162955 * Math.cos( 0.75452718043 +   182615.32199101939*t);
      mercury_y_1=mercury_y_1 * t;

      let mercury_y_2=0.0;
      mercury_y_2+=     0.00004612157 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mercury_y_2+=     0.00001575670 * Math.cos( 2.81172733349 +    52175.80628314840*t);
      mercury_y_2+=     0.00000927896 * Math.cos( 5.85368769122 +    78263.70942472259*t);
      mercury_y_2+=     0.00000670255 * Math.cos( 0.90964509090 +    26087.90314157420*t);
      mercury_y_2+=     0.00000373744 * Math.cos( 2.62279275699 +   104351.61256629678*t);
      mercury_y_2+=     0.00000131389 * Math.cos( 5.67519052208 +   130439.51570787099*t);
      mercury_y_2=mercury_y_2 * t * t;

      return mercury_y_0+mercury_y_1+mercury_y_2;
   }

   static mercury_z(t){
      let mercury_z_0=0.0;
      mercury_z_0+=     0.04607665326 * Math.cos( 1.99295081967 +    26087.90314157420*t);
      mercury_z_0+=     0.00708734365 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mercury_z_0+=     0.00469171617 * Math.cos( 5.04215742764 +    52175.80628314840*t);
      mercury_z_0+=     0.00071626395 * Math.cos( 1.80894256071 +    78263.70942472259*t);
      mercury_z_0+=     0.00012957446 * Math.cos( 4.85922032010 +   104351.61256629678*t);
      mercury_z_0+=     0.00002575002 * Math.cos( 1.62646731545 +   130439.51570787099*t);
      mercury_z_0+=     0.00000543259 * Math.cos( 4.67698860167 +   156527.41884944518*t);
      mercury_z_0+=     0.00000119462 * Math.cos( 1.44437994097 +   182615.32199101939*t);

      let mercury_z_1=0.0;
      mercury_z_1+=     0.00108722177 * Math.cos( 3.91134750825 +    26087.90314157420*t);
      mercury_z_1+=     0.00057826621 * Math.cos( 3.14159265359 +        0.00000000000*t);
      mercury_z_1+=     0.00004297352 * Math.cos( 2.56373047177 +    52175.80628314840*t);
      mercury_z_1+=     0.00002435833 * Math.cos( 0.05112640506 +    78263.70942472259*t);
      mercury_z_1+=     0.00000795699 * Math.cos( 3.20041081922 +   104351.61256629678*t);
      mercury_z_1+=     0.00000229251 * Math.cos( 0.00558431110 +   130439.51570787099*t);
      mercury_z_1=mercury_z_1 * t;

      let mercury_z_2=0.0;
      mercury_z_2+=     0.00001053118 * Math.cos( 5.37979214357 +    26087.90314157420*t);
      mercury_z_2+=     0.00001185024 * Math.cos( 0.00000000000 +        0.00000000000*t);
      mercury_z_2=mercury_z_2 * t * t;

      return mercury_z_0+mercury_z_1+mercury_z_2;
   }

   static neptune_x(t){
      let neptune_x_0=0.0;
      neptune_x_0+=    30.05890004476 * Math.cos( 5.31211340029 +       38.13303563780*t);
      neptune_x_0+=     0.27080164222 * Math.cos( 3.14159265359 +        0.00000000000*t);
      neptune_x_0+=     0.13505661755 * Math.cos( 3.50078975634 +       76.26607127560*t);
      neptune_x_0+=     0.15726094556 * Math.cos( 0.11319072675 +       36.64856292950*t);
      neptune_x_0+=     0.14935120126 * Math.cos( 1.08499403018 +       39.61750834610*t);
      neptune_x_0+=     0.02597313814 * Math.cos( 1.99590301412 +        1.48447270830*t);
      neptune_x_0+=     0.01074040708 * Math.cos( 5.38502938672 +       74.78159856730*t);
      neptune_x_0+=     0.00823793287 * Math.cos( 1.43221581862 +       35.16409022120*t);
      neptune_x_0+=     0.00817588813 * Math.cos( 0.78180174031 +        2.96894541660*t);
      neptune_x_0+=     0.00565534918 * Math.cos( 5.98964907613 +       41.10198105440*t);
      neptune_x_0+=     0.00495719107 * Math.cos( 0.59948143567 +      529.69096509460*t);
      neptune_x_0+=     0.00307525907 * Math.cos( 0.40023311011 +       73.29712585900*t);
      neptune_x_0+=     0.00272253551 * Math.cos( 0.87443494387 +      213.29909543800*t);
      neptune_x_0+=     0.00135887219 * Math.cos( 5.54676577816 +       77.75054398390*t);
      neptune_x_0+=     0.00090965704 * Math.cos( 1.68910246115 +      114.39910691340*t);
      neptune_x_0+=     0.00069040539 * Math.cos( 5.83469123520 +        4.45341812490*t);
      neptune_x_0+=     0.00060813556 * Math.cos( 2.62589958380 +       33.67961751290*t);
      neptune_x_0+=     0.00054690827 * Math.cos( 1.55799996661 +       71.81265315070*t);
      neptune_x_0+=     0.00028889260 * Math.cos( 4.78966826027 +       42.58645376270*t);
      neptune_x_0+=     0.00012614732 * Math.cos( 3.57002516434 +      112.91463420510*t);
      neptune_x_0+=     0.00012749153 * Math.cos( 2.73719269645 +      111.43016149680*t);
      neptune_x_0+=     0.00012013994 * Math.cos( 0.94912933496 +     1059.38193018920*t);
      neptune_x_0+=     0.00007540650 * Math.cos( 2.77783477855 +       70.32818044240*t);
      neptune_x_0+=     0.00007573383 * Math.cos( 0.10011329853 +      426.59819087600*t);
      neptune_x_0+=     0.00008004318 * Math.cos( 1.63965626260 +      108.46121608020*t);
      neptune_x_0+=     0.00006464842 * Math.cos( 4.62580066013 +        5.93789083320*t);
      neptune_x_0+=     0.00005565860 * Math.cos( 3.82502185953 +       32.19514480460*t);
      neptune_x_0+=     0.00004654361 * Math.cos( 0.10385887980 +       37.61177077600*t);
      neptune_x_0+=     0.00004732434 * Math.cos( 4.09723977191 +       79.23501669220*t);
      neptune_x_0+=     0.00004557247 * Math.cos( 1.09712669317 +       38.65430049960*t);
      neptune_x_0+=     0.00004322550 * Math.cos( 2.37744780188 +       38.08485152800*t);
      neptune_x_0+=     0.00004315539 * Math.cos( 5.10473142056 +       38.18121974760*t);
      neptune_x_0+=     0.00004089036 * Math.cos( 1.99429048244 +       37.16982779130*t);
      neptune_x_0+=     0.00004249674 * Math.cos( 5.63324475823 +       28.57180808220*t);
      neptune_x_0+=     0.00003920412 * Math.cos( 5.49263784865 +       39.09624348430*t);
      neptune_x_0+=     0.00003951848 * Math.cos( 2.29996934110 +       98.89998852460*t);
      neptune_x_0+=     0.00003322735 * Math.cos( 4.68798591938 +        4.19278569400*t);
      neptune_x_0+=     0.00003108292 * Math.cos( 1.84434543409 +       47.69426319340*t);
      neptune_x_0+=     0.00003260095 * Math.cos( 1.81839652878 +      145.10977900970*t);
      neptune_x_0+=     0.00002723442 * Math.cos( 3.82296285941 +      109.94568878850*t);
      neptune_x_0+=     0.00002522938 * Math.cos( 4.66296126912 +      312.19908396260*t);
      neptune_x_0+=     0.00001887430 * Math.cos( 3.20485417792 +       35.68535508300*t);
      neptune_x_0+=     0.00001648985 * Math.cos( 4.06990666591 +       30.05628079050*t);
      neptune_x_0+=     0.00001826700 * Math.cos( 3.58024318649 +       44.07092647100*t);
      neptune_x_0+=     0.00001945462 * Math.cos( 4.15326825288 +      206.18554843720*t);
      neptune_x_0+=     0.00001681255 * Math.cos( 4.27560304282 +       40.58071619260*t);
      neptune_x_0+=     0.00001533383 * Math.cos( 1.17732211665 +       38.02116105320*t);
      neptune_x_0+=     0.00001891892 * Math.cos( 0.74998855536 +      220.41264243880*t);
      neptune_x_0+=     0.00001527526 * Math.cos( 0.02173640246 +       38.24491022240*t);
      neptune_x_0+=     0.00002084477 * Math.cos( 1.56821671369 +      149.56319713460*t);
      neptune_x_0+=     0.00002083682 * Math.cos( 2.83676961811 +      137.03302416240*t);
      neptune_x_0+=     0.00001615063 * Math.cos( 2.91063835010 +      106.97674337190*t);
      neptune_x_0+=     0.00001265797 * Math.cos( 3.42037275447 +       46.20979048510*t);
      neptune_x_0+=     0.00001560429 * Math.cos( 0.55865739143 +       37.87240320690*t);
      neptune_x_0+=     0.00001545705 * Math.cos( 0.64028780672 +       38.39366806870*t);
      neptune_x_0+=     0.00001434798 * Math.cos( 0.72658718863 +      522.57741809380*t);
      neptune_x_0+=     0.00001271543 * Math.cos( 2.74412981229 +       33.94024994380*t);
      neptune_x_0+=     0.00001407422 * Math.cos( 3.61743288666 +      536.80451209540*t);
      neptune_x_0+=     0.00001387922 * Math.cos( 3.71814330952 +      115.88357962170*t);
      neptune_x_0+=     0.00001228939 * Math.cos( 2.78878211792 +       72.07328558160*t);
      neptune_x_0+=     0.00001448439 * Math.cos( 1.98814317259 +      181.75834193920*t);
      neptune_x_0+=     0.00001170078 * Math.cos( 3.98594689041 +        8.07675484730*t);
      neptune_x_0+=     0.00001080795 * Math.cos( 4.75485636019 +       42.32582133180*t);
      neptune_x_0+=     0.00001220341 * Math.cos( 2.64791449584 +      148.07872442630*t);
      neptune_x_0+=     0.00000942722 * Math.cos( 3.99861076677 +       68.84370773410*t);
      neptune_x_0+=     0.00000722013 * Math.cos( 6.16811781566 +      152.53214255120*t);
      neptune_x_0+=     0.00000608265 * Math.cos( 4.49563700854 +       35.21227433100*t);
      neptune_x_0+=     0.00000714969 * Math.cos( 3.09121631507 +      143.62530630140*t);
      neptune_x_0+=     0.00000633834 * Math.cos( 3.41692648170 +        7.42236354150*t);
      neptune_x_0+=     0.00000554473 * Math.cos( 2.98634397776 +       41.05379694460*t);
      neptune_x_0+=     0.00000566306 * Math.cos( 5.02809882280 +       30.71067209630*t);
      neptune_x_0+=     0.00000679542 * Math.cos( 2.15673681356 +      218.40690486870*t);
      neptune_x_0+=     0.00000463140 * Math.cos( 2.74436643796 +       31.54075349880*t);
      neptune_x_0+=     0.00000451619 * Math.cos( 4.62757040522 +       44.72531777680*t);
      neptune_x_0+=     0.00000528038 * Math.cos( 0.34505105111 +        0.96320784650*t);
      neptune_x_0+=     0.00000439638 * Math.cos( 1.29678048299 +     1589.07289528380*t);
      neptune_x_0+=     0.00000406092 * Math.cos( 5.51084213663 +        6.59228213900*t);
      neptune_x_0+=     0.00000493231 * Math.cos( 3.82613187047 +      146.59425171800*t);
      neptune_x_0+=     0.00000306843 * Math.cos( 2.62651223895 +       60.76695288680*t);
      neptune_x_0+=     0.00000405411 * Math.cos( 5.31947629009 +       31.01948863700*t);
      neptune_x_0+=     0.00000337082 * Math.cos( 1.72339969429 +        0.52126486180*t);
      neptune_x_0+=     0.00000346164 * Math.cos( 3.26507470705 +      180.27386923090*t);
      neptune_x_0+=     0.00000313191 * Math.cos( 3.01986161415 +      419.48464387520*t);
      neptune_x_0+=     0.00000382398 * Math.cos( 0.21680708235 +      487.36514376280*t);
      neptune_x_0+=     0.00000301491 * Math.cos( 5.17778763481 +       84.34282612290*t);
      neptune_x_0+=     0.00000336250 * Math.cos( 2.14824434860 +       45.24658263860*t);
      neptune_x_0+=     0.00000285404 * Math.cos( 1.74711125301 +      110.20632121940*t);
      neptune_x_0+=     0.00000304503 * Math.cos( 5.63258357751 +      639.89728631400*t);
      neptune_x_0+=     0.00000333233 * Math.cos( 2.32861862173 +      255.05546779820*t);
      neptune_x_0+=     0.00000268060 * Math.cos( 3.30852177378 +       36.76043751410*t);
      neptune_x_0+=     0.00000264760 * Math.cos( 4.12724083445 +       39.50563376150*t);
      neptune_x_0+=     0.00000313989 * Math.cos( 2.72704786801 +      388.46515523820*t);
      neptune_x_0+=     0.00000226971 * Math.cos( 4.59278380480 +      274.06604832480*t);
      neptune_x_0+=     0.00000306048 * Math.cos( 1.75144377069 +     6283.07584999140*t);
      neptune_x_0+=     0.00000283841 * Math.cos( 3.36226298508 +       12.53017297220*t);
      neptune_x_0+=     0.00000242743 * Math.cos( 2.06472522938 +       14.01464568050*t);
      neptune_x_0+=     0.00000226154 * Math.cos( 2.83844512995 +       80.71948940050*t);
      neptune_x_0+=     0.00000233075 * Math.cos( 4.15738074001 +      105.49227066360*t);
      neptune_x_0+=     0.00000239672 * Math.cos( 0.55843257386 +       27.08733537390*t);
      neptune_x_0+=     0.00000265940 * Math.cos( 4.11954506638 +      944.98282327580*t);
      neptune_x_0+=     0.00000227822 * Math.cos( 2.13057267497 +      103.09277421860*t);
      neptune_x_0+=     0.00000215988 * Math.cos( 2.65917690725 +      316.39186965660*t);
      neptune_x_0+=     0.00000190998 * Math.cos( 2.32419774896 +       69.15252427480*t);
      neptune_x_0+=     0.00000203230 * Math.cos( 0.60054564924 +      415.29185818120*t);
      neptune_x_0+=     0.00000176465 * Math.cos( 0.14731264750 +       36.53668834490*t);
      neptune_x_0+=     0.00000177003 * Math.cos( 0.09240613438 +       24.11838995730*t);
      neptune_x_0+=     0.00000185282 * Math.cos( 3.31492482279 +      175.16605980020*t);
      neptune_x_0+=     0.00000175209 * Math.cos( 1.12575721851 +       39.72938293070*t);
      neptune_x_0+=     0.00000176810 * Math.cos( 3.44067665667 +      216.92243216040*t);
      neptune_x_0+=     0.00000135459 * Math.cos( 3.29658706564 +        9.56122755560*t);
      neptune_x_0+=     0.00000134759 * Math.cos( 5.48177520941 +       75.74480641380*t);
      neptune_x_0+=     0.00000179189 * Math.cos( 3.95792517028 +      183.24281464750*t);
      neptune_x_0+=     0.00000148346 * Math.cos( 1.68010000396 +      151.04766984290*t);
      neptune_x_0+=     0.00000129174 * Math.cos( 5.91949003083 +       43.24084506850*t);
      neptune_x_0+=     0.00000177820 * Math.cos( 3.17257015761 +    10213.28554621100*t);
      neptune_x_0+=     0.00000156561 * Math.cos( 4.19153867973 +       63.73589830340*t);
      neptune_x_0+=     0.00000146334 * Math.cos( 4.81027789789 +       11.04570026390*t);
      neptune_x_0+=     0.00000124092 * Math.cos( 0.33312196832 +       82.85835341460*t);
      neptune_x_0+=     0.00000121226 * Math.cos( 5.10584282456 +       37.92058731670*t);
      neptune_x_0+=     0.00000129049 * Math.cos( 3.80684882859 +       36.86101125060*t);
      neptune_x_0+=     0.00000120117 * Math.cos( 2.36053032404 +       38.34548395890*t);
      neptune_x_0+=     0.00000169037 * Math.cos( 2.49417096791 +      291.70403072770*t);
      neptune_x_0+=     0.00000121138 * Math.cos( 1.49666213233 +       33.02522620710*t);
      neptune_x_0+=     0.00000129442 * Math.cos( 2.36907122801 +       45.55539917930*t);
      neptune_x_0+=     0.00000144638 * Math.cos( 0.63080734164 +       49.17873590170*t);
      neptune_x_0+=     0.00000122915 * Math.cos( 3.67433552159 +       39.40506002500*t);
      neptune_x_0+=     0.00000154797 * Math.cos( 1.74840367711 +       77.22927912210*t);
      neptune_x_0+=     0.00000106839 * Math.cos( 0.57301677365 +        5.10780943070*t);
      neptune_x_0+=     0.00000103540 * Math.cos( 5.25634656769 +       40.84134862350*t);
      neptune_x_0+=     0.00000102917 * Math.cos( 2.29532659562 +       35.42472265210*t);
      neptune_x_0+=     0.00000111109 * Math.cos( 5.21447473078 +       67.35923502580*t);
      neptune_x_0+=     0.00000116205 * Math.cos( 5.56364568271 +      632.78373931320*t);
      neptune_x_0+=     0.00000110050 * Math.cos( 4.33896766039 +      142.14083359310*t);
      neptune_x_0+=     0.00000104452 * Math.cos( 6.26048746922 +      433.71173787680*t);
      neptune_x_0+=     0.00000119617 * Math.cos( 5.01817354003 +       25.60286266560*t);
      neptune_x_0+=     0.00000108865 * Math.cos( 0.01285078004 +     1162.47470440780*t);
      neptune_x_0+=     0.00000100254 * Math.cos( 2.52703279512 +      453.42489381900*t);

      let neptune_x_1=0.0;
      neptune_x_1+=     0.00255840261 * Math.cos( 2.01935686795 +       36.64856292950*t);
      neptune_x_1+=     0.00243125299 * Math.cos( 5.46214902873 +       39.61750834610*t);
      neptune_x_1+=     0.00118398168 * Math.cos( 2.88251845061 +       76.26607127560*t);
      neptune_x_1+=     0.00037965449 * Math.cos( 3.14159265359 +        0.00000000000*t);
      neptune_x_1+=     0.00021924705 * Math.cos( 3.20156164152 +       35.16409022120*t);
      neptune_x_1+=     0.00017459808 * Math.cos( 4.26349398817 +       41.10198105440*t);
      neptune_x_1+=     0.00013130617 * Math.cos( 5.36424961848 +        2.96894541660*t);
      neptune_x_1+=     0.00005086527 * Math.cos( 1.92377354729 +       38.13303563780*t);
      neptune_x_1+=     0.00004899718 * Math.cos( 2.09349497813 +       73.29712585900*t);
      neptune_x_1+=     0.00002745267 * Math.cos( 4.06252818667 +       77.75054398390*t);
      neptune_x_1+=     0.00002204414 * Math.cos( 4.38855639521 +       33.67961751290*t);
      neptune_x_1+=     0.00002168719 * Math.cos( 4.11768012563 +        4.45341812490*t);
      neptune_x_1+=     0.00001572202 * Math.cos( 1.07606611589 +      114.39910691340*t);
      neptune_x_1+=     0.00001344022 * Math.cos( 3.03802059051 +       42.58645376270*t);
      neptune_x_1+=     0.00001285542 * Math.cos( 6.02367554997 +       74.78159856730*t);
      neptune_x_1+=     0.00000897458 * Math.cos( 4.27066342082 +      426.59819087600*t);
      neptune_x_1+=     0.00000865247 * Math.cos( 1.66600949831 +       37.61177077600*t);
      neptune_x_1+=     0.00000849963 * Math.cos( 5.81599544749 +       38.65430049960*t);
      neptune_x_1+=     0.00000920969 * Math.cos( 3.34422970943 +       71.81265315070*t);
      neptune_x_1+=     0.00000776345 * Math.cos( 5.84688443216 +      206.18554843720*t);
      neptune_x_1+=     0.00000753306 * Math.cos( 5.33193950958 +      220.41264243880*t);
      neptune_x_1+=     0.00000607837 * Math.cos( 0.10459953392 +     1059.38193018920*t);
      neptune_x_1+=     0.00000637551 * Math.cos( 5.41077728291 +        1.48447270830*t);
      neptune_x_1+=     0.00000571379 * Math.cos( 2.43114575977 +      522.57741809380*t);
      neptune_x_1+=     0.00000562755 * Math.cos( 1.91445156016 +      536.80451209540*t);
      neptune_x_1+=     0.00000501158 * Math.cos( 1.71336416584 +       28.57180808220*t);
      neptune_x_1+=     0.00000477774 * Math.cos( 4.41606171374 +       98.89998852460*t);
      neptune_x_1+=     0.00000454020 * Math.cos( 1.71446347956 +       35.68535508300*t);
      neptune_x_1+=     0.00000410057 * Math.cos( 5.76580004770 +       40.58071619260*t);
      neptune_x_1+=     0.00000366899 * Math.cos( 5.76755714114 +       47.69426319340*t);
      neptune_x_1+=     0.00000301105 * Math.cos( 2.88798068983 +        5.93789083320*t);
      neptune_x_1+=     0.00000261005 * Math.cos( 5.58341588259 +       32.19514480460*t);
      neptune_x_1+=     0.00000208502 * Math.cos( 4.50403508407 +       70.32818044240*t);
      neptune_x_1+=     0.00000172634 * Math.cos( 4.41668100139 +       33.94024994380*t);
      neptune_x_1+=     0.00000156880 * Math.cos( 2.59636158964 +       79.23501669220*t);
      neptune_x_1+=     0.00000152545 * Math.cos( 0.58200211092 +       30.05628079050*t);
      neptune_x_1+=     0.00000150774 * Math.cos( 3.03955693857 +       42.32582133180*t);
      neptune_x_1+=     0.00000161730 * Math.cos( 0.79247603617 +       31.01948863700*t);
      neptune_x_1+=     0.00000132841 * Math.cos( 1.62575223921 +        8.07675484730*t);
      neptune_x_1+=     0.00000134574 * Math.cos( 0.39220827354 +       45.24658263860*t);
      neptune_x_1+=     0.00000115906 * Math.cos( 1.81847065740 +       44.07092647100*t);
      neptune_x_1+=     0.00000111639 * Math.cos( 0.63975084587 +       46.20979048510*t);
      neptune_x_1+=     0.00000110293 * Math.cos( 6.26561040615 +       35.21227433100*t);
      neptune_x_1+=     0.00000100459 * Math.cos( 1.21320933829 +       41.05379694460*t);
      neptune_x_1+=     0.00000109047 * Math.cos( 3.08916188250 +      112.91463420510*t);
      neptune_x_1=neptune_x_1 * t;

      let neptune_x_2=0.0;
      neptune_x_2+=     0.00005371138 * Math.cos( 0.00000000000 +        0.00000000000*t);
      neptune_x_2+=     0.00004536283 * Math.cos( 5.02700751836 +       36.64856292950*t);
      neptune_x_2+=     0.00004350766 * Math.cos( 2.45420254304 +       39.61750834610*t);
      neptune_x_2+=     0.00003092965 * Math.cos( 0.62250463031 +       38.13303563780*t);
      neptune_x_2+=     0.00002163703 * Math.cos( 1.79218168368 +       76.26607127560*t);
      neptune_x_2+=     0.00000390868 * Math.cos( 5.67643483980 +       35.16409022120*t);
      neptune_x_2+=     0.00000301339 * Math.cos( 1.81737258860 +       41.10198105440*t);
      neptune_x_2+=     0.00000204562 * Math.cos( 2.46637556893 +        2.96894541660*t);
      neptune_x_2+=     0.00000159748 * Math.cos( 1.25894343852 +      206.18554843720*t);
      neptune_x_2+=     0.00000155792 * Math.cos( 3.62416667860 +      220.41264243880*t);
      neptune_x_2+=     0.00000117879 * Math.cos( 4.12696937896 +      522.57741809380*t);
      neptune_x_2+=     0.00000114478 * Math.cos( 0.05970217764 +       35.68535508300*t);
      neptune_x_2+=     0.00000112891 * Math.cos( 0.21785515638 +      536.80451209540*t);
      neptune_x_2+=     0.00000105947 * Math.cos( 1.13935993640 +       40.58071619260*t);
      neptune_x_2=neptune_x_2 * t * t;

      let neptune_x_3=0.0;
      neptune_x_3+=     0.00000192703 * Math.cos( 0.83849647680 +       36.64856292950*t);
      neptune_x_3+=     0.00000182218 * Math.cos( 0.36067577276 +       39.61750834610*t);
      neptune_x_3+=     0.00000180880 * Math.cos( 0.00000000000 +        0.00000000000*t);
      neptune_x_3+=     0.00000131073 * Math.cos( 3.72972175765 +       38.13303563780*t);
      neptune_x_3=neptune_x_3 * t * t * t;

      return neptune_x_0+neptune_x_1+neptune_x_2+neptune_x_3;
   }

   static neptune_y(t){
      let neptune_y_0=0.0;
      neptune_y_0+=    30.06056351665 * Math.cos( 3.74086294714 +       38.13303563780*t);
      neptune_y_0+=     0.30205857683 * Math.cos( 3.14159265359 +        0.00000000000*t);
      neptune_y_0+=     0.13506391797 * Math.cos( 1.92953034883 +       76.26607127560*t);
      neptune_y_0+=     0.15706589373 * Math.cos( 4.82539970129 +       36.64856292950*t);
      neptune_y_0+=     0.14936165806 * Math.cos( 5.79694900665 +       39.61750834610*t);
      neptune_y_0+=     0.02584250749 * Math.cos( 0.42549700754 +        1.48447270830*t);
      neptune_y_0+=     0.01073739772 * Math.cos( 3.81371728533 +       74.78159856730*t);
      neptune_y_0+=     0.00815187583 * Math.cos( 5.49429775826 +        2.96894541660*t);
      neptune_y_0+=     0.00582199295 * Math.cos( 6.19633718936 +       35.16409022120*t);
      neptune_y_0+=     0.00565576412 * Math.cos( 4.41843009015 +       41.10198105440*t);
      neptune_y_0+=     0.00495581047 * Math.cos( 5.31205825784 +      529.69096509460*t);
      neptune_y_0+=     0.00304525203 * Math.cos( 5.11048113661 +       73.29712585900*t);
      neptune_y_0+=     0.00272640298 * Math.cos( 5.58603690785 +      213.29909543800*t);
      neptune_y_0+=     0.00135897385 * Math.cos( 3.97553750964 +       77.75054398390*t);
      neptune_y_0+=     0.00090970871 * Math.cos( 0.11783619888 +      114.39910691340*t);
      neptune_y_0+=     0.00068790261 * Math.cos( 4.26391997151 +        4.45341812490*t);
      neptune_y_0+=     0.00028893355 * Math.cos( 3.21848975032 +       42.58645376270*t);
      neptune_y_0+=     0.00020081559 * Math.cos( 1.19787916085 +       33.67961751290*t);
      neptune_y_0+=     0.00012613583 * Math.cos( 1.99777332934 +      112.91463420510*t);
      neptune_y_0+=     0.00012828708 * Math.cos( 1.16740053443 +      111.43016149680*t);
      neptune_y_0+=     0.00012012961 * Math.cos( 5.66157563804 +     1059.38193018920*t);
      neptune_y_0+=     0.00008768580 * Math.cos( 3.23487156950 +      108.46121608020*t);
      neptune_y_0+=     0.00007581788 * Math.cos( 4.81169168396 +      426.59819087600*t);
      neptune_y_0+=     0.00006439265 * Math.cos( 3.05453259951 +        5.93789083320*t);
      neptune_y_0+=     0.00005297978 * Math.cos( 0.79002313990 +       71.81265315070*t);
      neptune_y_0+=     0.00004650708 * Math.cos( 4.81540983294 +       37.61177077600*t);
      neptune_y_0+=     0.00004733483 * Math.cos( 2.52620194642 +       79.23501669220*t);
      neptune_y_0+=     0.00004557247 * Math.cos( 5.80951552318 +       38.65430049960*t);
      neptune_y_0+=     0.00004322550 * Math.cos( 0.80665145881 +       38.08485152800*t);
      neptune_y_0+=     0.00004315539 * Math.cos( 3.53393506841 +       38.18121974760*t);
      neptune_y_0+=     0.00004089036 * Math.cos( 0.42349446479 +       37.16982779130*t);
      neptune_y_0+=     0.00004247643 * Math.cos( 4.06355336504 +       28.57180808220*t);
      neptune_y_0+=     0.00003932515 * Math.cos( 3.91607592815 +       39.09624348430*t);
      neptune_y_0+=     0.00003930135 * Math.cos( 3.86614178174 +       98.89998852460*t);
      neptune_y_0+=     0.00003323991 * Math.cos( 3.11674274385 +        4.19278569400*t);
      neptune_y_0+=     0.00003112636 * Math.cos( 0.27319642944 +       47.69426319340*t);
      neptune_y_0+=     0.00003373281 * Math.cos( 3.39616255650 +      145.10977900970*t);
      neptune_y_0+=     0.00002670944 * Math.cos( 2.31235275416 +      109.94568878850*t);
      neptune_y_0+=     0.00002523042 * Math.cos( 6.23400745185 +      312.19908396260*t);
      neptune_y_0+=     0.00001888827 * Math.cos( 1.63364331324 +       35.68535508300*t);
      neptune_y_0+=     0.00001647474 * Math.cos( 2.50010254963 +       30.05628079050*t);
      neptune_y_0+=     0.00001826390 * Math.cos( 2.00938305966 +       44.07092647100*t);
      neptune_y_0+=     0.00001967147 * Math.cos( 2.56634772532 +      206.18554843720*t);
      neptune_y_0+=     0.00001681258 * Math.cos( 2.70480318579 +       40.58071619260*t);
      neptune_y_0+=     0.00001533383 * Math.cos( 5.88971113590 +       38.02116105320*t);
      neptune_y_0+=     0.00001894261 * Math.cos( 5.46274825258 +      220.41264243880*t);
      neptune_y_0+=     0.00001527526 * Math.cos( 4.73412534395 +       38.24491022240*t);
      neptune_y_0+=     0.00002086907 * Math.cos( 6.28313624461 +      149.56319713460*t);
      neptune_y_0+=     0.00002057794 * Math.cos( 4.38552505781 +      137.03302416240*t);
      neptune_y_0+=     0.00001720954 * Math.cos( 4.49400805134 +      106.97674337190*t);
      neptune_y_0+=     0.00001314116 * Math.cos( 1.80386443362 +       46.20979048510*t);
      neptune_y_0+=     0.00001732739 * Math.cos( 4.14518500834 +       70.32818044240*t);
      neptune_y_0+=     0.00001559193 * Math.cos( 5.27114846878 +       37.87240320690*t);
      neptune_y_0+=     0.00001545705 * Math.cos( 5.35267669439 +       38.39366806870*t);
      neptune_y_0+=     0.00001435274 * Math.cos( 5.44292013172 +      522.57741809380*t);
      neptune_y_0+=     0.00001404991 * Math.cos( 2.04611088339 +      536.80451209540*t);
      neptune_y_0+=     0.00001242929 * Math.cos( 1.10242173566 +       33.94024994380*t);
      neptune_y_0+=     0.00001388024 * Math.cos( 2.14792830412 +      115.88357962170*t);
      neptune_y_0+=     0.00001467042 * Math.cos( 3.56226463770 +      181.75834193920*t);
      neptune_y_0+=     0.00001227926 * Math.cos( 1.21334651843 +       72.07328558160*t);
      neptune_y_0+=     0.00001080807 * Math.cos( 3.18401661435 +       42.32582133180*t);
      neptune_y_0+=     0.00001111708 * Math.cos( 5.51669920239 +        8.07675484730*t);
      neptune_y_0+=     0.00001237027 * Math.cos( 1.08622199668 +      148.07872442630*t);
      neptune_y_0+=     0.00000722015 * Math.cos( 4.59722014658 +      152.53214255120*t);
      neptune_y_0+=     0.00000608825 * Math.cos( 2.92430662163 +       35.21227433100*t);
      neptune_y_0+=     0.00000730763 * Math.cos( 4.66633801542 +      143.62530630140*t);
      neptune_y_0+=     0.00000631807 * Math.cos( 1.84632009649 +        7.42236354150*t);
      neptune_y_0+=     0.00000553106 * Math.cos( 1.41499357343 +       41.05379694460*t);
      neptune_y_0+=     0.00000685011 * Math.cos( 3.73017585433 +      218.40690486870*t);
      neptune_y_0+=     0.00000463231 * Math.cos( 1.17324835377 +       31.54075349880*t);
      neptune_y_0+=     0.00000515088 * Math.cos( 1.92209565801 +        0.96320784650*t);
      neptune_y_0+=     0.00000436148 * Math.cos( 6.01177332586 +     1589.07289528380*t);
      neptune_y_0+=     0.00000390093 * Math.cos( 0.79231945944 +        6.59228213900*t);
      neptune_y_0+=     0.00000349284 * Math.cos( 4.32031199243 +       60.76695288680*t);
      neptune_y_0+=     0.00000321807 * Math.cos( 3.29433287410 +       44.72531777680*t);
      neptune_y_0+=     0.00000349862 * Math.cos( 0.19787949770 +        0.52126486180*t);
      neptune_y_0+=     0.00000393916 * Math.cos( 3.78100833011 +       31.01948863700*t);
      neptune_y_0+=     0.00000316348 * Math.cos( 1.38572032630 +      419.48464387520*t);
      neptune_y_0+=     0.00000349029 * Math.cos( 4.83858968730 +      180.27386923090*t);
      neptune_y_0+=     0.00000343010 * Math.cos( 5.48051962983 +       68.84370773410*t);
      neptune_y_0+=     0.00000382160 * Math.cos( 1.78928133965 +      487.36514376280*t);
      neptune_y_0+=     0.00000295855 * Math.cos( 0.17950850812 +      110.20632121940*t);
      neptune_y_0+=     0.00000295930 * Math.cos( 3.61173094894 +       84.34282612290*t);
      neptune_y_0+=     0.00000336173 * Math.cos( 0.57726127805 +       45.24658263860*t);
      neptune_y_0+=     0.00000257398 * Math.cos( 4.11483645770 +       32.19514480460*t);
      neptune_y_0+=     0.00000306710 * Math.cos( 4.06192922264 +      639.89728631400*t);
      neptune_y_0+=     0.00000334170 * Math.cos( 3.90094190194 +      255.05546779820*t);
      neptune_y_0+=     0.00000268060 * Math.cos( 1.73772593259 +       36.76043751410*t);
      neptune_y_0+=     0.00000264760 * Math.cos( 2.55644401603 +       39.50563376150*t);
      neptune_y_0+=     0.00000316497 * Math.cos( 1.14702826286 +      388.46515523820*t);
      neptune_y_0+=     0.00000227226 * Math.cos( 6.16115950447 +      274.06604832480*t);
      neptune_y_0+=     0.00000306177 * Math.cos( 0.18466278211 +     6283.07584999140*t);
      neptune_y_0+=     0.00000284905 * Math.cos( 1.78974042607 +       12.53017297220*t);
      neptune_y_0+=     0.00000269131 * Math.cos( 3.43524554279 +      103.09277421860*t);
      neptune_y_0+=     0.00000249102 * Math.cos( 5.73547996252 +      105.49227066360*t);
      neptune_y_0+=     0.00000252180 * Math.cos( 5.24389175498 +       27.08733537390*t);
      neptune_y_0+=     0.00000242394 * Math.cos( 0.49323094252 +       14.01464568050*t);
      neptune_y_0+=     0.00000226119 * Math.cos( 1.26707727523 +       80.71948940050*t);
      neptune_y_0+=     0.00000265738 * Math.cos( 5.67029686231 +      944.98282327580*t);
      neptune_y_0+=     0.00000213341 * Math.cos( 1.07801273826 +      316.39186965660*t);
      neptune_y_0+=     0.00000190279 * Math.cos( 0.75836937752 +       69.15252427480*t);
      neptune_y_0+=     0.00000202599 * Math.cos( 2.17083509018 +      415.29185818120*t);
      neptune_y_0+=     0.00000193212 * Math.cos( 2.53839692499 +      146.59425171800*t);
      neptune_y_0+=     0.00000176465 * Math.cos( 4.85970219043 +       36.53668834490*t);
      neptune_y_0+=     0.00000202771 * Math.cos( 4.96195983984 +      175.16605980020*t);
      neptune_y_0+=     0.00000175209 * Math.cos( 5.83814563218 +       39.72938293070*t);
      neptune_y_0+=     0.00000178926 * Math.cos( 5.00860456688 +      216.92243216040*t);
      neptune_y_0+=     0.00000142340 * Math.cos( 3.85429789127 +       75.74480641380*t);
      neptune_y_0+=     0.00000158140 * Math.cos( 3.25169431065 +       11.04570026390*t);
      neptune_y_0+=     0.00000146954 * Math.cos( 0.12002838388 +      151.04766984290*t);
      neptune_y_0+=     0.00000178005 * Math.cos( 1.60950059216 +    10213.28554621100*t);
      neptune_y_0+=     0.00000152465 * Math.cos( 0.17890470659 +       30.71067209630*t);
      neptune_y_0+=     0.00000168895 * Math.cos( 2.50893462160 +       63.73589830340*t);
      neptune_y_0+=     0.00000121226 * Math.cos( 3.53504657259 +       37.92058731670*t);
      neptune_y_0+=     0.00000129049 * Math.cos( 2.23605298372 +       36.86101125060*t);
      neptune_y_0+=     0.00000120580 * Math.cos( 0.82135679727 +       38.34548395890*t);
      neptune_y_0+=     0.00000168916 * Math.cos( 4.06766309411 +      291.70403072770*t);
      neptune_y_0+=     0.00000121139 * Math.cos( 6.20886903488 +       33.02522620710*t);
      neptune_y_0+=     0.00000129291 * Math.cos( 0.79819261590 +       45.55539917930*t);
      neptune_y_0+=     0.00000144727 * Math.cos( 5.34205062943 +       49.17873590170*t);
      neptune_y_0+=     0.00000140927 * Math.cos( 3.81630631334 +       62.25142559510*t);
      neptune_y_0+=     0.00000122915 * Math.cos( 2.10353868683 +       39.40506002500*t);
      neptune_y_0+=     0.00000154987 * Math.cos( 0.18057956757 +       77.22927912210*t);
      neptune_y_0+=     0.00000106636 * Math.cos( 2.14652349217 +        5.10780943070*t);
      neptune_y_0+=     0.00000127651 * Math.cos( 1.61797740136 +       24.11838995730*t);
      neptune_y_0+=     0.00000103774 * Math.cos( 5.23985408179 +       82.85835341460*t);
      neptune_y_0+=     0.00000103541 * Math.cos( 3.68555193560 +       40.84134862350*t);
      neptune_y_0+=     0.00000104338 * Math.cos( 0.71903696521 +       35.42472265210*t);
      neptune_y_0+=     0.00000112775 * Math.cos( 5.91862646573 +      142.14083359310*t);
      neptune_y_0+=     0.00000112383 * Math.cos( 3.99009058088 +      632.78373931320*t);
      neptune_y_0+=     0.00000104958 * Math.cos( 4.69015786357 +      433.71173787680*t);
      neptune_y_0+=     0.00000106990 * Math.cos( 4.73100569276 +     1162.47470440780*t);

      let neptune_y_1=0.0;
      neptune_y_1+=     0.00352947493 * Math.cos( 3.14159265359 +        0.00000000000*t);
      neptune_y_1+=     0.00256125493 * Math.cos( 0.44757496817 +       36.64856292950*t);
      neptune_y_1+=     0.00243147725 * Math.cos( 3.89099798696 +       39.61750834610*t);
      neptune_y_1+=     0.00118427205 * Math.cos( 1.31128027037 +       76.26607127560*t);
      neptune_y_1+=     0.00021936702 * Math.cos( 1.63124087591 +       35.16409022120*t);
      neptune_y_1+=     0.00017462332 * Math.cos( 2.69229902966 +       41.10198105440*t);
      neptune_y_1+=     0.00012992380 * Math.cos( 3.79578633002 +        2.96894541660*t);
      neptune_y_1+=     0.00004945117 * Math.cos( 0.51727080684 +       73.29712585900*t);
      neptune_y_1+=     0.00002745921 * Math.cos( 2.49178311082 +       77.75054398390*t);
      neptune_y_1+=     0.00002145481 * Math.cos( 2.54768447291 +        4.45341812490*t);
      neptune_y_1+=     0.00001572289 * Math.cos( 5.78853350711 +      114.39910691340*t);
      neptune_y_1+=     0.00001565725 * Math.cos( 2.89846266272 +       33.67961751290*t);
      neptune_y_1+=     0.00001458269 * Math.cos( 1.61835542699 +       38.13303563780*t);
      neptune_y_1+=     0.00001293459 * Math.cos( 4.45868061082 +       74.78159856730*t);
      neptune_y_1+=     0.00001343731 * Math.cos( 1.46712622109 +       42.58645376270*t);
      neptune_y_1+=     0.00000898500 * Math.cos( 2.69840159769 +      426.59819087600*t);
      neptune_y_1+=     0.00000865987 * Math.cos( 0.09556314885 +       37.61177077600*t);
      neptune_y_1+=     0.00000849963 * Math.cos( 4.24519893359 +       38.65430049960*t);
      neptune_y_1+=     0.00000920293 * Math.cos( 1.77507768901 +       71.81265315070*t);
      neptune_y_1+=     0.00000780099 * Math.cos( 4.27192640198 +      206.18554843720*t);
      neptune_y_1+=     0.00000754744 * Math.cos( 3.76138025905 +      220.41264243880*t);
      neptune_y_1+=     0.00000606975 * Math.cos( 4.81932341510 +     1059.38193018920*t);
      neptune_y_1+=     0.00000535973 * Math.cos( 2.93053797020 +        1.48447270830*t);
      neptune_y_1+=     0.00000572284 * Math.cos( 0.85667831685 +      522.57741809380*t);
      neptune_y_1+=     0.00000559236 * Math.cos( 0.34587880894 +      536.80451209540*t);
      neptune_y_1+=     0.00000500998 * Math.cos( 0.14254169132 +       28.57180808220*t);
      neptune_y_1+=     0.00000471868 * Math.cos( 5.96893505289 +       98.89998852460*t);
      neptune_y_1+=     0.00000453930 * Math.cos( 0.14360437422 +       35.68535508300*t);
      neptune_y_1+=     0.00000410057 * Math.cos( 4.19500269960 +       40.58071619260*t);
      neptune_y_1+=     0.00000366899 * Math.cos( 4.19675799066 +       47.69426319340*t);
      neptune_y_1+=     0.00000299214 * Math.cos( 1.31497587337 +        5.93789083320*t);
      neptune_y_1+=     0.00000170466 * Math.cos( 2.89252858677 +       33.94024994380*t);
      neptune_y_1+=     0.00000156618 * Math.cos( 1.02374224930 +       79.23501669220*t);
      neptune_y_1+=     0.00000152553 * Math.cos( 5.29478475308 +       30.05628079050*t);
      neptune_y_1+=     0.00000150776 * Math.cos( 1.46874533276 +       42.32582133180*t);
      neptune_y_1+=     0.00000162840 * Math.cos( 5.51940419316 +       31.01948863700*t);
      neptune_y_1+=     0.00000130379 * Math.cos( 3.20301703119 +        8.07675484730*t);
      neptune_y_1+=     0.00000121024 * Math.cos( 5.30860647354 +       46.20979048510*t);
      neptune_y_1+=     0.00000134658 * Math.cos( 5.10386276839 +       45.24658263860*t);
      neptune_y_1+=     0.00000115930 * Math.cos( 0.24759979383 +       44.07092647100*t);
      neptune_y_1+=     0.00000110293 * Math.cos( 4.69481506643 +       35.21227433100*t);
      neptune_y_1+=     0.00000108365 * Math.cos( 1.52289786655 +      112.91463420510*t);
      neptune_y_1=neptune_y_1 * t;

      let neptune_y_2=0.0;
      neptune_y_2+=     0.00004539421 * Math.cos( 3.45613207922 +       36.64856292950*t);
      neptune_y_2+=     0.00004347956 * Math.cos( 0.88317230351 +       39.61750834610*t);
      neptune_y_2+=     0.00003595394 * Math.cos( 3.14159265359 +        0.00000000000*t);
      neptune_y_2+=     0.00003058647 * Math.cos( 5.31956613665 +       38.13303563780*t);
      neptune_y_2+=     0.00002163809 * Math.cos( 0.22086532214 +       76.26607127560*t);
      neptune_y_2+=     0.00000394632 * Math.cos( 4.10915465726 +       35.16409022120*t);
      neptune_y_2+=     0.00000301094 * Math.cos( 0.24659723217 +       41.10198105440*t);
      neptune_y_2+=     0.00000160365 * Math.cos( 5.99443081049 +      206.18554843720*t);
      neptune_y_2+=     0.00000156892 * Math.cos( 2.05073612924 +      220.41264243880*t);
      neptune_y_2+=     0.00000186626 * Math.cos( 0.85138234128 +        2.96894541660*t);
      neptune_y_2+=     0.00000118091 * Math.cos( 2.56552779577 +      522.57741809380*t);
      neptune_y_2+=     0.00000114478 * Math.cos( 4.77209191510 +       35.68535508300*t);
      neptune_y_2+=     0.00000112049 * Math.cos( 4.93195559733 +      536.80451209540*t);
      neptune_y_2+=     0.00000105947 * Math.cos( 5.85174809888 +       40.58071619260*t);
      neptune_y_2+=     0.00000101381 * Math.cos( 0.89282766843 +      213.29909543800*t);
      neptune_y_2=neptune_y_2 * t * t;

      let neptune_y_3=0.0;
      neptune_y_3+=     0.00000192703 * Math.cos( 5.55088601013 +       36.64856292950*t);
      neptune_y_3+=     0.00000182218 * Math.cos( 5.07306416874 +       39.61750834610*t);
      neptune_y_3+=     0.00000176062 * Math.cos( 0.00000000000 +        0.00000000000*t);
      neptune_y_3+=     0.00000130731 * Math.cos( 2.18169161636 +       38.13303563780*t);
      neptune_y_3=neptune_y_3 * t * t * t;

      return neptune_y_0+neptune_y_1+neptune_y_2+neptune_y_3;
   }

   static neptune_z(t){
      let neptune_z_0=0.0;
      neptune_z_0+=     0.92866054405 * Math.cos( 1.44103930278 +       38.13303563780*t);
      neptune_z_0+=     0.01245978462 * Math.cos( 0.00000000000 +        0.00000000000*t);
      neptune_z_0+=     0.00474333567 * Math.cos( 2.52218774238 +       36.64856292950*t);
      neptune_z_0+=     0.00451987936 * Math.cos( 3.50949720541 +       39.61750834610*t);
      neptune_z_0+=     0.00417558068 * Math.cos( 5.91310695421 +       76.26607127560*t);
      neptune_z_0+=     0.00084104329 * Math.cos( 4.38928900096 +        1.48447270830*t);
      neptune_z_0+=     0.00032704958 * Math.cos( 1.52048692001 +       74.78159856730*t);
      neptune_z_0+=     0.00030873335 * Math.cos( 3.29017611456 +       35.16409022120*t);
      neptune_z_0+=     0.00025812584 * Math.cos( 3.19303128782 +        2.96894541660*t);
      neptune_z_0+=     0.00016865319 * Math.cos( 2.13251104425 +       41.10198105440*t);
      neptune_z_0+=     0.00011789909 * Math.cos( 3.60001877675 +      213.29909543800*t);
      neptune_z_0+=     0.00009770125 * Math.cos( 2.80133971586 +       73.29712585900*t);
      neptune_z_0+=     0.00011279680 * Math.cos( 3.55816676334 +      529.69096509460*t);
      neptune_z_0+=     0.00004119873 * Math.cos( 1.67934316836 +       77.75054398390*t);
      neptune_z_0+=     0.00002818034 * Math.cos( 4.10661077794 +      114.39910691340*t);
      neptune_z_0+=     0.00002868677 * Math.cos( 4.27011526203 +       33.67961751290*t);
      neptune_z_0+=     0.00002213464 * Math.cos( 1.96045135168 +        4.45341812490*t);
      neptune_z_0+=     0.00001865650 * Math.cos( 5.05540709577 +       71.81265315070*t);
      neptune_z_0+=     0.00000840177 * Math.cos( 0.94268885160 +       42.58645376270*t);
      neptune_z_0+=     0.00000457516 * Math.cos( 5.71650412080 +      108.46121608020*t);
      neptune_z_0+=     0.00000530252 * Math.cos( 0.85800267793 +      111.43016149680*t);
      neptune_z_0+=     0.00000490859 * Math.cos( 6.07827301209 +      112.91463420510*t);
      neptune_z_0+=     0.00000331254 * Math.cos( 0.29304964526 +       70.32818044240*t);
      neptune_z_0+=     0.00000330045 * Math.cos( 2.83839676215 +      426.59819087600*t);
      neptune_z_0+=     0.00000273589 * Math.cos( 3.91013681794 +     1059.38193018920*t);
      neptune_z_0+=     0.00000277586 * Math.cos( 1.45092010545 +      148.07872442630*t);
      neptune_z_0+=     0.00000274474 * Math.cos( 5.42657022437 +       32.19514480460*t);
      neptune_z_0+=     0.00000205306 * Math.cos( 0.75818737085 +        5.93789083320*t);
      neptune_z_0+=     0.00000173516 * Math.cos( 5.85498030099 +      145.10977900970*t);
      neptune_z_0+=     0.00000141275 * Math.cos( 1.73147597657 +       28.57180808220*t);
      neptune_z_0+=     0.00000139093 * Math.cos( 1.67466701191 +      184.72728735580*t);
      neptune_z_0+=     0.00000143647 * Math.cos( 2.51620047812 +       37.61177077600*t);
      neptune_z_0+=     0.00000136955 * Math.cos( 0.20339778664 +       79.23501669220*t);
      neptune_z_0+=     0.00000126296 * Math.cos( 4.40661385040 +       37.16982779130*t);
      neptune_z_0+=     0.00000120906 * Math.cos( 1.61767636602 +       39.09624348430*t);
      neptune_z_0+=     0.00000111761 * Math.cos( 6.20948230785 +       98.89998852460*t);
      neptune_z_0+=     0.00000140758 * Math.cos( 3.50944989694 +       38.65430049960*t);
      neptune_z_0+=     0.00000111589 * Math.cos( 4.18561395578 +       47.69426319340*t);
      neptune_z_0+=     0.00000133509 * Math.cos( 4.78977105547 +       38.08485152800*t);
      neptune_z_0+=     0.00000102622 * Math.cos( 0.81673762159 +        4.19278569400*t);
      neptune_z_0+=     0.00000133292 * Math.cos( 1.23386935925 +       38.18121974760*t);

      let neptune_z_1=0.0;
      neptune_z_1+=     0.00154885971 * Math.cos( 2.14239039664 +       38.13303563780*t);
      neptune_z_1+=     0.00007783708 * Math.cos( 4.40146905905 +       36.64856292950*t);
      neptune_z_1+=     0.00006862414 * Math.cos( 1.65930160610 +       39.61750834610*t);
      neptune_z_1+=     0.00009464276 * Math.cos( 0.00000000000 +        0.00000000000*t);
      neptune_z_1+=     0.00003891873 * Math.cos( 5.46761139427 +       76.26607127560*t);
      neptune_z_1+=     0.00000794811 * Math.cos( 5.98635430889 +       35.16409022120*t);
      neptune_z_1+=     0.00000539404 * Math.cos( 4.94521335014 +      213.29909543800*t);
      neptune_z_1+=     0.00000506405 * Math.cos( 0.44976388514 +       41.10198105440*t);
      neptune_z_1+=     0.00000388058 * Math.cos( 1.52509517254 +      529.69096509460*t);
      neptune_z_1+=     0.00000374315 * Math.cos( 1.56222971632 +        2.96894541660*t);
      neptune_z_1+=     0.00000177485 * Math.cos( 4.37166358766 +       73.29712585900*t);
      neptune_z_1+=     0.00000183128 * Math.cos( 5.40794621153 +        1.48447270830*t);
      neptune_z_1=neptune_z_1 * t;

      let neptune_z_2=0.0;
      neptune_z_2+=     0.00001264840 * Math.cos( 1.91401498992 +       38.13303563780*t);
      neptune_z_2+=     0.00000130346 * Math.cos( 1.12728833394 +       36.64856292950*t);
      neptune_z_2+=     0.00000127993 * Math.cos( 4.77241139328 +       39.61750834610*t);
      neptune_z_2=neptune_z_2 * t * t;

      let neptune_z_3=0.0;
      neptune_z_3+=     0.00000124222 * Math.cos( 3.06928911462 +       38.13303563780*t);
      neptune_z_3=neptune_z_3 * t * t * t;

      return neptune_z_0+neptune_z_1+neptune_z_2+neptune_z_3;
   }

   static saturn_x(t){
      let saturn_x_0=0.0;
      saturn_x_0+=     9.51638335797 * Math.cos( 0.87441380794 +      213.29909543800*t);
      saturn_x_0+=     0.26412374238 * Math.cos( 0.12390892620 +      426.59819087600*t);
      saturn_x_0+=     0.06760430339 * Math.cos( 4.16767145778 +      206.18554843720*t);
      saturn_x_0+=     0.06624260115 * Math.cos( 0.75094737780 +      220.41264243880*t);
      saturn_x_0+=     0.04244797817 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_x_0+=     0.02336340488 * Math.cos( 2.02227784673 +        7.11354700080*t);
      saturn_x_0+=     0.01255372247 * Math.cos( 2.17338917731 +      110.20632121940*t);
      saturn_x_0+=     0.01115684467 * Math.cos( 3.15686878377 +      419.48464387520*t);
      saturn_x_0+=     0.01097683232 * Math.cos( 5.65753337256 +      639.89728631400*t);
      saturn_x_0+=     0.00716328481 * Math.cos( 2.71149993708 +      316.39186965660*t);
      saturn_x_0+=     0.00509313365 * Math.cos( 4.95865624780 +      103.09277421860*t);
      saturn_x_0+=     0.00433994439 * Math.cos( 0.72012820974 +      529.69096509460*t);
      saturn_x_0+=     0.00372894461 * Math.cos( 0.00137195497 +      433.71173787680*t);
      saturn_x_0+=     0.00097843523 * Math.cos( 1.01485750417 +      323.50541665740*t);
      saturn_x_0+=     0.00080600536 * Math.cos( 5.62103979796 +       11.04570026390*t);
      saturn_x_0+=     0.00083782316 * Math.cos( 0.62038893702 +      227.52618943960*t);
      saturn_x_0+=     0.00074150224 * Math.cos( 2.38206066655 +      632.78373931320*t);
      saturn_x_0+=     0.00070219382 * Math.cos( 0.88789752415 +      209.36694217490*t);
      saturn_x_0+=     0.00068855792 * Math.cos( 4.01788097627 +      217.23124870110*t);
      saturn_x_0+=     0.00065620467 * Math.cos( 2.69728593339 +      202.25339517410*t);
      saturn_x_0+=     0.00058297911 * Math.cos( 2.16155251399 +      224.34479570190*t);
      saturn_x_0+=     0.00054022837 * Math.cos( 4.90928184374 +      853.19638175200*t);
      saturn_x_0+=     0.00045550446 * Math.cos( 1.88235037830 +       14.22709400160*t);
      saturn_x_0+=     0.00038345667 * Math.cos( 4.39815501478 +      199.07200143640*t);
      saturn_x_0+=     0.00044551703 * Math.cos( 5.60763553535 +       63.73589830340*t);
      saturn_x_0+=     0.00025165185 * Math.cos( 0.37800582257 +      216.48048917570*t);
      saturn_x_0+=     0.00024554499 * Math.cos( 4.53150598095 +      210.11770170030*t);
      saturn_x_0+=     0.00024673219 * Math.cos( 5.90891573850 +      522.57741809380*t);
      saturn_x_0+=     0.00024677050 * Math.cos( 5.60389382420 +      415.55249061210*t);
      saturn_x_0+=     0.00025491374 * Math.cos( 1.63922423181 +      117.31986822020*t);
      saturn_x_0+=     0.00031253049 * Math.cos( 4.62976601833 +      735.87651353180*t);
      saturn_x_0+=     0.00023372467 * Math.cos( 5.53491987276 +      647.01083331480*t);
      saturn_x_0+=     0.00023355468 * Math.cos( 0.18791490124 +      149.56319713460*t);
      saturn_x_0+=     0.00024805815 * Math.cos( 5.50327676733 +       74.78159856730*t);
      saturn_x_0+=     0.00014731703 * Math.cos( 4.67981909838 +      277.03499374140*t);
      saturn_x_0+=     0.00012427525 * Math.cos( 1.02995545746 +     1059.38193018920*t);
      saturn_x_0+=     0.00009943329 * Math.cos( 0.84628387596 +        3.93215326310*t);
      saturn_x_0+=     0.00012393514 * Math.cos( 4.19747622821 +      490.33408917940*t);
      saturn_x_0+=     0.00012026472 * Math.cos( 5.66372282839 +      351.81659230870*t);
      saturn_x_0+=     0.00008222014 * Math.cos( 2.47875301104 +      742.99006053260*t);
      saturn_x_0+=     0.00009087093 * Math.cos( 4.33505326762 +     1052.26838318840*t);
      saturn_x_0+=     0.00006717741 * Math.cos( 5.51897460997 +      838.96928775040*t);
      saturn_x_0+=     0.00006232999 * Math.cos( 2.45837758015 +      846.08283475120*t);
      saturn_x_0+=     0.00007161671 * Math.cos( 2.18152751738 +       95.97922721780*t);
      saturn_x_0+=     0.00006321101 * Math.cos( 0.83915408770 +      309.27832265580*t);
      saturn_x_0+=     0.00006074958 * Math.cos( 6.15905897331 +      440.82528487760*t);
      saturn_x_0+=     0.00005343894 * Math.cos( 3.60046273598 +      412.37109687440*t);
      saturn_x_0+=     0.00004860582 * Math.cos( 0.26461045175 +      536.80451209540*t);
      saturn_x_0+=     0.00005775802 * Math.cos( 5.30717695229 +       38.13303563780*t);
      saturn_x_0+=     0.00005194178 * Math.cos( 4.54584467686 +      210.85141488320*t);
      saturn_x_0+=     0.00005152474 * Math.cos( 0.34669517150 +      215.74677599280*t);
      saturn_x_0+=     0.00003792540 * Math.cos( 5.99766568983 +      422.66603761290*t);
      saturn_x_0+=     0.00003762834 * Math.cos( 3.72112920226 +      212.33588759150*t);
      saturn_x_0+=     0.00003747433 * Math.cos( 1.16965137714 +      214.26230328450*t);
      saturn_x_0+=     0.00003114576 * Math.cos( 0.84631897292 +      213.25091132820*t);
      saturn_x_0+=     0.00003113641 * Math.cos( 4.04410367190 +      213.34727954780*t);
      saturn_x_0+=     0.00002990421 * Math.cos( 0.04148806852 +      625.67019231240*t);
      saturn_x_0+=     0.00004111695 * Math.cos( 5.96153153046 +      137.03302416240*t);
      saturn_x_0+=     0.00002966450 * Math.cos( 5.39568820046 +      138.51749687070*t);
      saturn_x_0+=     0.00002827527 * Math.cos( 0.73252555642 +      330.61896365820*t);
      saturn_x_0+=     0.00003363323 * Math.cos( 1.42089586686 +      437.64389113990*t);
      saturn_x_0+=     0.00002886599 * Math.cos( 1.14057922619 +       85.82729883120*t);
      saturn_x_0+=     0.00002634075 * Math.cos( 5.40645201521 +      288.08069400530*t);
      saturn_x_0+=     0.00002713354 * Math.cos( 0.96812639712 +      203.73786788240*t);
      saturn_x_0+=     0.00003169390 * Math.cos( 5.76640408988 +       76.26607127560*t);
      saturn_x_0+=     0.00002618634 * Math.cos( 5.49334837098 +      127.47179660680*t);
      saturn_x_0+=     0.00002527746 * Math.cos( 5.09752068381 +      628.85158605010*t);
      saturn_x_0+=     0.00002989778 * Math.cos( 4.15673836604 +     1066.49547719000*t);
      saturn_x_0+=     0.00002507415 * Math.cos( 1.49447138038 +        9.56122755560*t);
      saturn_x_0+=     0.00002470181 * Math.cos( 5.27435870056 +     1155.36115740700*t);
      saturn_x_0+=     0.00002427626 * Math.cos( 3.97311214231 +      222.86032299360*t);
      saturn_x_0+=     0.00003128325 * Math.cos( 4.05483976553 +     1368.66025284500*t);
      saturn_x_0+=     0.00002309076 * Math.cos( 3.67821438247 +      430.53034413910*t);
      saturn_x_0+=     0.00002162629 * Math.cos( 3.26951119901 +      340.77089204480*t);
      saturn_x_0+=     0.00002912676 * Math.cos( 1.76893577106 +        3.18139373770*t);
      saturn_x_0+=     0.00002095366 * Math.cos( 3.55759089756 +      423.41679713830*t);
      saturn_x_0+=     0.00002335270 * Math.cos( 5.86791072516 +      388.46515523820*t);
      saturn_x_0+=     0.00001634262 * Math.cos( 4.54357767539 +       12.53017297220*t);
      saturn_x_0+=     0.00001635975 * Math.cos( 2.19968869780 +      212.77783057620*t);
      saturn_x_0+=     0.00001632759 * Math.cos( 2.69164822165 +      213.82036029980*t);
      saturn_x_0+=     0.00001498689 * Math.cos( 3.60168057129 +       52.69019803950*t);
      saturn_x_0+=     0.00001461217 * Math.cos( 5.92456743836 +      429.77958461370*t);
      saturn_x_0+=     0.00001963947 * Math.cos( 2.05086487180 +        1.48447270830*t);
      saturn_x_0+=     0.00001538425 * Math.cos( 4.78544077085 +      860.30992875280*t);
      saturn_x_0+=     0.00001485856 * Math.cos( 5.65501463408 +      949.17560896980*t);
      saturn_x_0+=     0.00001418116 * Math.cos( 5.41419993599 +      350.33211960040*t);
      saturn_x_0+=     0.00001147607 * Math.cos( 0.19147238521 +      942.06206196900*t);
      saturn_x_0+=     0.00001111703 * Math.cos( 0.47907488492 +      234.63973644040*t);
      saturn_x_0+=     0.00001019566 * Math.cos( 5.00707811029 +     1471.75302706360*t);
      saturn_x_0+=     0.00001009190 * Math.cos( 1.34289487761 +      265.98929347750*t);
      saturn_x_0+=     0.00000977078 * Math.cos( 6.08156695465 +      515.46387109300*t);
      saturn_x_0+=     0.00001089450 * Math.cos( 5.82690672710 +      362.86229257260*t);
      saturn_x_0+=     0.00001092244 * Math.cos( 1.13561107749 +      173.94221952280*t);
      saturn_x_0+=     0.00001173456 * Math.cos( 3.79591687208 +     1685.05212250160*t);
      saturn_x_0+=     0.00000867990 * Math.cos( 3.23603400378 +      210.37833413120*t);
      saturn_x_0+=     0.00001118369 * Math.cos( 3.46624149583 +      703.63318461740*t);
      saturn_x_0+=     0.00000867952 * Math.cos( 1.65168536612 +      216.21985674480*t);
      saturn_x_0+=     0.00001150595 * Math.cos( 3.74707160019 +      200.76892246580*t);
      saturn_x_0+=     0.00000829641 * Math.cos( 0.58167216896 +      212.54833591260*t);
      saturn_x_0+=     0.00000825033 * Math.cos( 4.30734330456 +      214.04985496340*t);
      saturn_x_0+=     0.00000881459 * Math.cos( 1.47222252626 +      209.10630974400*t);
      saturn_x_0+=     0.00000865067 * Math.cos( 3.41432256973 +      217.49188113200*t);
      saturn_x_0+=     0.00000789282 * Math.cos( 0.23960587227 +      223.59403617650*t);
      saturn_x_0+=     0.00001007761 * Math.cos( 1.08964371328 +      225.82926841020*t);
      saturn_x_0+=     0.00000918433 * Math.cos( 4.86149490085 +      565.11568774670*t);
      saturn_x_0+=     0.00000731350 * Math.cos( 5.90815395090 +     1265.56747862640*t);
      saturn_x_0+=     0.00000859969 * Math.cos( 3.70935438142 +      252.65597135320*t);
      saturn_x_0+=     0.00000780935 * Math.cos( 4.83859148457 +      728.76296653100*t);
      saturn_x_0+=     0.00000787944 * Math.cos( 2.18484045281 +       88.86568021700*t);
      saturn_x_0+=     0.00000710327 * Math.cos( 3.41709256412 +      417.03696332040*t);
      saturn_x_0+=     0.00000718894 * Math.cos( 1.95883016371 +      956.28915597060*t);
      saturn_x_0+=     0.00000918525 * Math.cos( 4.57697125213 +      563.63121503840*t);
      saturn_x_0+=     0.00000798401 * Math.cos( 2.01609257440 +      207.88246946660*t);
      saturn_x_0+=     0.00000647073 * Math.cos( 2.95872943804 +       99.16062095550*t);
      saturn_x_0+=     0.00000708539 * Math.cos( 0.91058417437 +      207.67002114550*t);
      saturn_x_0+=     0.00000768432 * Math.cos( 2.89648077129 +      218.71572140940*t);
      saturn_x_0+=     0.00000692104 * Math.cos( 3.97719114831 +      218.92816973050*t);
      saturn_x_0+=     0.00000727485 * Math.cos( 0.30850251852 +     1162.47470440780*t);
      saturn_x_0+=     0.00000633567 * Math.cos( 6.23245450174 +       70.84944530420*t);
      saturn_x_0+=     0.00000613975 * Math.cos( 2.45662208568 +      142.44965013380*t);
      saturn_x_0+=     0.00000798605 * Math.cos( 1.35392610026 +       22.09140052780*t);
      saturn_x_0+=     0.00000833141 * Math.cos( 2.96256457754 +      160.60889739850*t);
      saturn_x_0+=     0.00000760670 * Math.cos( 1.72547418591 +       21.34064100240*t);
      saturn_x_0+=     0.00000624518 * Math.cos( 2.79603428367 +       18.15924726470*t);
      saturn_x_0+=     0.00000698288 * Math.cos( 0.39606094967 +       62.25142559510*t);
      saturn_x_0+=     0.00000599292 * Math.cos( 3.85685062144 +      554.06998748280*t);
      saturn_x_0+=     0.00000696752 * Math.cos( 0.57191090814 +      124.43341522100*t);
      saturn_x_0+=     0.00000613225 * Math.cos( 4.42187080646 +      217.96496188400*t);
      saturn_x_0+=     0.00000516082 * Math.cos( 2.58929130314 +      408.43894361130*t);
      saturn_x_0+=     0.00000581150 * Math.cos( 2.07880434678 +      231.45834270270*t);
      saturn_x_0+=     0.00000665581 * Math.cos( 2.82434445437 +      425.11371816770*t);
      saturn_x_0+=     0.00000513474 * Math.cos( 0.39337122033 +      414.06801790380*t);
      saturn_x_0+=     0.00000657131 * Math.cos( 1.40194432916 +       65.22037101170*t);
      saturn_x_0+=     0.00000493977 * Math.cos( 0.34470358866 +      302.16477565500*t);
      saturn_x_0+=     0.00000503950 * Math.cos( 6.20460558308 +     1258.45393162560*t);
      saturn_x_0+=     0.00000530435 * Math.cos( 2.53005245833 +      214.78356814630*t);
      saturn_x_0+=     0.00000548712 * Math.cos( 0.47707901323 +      208.63322899200*t);
      saturn_x_0+=     0.00000447477 * Math.cos( 4.71542440428 +      203.00415469950*t);
      saturn_x_0+=     0.00000446305 * Math.cos( 4.74401934346 +     1788.14489672020*t);
      saturn_x_0+=     0.00000465392 * Math.cos( 5.40750083938 +      654.12438031560*t);
      saturn_x_0+=     0.00000502185 * Math.cos( 4.37004071521 +      251.43213107580*t);
      saturn_x_0+=     0.00000448425 * Math.cos( 1.35674392267 +     1589.07289528380*t);
      saturn_x_0+=     0.00000517284 * Math.cos( 2.16331838082 +      211.81462272970*t);
      saturn_x_0+=     0.00000413563 * Math.cos( 3.63586974301 +      148.07872442630*t);
      saturn_x_0+=     0.00000399606 * Math.cos( 3.23973258155 +      213.18722085340*t);
      saturn_x_0+=     0.00000399606 * Math.cos( 1.64957508001 +      213.41097002260*t);
      saturn_x_0+=     0.00000384384 * Math.cos( 5.65541518775 +     1581.95934828300*t);
      saturn_x_0+=     0.00000400290 * Math.cos( 3.15876824938 +      404.50679034820*t);
      saturn_x_0+=     0.00000395127 * Math.cos( 0.08823789222 +     1478.86657406440*t);
      saturn_x_0+=     0.00000350293 * Math.cos( 5.00255705341 +      198.32124191100*t);
      saturn_x_0+=     0.00000464864 * Math.cos( 3.54480854933 +     2001.44399215820*t);
      saturn_x_0+=     0.00000351121 * Math.cos( 5.86405155542 +       98.89998852460*t);
      saturn_x_0+=     0.00000335788 * Math.cos( 1.02993303771 +      213.51154375910*t);
      saturn_x_0+=     0.00000335788 * Math.cos( 3.85937462386 +      213.08664711690*t);
      saturn_x_0+=     0.00000367643 * Math.cos( 4.66054518863 +      114.13847448250*t);
      saturn_x_0+=     0.00000367304 * Math.cos( 5.88650282265 +      750.10360753340*t);
      saturn_x_0+=     0.00000369772 * Math.cos( 5.39924643016 +      151.04766984290*t);
      saturn_x_0+=     0.00000318641 * Math.cos( 5.70073398414 +      831.85574074960*t);
      saturn_x_0+=     0.00000317269 * Math.cos( 6.15399946707 +      228.27694896500*t);
      saturn_x_0+=     0.00000416098 * Math.cos( 5.91051454266 +      191.20769491020*t);
      saturn_x_0+=     0.00000319406 * Math.cos( 0.72194326719 +      175.16605980020*t);
      saturn_x_0+=     0.00000381531 * Math.cos( 1.39616544631 +      312.19908396260*t);
      saturn_x_0+=     0.00000382800 * Math.cos( 2.56517911849 +       56.62235130260*t);
      saturn_x_0+=     0.00000402465 * Math.cos( 4.29571195670 +      177.87437278590*t);
      saturn_x_0+=     0.00000337120 * Math.cos( 2.96241883499 +      479.28838891550*t);
      saturn_x_0+=     0.00000270298 * Math.cos( 5.13892679265 +      635.96513305090*t);
      saturn_x_0+=     0.00000268385 * Math.cos( 4.75118314124 +      191.95845443560*t);
      saturn_x_0+=     0.00000269380 * Math.cos( 1.30301159795 +      278.51946644970*t);
      saturn_x_0+=     0.00000268854 * Math.cos( 5.66985306128 +      205.22234059070*t);
      saturn_x_0+=     0.00000315241 * Math.cos( 1.98234278819 +      106.27416795630*t);
      saturn_x_0+=     0.00000269016 * Math.cos( 2.15203921815 +      327.43756992050*t);
      saturn_x_0+=     0.00000347502 * Math.cos( 5.76861803456 +      195.13984817330*t);
      saturn_x_0+=     0.00000347341 * Math.cos( 0.61908132149 +      248.72381809010*t);
      saturn_x_0+=     0.00000296359 * Math.cos( 1.51933329331 +       10.29494073850*t);
      saturn_x_0+=     0.00000280829 * Math.cos( 3.77309922396 +        2.44768055480*t);
      saturn_x_0+=     0.00000252470 * Math.cos( 1.67539597791 +      213.55972786890*t);
      saturn_x_0+=     0.00000252470 * Math.cos( 3.21391208773 +      213.03846300710*t);
      saturn_x_0+=     0.00000272972 * Math.cos( 4.55564352170 +     1045.15483618760*t);
      saturn_x_0+=     0.00000239800 * Math.cos( 5.92731308060 +     1574.84580128220*t);
      saturn_x_0+=     0.00000241206 * Math.cos( 5.74905299531 +      221.37585028530*t);
      saturn_x_0+=     0.00000224581 * Math.cos( 1.93088202036 +       39.35687591520*t);
      saturn_x_0+=     0.00000303332 * Math.cos( 1.08981956452 +      483.22054217860*t);
      saturn_x_0+=     0.00000292918 * Math.cos( 3.86514080986 +      424.15051032120*t);
      saturn_x_0+=     0.00000304839 * Math.cos( 1.75379009485 +     6283.07584999140*t);
      saturn_x_0+=     0.00000236937 * Math.cos( 4.96032795425 +      235.39049596580*t);
      saturn_x_0+=     0.00000211444 * Math.cos( 0.02150963509 +      543.91805909620*t);
      saturn_x_0+=     0.00000234092 * Math.cos( 5.78186298869 +      275.55052103310*t);
      saturn_x_0+=     0.00000204931 * Math.cos( 4.46341699841 +      842.15068148810*t);
      saturn_x_0+=     0.00000203518 * Math.cos( 4.48361003131 +     2104.53676637680*t);
      saturn_x_0+=     0.00000266641 * Math.cos( 3.49646394105 +      121.25202148330*t);
      saturn_x_0+=     0.00000230862 * Math.cos( 4.03811269085 +      497.44763618020*t);
      saturn_x_0+=     0.00000202640 * Math.cos( 2.91715278214 +      284.14854074220*t);
      saturn_x_0+=     0.00000192711 * Math.cos( 5.33622790894 +     1898.35121793960*t);
      saturn_x_0+=     0.00000217166 * Math.cos( 6.14501268573 +      429.04587143080*t);
      saturn_x_0+=     0.00000213986 * Math.cos( 2.44871785704 +        8.07675484730*t);
      saturn_x_0+=     0.00000212877 * Math.cos( 0.67438396717 +      650.94298657790*t);
      saturn_x_0+=     0.00000215232 * Math.cos( 2.97872772544 +      425.63498302950*t);
      saturn_x_0+=     0.00000236824 * Math.cos( 3.57393052829 +      219.44943459230*t);
      saturn_x_0+=     0.00000203264 * Math.cos( 1.15942079115 +     1375.77379984580*t);
      saturn_x_0+=     0.00000174574 * Math.cos( 3.29077366662 +      426.64637498580*t);
      saturn_x_0+=     0.00000218159 * Math.cos( 1.64908016840 +      269.92144674060*t);
      saturn_x_0+=     0.00000169471 * Math.cos( 4.78021413557 +      501.37978944330*t);
      saturn_x_0+=     0.00000174569 * Math.cos( 0.09297884169 +      426.55000676620*t);
      saturn_x_0+=     0.00000176368 * Math.cos( 0.50228212449 +      618.55664531160*t);
      saturn_x_0+=     0.00000163515 * Math.cos( 0.76931838572 +      312.45971639350*t);
      saturn_x_0+=     0.00000182548 * Math.cos( 1.24685117319 +      210.59078245230*t);
      saturn_x_0+=     0.00000170038 * Math.cos( 6.21992022263 +     1795.25844372100*t);
      saturn_x_0+=     0.00000188022 * Math.cos( 0.50637735109 +      427.56139872250*t);
      saturn_x_0+=     0.00000179530 * Math.cos( 3.64276719183 +      216.00740842370*t);
      saturn_x_0+=     0.00000180882 * Math.cos( 3.08082546788 +       84.34282612290*t);
      saturn_x_0+=     0.00000166973 * Math.cos( 4.32185770884 +      355.74874557180*t);
      saturn_x_0+=     0.00000151676 * Math.cos( 4.13754942735 +      213.45915413240*t);
      saturn_x_0+=     0.00000151676 * Math.cos( 0.75207673924 +      213.13903674360*t);
      saturn_x_0+=     0.00000151432 * Math.cos( 3.90513456730 +      220.46082654860*t);
      saturn_x_0+=     0.00000194652 * Math.cos( 5.26736778530 +      488.84961647110*t);
      saturn_x_0+=     0.00000149055 * Math.cos( 5.67257832801 +      107.02492748170*t);
      saturn_x_0+=     0.00000191290 * Math.cos( 3.29984174656 +     2317.83586181480*t);
      saturn_x_0+=     0.00000166449 * Math.cos( 3.40892440053 +     1279.79457262800*t);
      saturn_x_0+=     0.00000180790 * Math.cos( 0.04936208794 +      491.81856188770*t);
      saturn_x_0+=     0.00000188196 * Math.cos( 1.34108074604 +      207.14875628370*t);
      saturn_x_0+=     0.00000171504 * Math.cos( 3.32007828165 +       73.29712585900*t);
      saturn_x_0+=     0.00000146618 * Math.cos( 0.72929682140 +      220.36445832900*t);
      saturn_x_0+=     0.00000193237 * Math.cos( 4.19968617237 +      188.92007304980*t);
      saturn_x_0+=     0.00000137090 * Math.cos( 5.42655130336 +     1148.24761040620*t);
      saturn_x_0+=     0.00000146331 * Math.cos( 6.12359043156 +        5.41662597140*t);
      saturn_x_0+=     0.00000185616 * Math.cos( 5.12367952113 +      601.76425067620*t);
      saturn_x_0+=     0.00000158034 * Math.cos( 3.42936876808 +      179.35884549420*t);
      saturn_x_0+=     0.00000176989 * Math.cos( 2.59441226782 +      344.70304530790*t);
      saturn_x_0+=     0.00000159685 * Math.cos( 5.53376678198 +      358.93013930950*t);
      saturn_x_0+=     0.00000155790 * Math.cos( 4.99237742083 +      289.56516671360*t);
      saturn_x_0+=     0.00000138147 * Math.cos( 3.19940941173 +      436.15941843160*t);
      saturn_x_0+=     0.00000177192 * Math.cos( 3.17596798012 +    10213.28554621100*t);
      saturn_x_0+=     0.00000125961 * Math.cos( 3.35117964179 +      643.82943957710*t);
      saturn_x_0+=     0.00000131798 * Math.cos( 2.50083539634 +      212.02707105080*t);
      saturn_x_0+=     0.00000139279 * Math.cos( 2.71243130336 +      636.71589257630*t);
      saturn_x_0+=     0.00000122329 * Math.cos( 1.96650577886 +       69.15252427480*t);
      saturn_x_0+=     0.00000130711 * Math.cos( 2.38850746748 +      214.57111982520*t);
      saturn_x_0+=     0.00000134225 * Math.cos( 5.65869864230 +        4.66586644600*t);
      saturn_x_0+=     0.00000122431 * Math.cos( 1.70605535564 +      621.73803904930*t);
      saturn_x_0+=     0.00000116811 * Math.cos( 1.61145832221 +      113.38771495710*t);
      saturn_x_0+=     0.00000118860 * Math.cos( 5.65033188726 +     1891.23767093880*t);
      saturn_x_0+=     0.00000156141 * Math.cos( 0.65756469165 +      237.67811782620*t);
      saturn_x_0+=     0.00000111031 * Math.cos( 1.01598464494 +      206.13736432740*t);
      saturn_x_0+=     0.00000117765 * Math.cos( 3.75859584496 +       32.24332891440*t);
      saturn_x_0+=     0.00000129033 * Math.cos( 1.46198971089 +      247.23934538180*t);
      saturn_x_0+=     0.00000109102 * Math.cos( 5.47152854194 +      114.39910691340*t);
      saturn_x_0+=     0.00000108637 * Math.cos( 1.81623475388 +      767.36908292080*t);
      saturn_x_0+=     0.00000128773 * Math.cos( 2.33422964044 +       78.71375183040*t);
      saturn_x_0+=     0.00000105318 * Math.cos( 5.22706552130 +        5.62907429250*t);
      saturn_x_0+=     0.00000127653 * Math.cos( 5.12749160961 +      134.58534360760*t);
      saturn_x_0+=     0.00000126069 * Math.cos( 4.37180806356 +      181.05576652360*t);
      saturn_x_0+=     0.00000102853 * Math.cos( 1.65813839227 +       67.66805156650*t);
      saturn_x_0+=     0.00000133601 * Math.cos( 2.75004967414 +       35.42472265210*t);
      saturn_x_0+=     0.00000110253 * Math.cos( 0.71569456242 +      245.54242435240*t);
      saturn_x_0+=     0.00000105830 * Math.cos( 1.45649128193 +      219.89137757700*t);
      saturn_x_0+=     0.00000106045 * Math.cos( 4.18483284486 +      206.23373254700*t);
      saturn_x_0+=     0.00000104371 * Math.cos( 4.03317054662 +     1073.60902419080*t);
      saturn_x_0+=     0.00000103745 * Math.cos( 4.30393732262 +     1361.54670584420*t);
      saturn_x_0+=     0.00000118241 * Math.cos( 2.14057046058 +     1272.68102562720*t);
      saturn_x_0+=     0.00000112266 * Math.cos( 0.59751798783 +     1692.16566950240*t);
      saturn_x_0+=     0.00000100403 * Math.cos( 3.54166586397 +      140.00196957900*t);

      let saturn_x_1=0.0;
      saturn_x_1+=     0.07575103962 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_x_1+=     0.03085041716 * Math.cos( 4.27565749128 +      426.59819087600*t);
      saturn_x_1+=     0.02714918399 * Math.cos( 5.85229412397 +      206.18554843720*t);
      saturn_x_1+=     0.02643100909 * Math.cos( 5.33291950584 +      220.41264243880*t);
      saturn_x_1+=     0.00627104520 * Math.cos( 0.32898307969 +        7.11354700080*t);
      saturn_x_1+=     0.00256560953 * Math.cos( 3.52478934343 +      639.89728631400*t);
      saturn_x_1+=     0.00312356512 * Math.cos( 4.83001724941 +      419.48464387520*t);
      saturn_x_1+=     0.00189196274 * Math.cos( 4.48642453552 +      433.71173787680*t);
      saturn_x_1+=     0.00203646570 * Math.cos( 1.10998681782 +      213.29909543800*t);
      saturn_x_1+=     0.00119531145 * Math.cos( 1.14735096078 +      110.20632121940*t);
      saturn_x_1+=     0.00066764238 * Math.cos( 3.72346596928 +      316.39186965660*t);
      saturn_x_1+=     0.00066901225 * Math.cos( 5.20257500380 +      227.52618943960*t);
      saturn_x_1+=     0.00031000840 * Math.cos( 6.06067919437 +      199.07200143640*t);
      saturn_x_1+=     0.00030418100 * Math.cos( 0.18746903351 +       14.22709400160*t);
      saturn_x_1+=     0.00022275210 * Math.cos( 6.19530878014 +      103.09277421860*t);
      saturn_x_1+=     0.00018939377 * Math.cos( 2.77618306725 +      853.19638175200*t);
      saturn_x_1+=     0.00018093009 * Math.cos( 5.09162723865 +      209.36694217490*t);
      saturn_x_1+=     0.00017777854 * Math.cos( 6.10381593351 +      217.23124870110*t);
      saturn_x_1+=     0.00016296201 * Math.cos( 4.86945681437 +      216.48048917570*t);
      saturn_x_1+=     0.00017120250 * Math.cos( 4.59611664188 +      632.78373931320*t);
      saturn_x_1+=     0.00015894491 * Math.cos( 0.03653502304 +      210.11770170030*t);
      saturn_x_1+=     0.00016192653 * Math.cos( 5.60798014450 +      323.50541665740*t);
      saturn_x_1+=     0.00014466010 * Math.cos( 3.67449380090 +      647.01083331480*t);
      saturn_x_1+=     0.00011061528 * Math.cos( 0.03163071461 +      117.31986822020*t);
      saturn_x_1+=     0.00009873183 * Math.cos( 5.20065307357 +      202.25339517410*t);
      saturn_x_1+=     0.00008707608 * Math.cos( 6.03511731637 +      224.34479570190*t);
      saturn_x_1+=     0.00005499109 * Math.cos( 4.40350603415 +      440.82528487760*t);
      saturn_x_1+=     0.00005512222 * Math.cos( 2.60556642348 +       11.04570026390*t);
      saturn_x_1+=     0.00004008257 * Math.cos( 1.48942966807 +      522.57741809380*t);
      saturn_x_1+=     0.00003571196 * Math.cos( 5.10821908379 +      412.37109687440*t);
      saturn_x_1+=     0.00002731381 * Math.cos( 4.10892223660 +      149.56319713460*t);
      saturn_x_1+=     0.00002763786 * Math.cos( 3.96253590209 +       95.97922721780*t);
      saturn_x_1+=     0.00001875862 * Math.cos( 2.52384080586 +        3.93215326310*t);
      saturn_x_1+=     0.00001765816 * Math.cos( 0.75684544353 +      277.03499374140*t);
      saturn_x_1+=     0.00001688957 * Math.cos( 3.98270950731 +      422.66603761290*t);
      saturn_x_1+=     0.00001544787 * Math.cos( 5.30283923836 +      330.61896365820*t);
      saturn_x_1+=     0.00001449143 * Math.cos( 6.26507179861 +      529.69096509460*t);
      saturn_x_1+=     0.00001395551 * Math.cos( 2.03533642541 +     1066.49547719000*t);
      saturn_x_1+=     0.00001330413 * Math.cos( 5.06312203212 +      234.63973644040*t);
      saturn_x_1+=     0.00001511648 * Math.cos( 6.23274598777 +        3.18139373770*t);
      saturn_x_1+=     0.00001271050 * Math.cos( 2.40338468675 +      415.55249061210*t);
      saturn_x_1+=     0.00001171680 * Math.cos( 4.59341412127 +      536.80451209540*t);
      saturn_x_1+=     0.00001129056 * Math.cos( 5.45794529295 +      423.41679713830*t);
      saturn_x_1+=     0.00001126400 * Math.cos( 2.88173213734 +      860.30992875280*t);
      saturn_x_1+=     0.00001101245 * Math.cos( 4.07698108824 +      429.77958461370*t);
      saturn_x_1+=     0.00001273315 * Math.cos( 0.09572429396 +      742.99006053260*t);
      saturn_x_1+=     0.00001342277 * Math.cos( 2.98929557875 +      210.85141488320*t);
      saturn_x_1+=     0.00001331045 * Math.cos( 1.90899526877 +      215.74677599280*t);
      saturn_x_1+=     0.00000959849 * Math.cos( 0.92675530269 +      838.96928775040*t);
      saturn_x_1+=     0.00000961568 * Math.cos( 4.48936457741 +      846.08283475120*t);
      saturn_x_1+=     0.00000882604 * Math.cos( 5.41464304432 +      437.64389113990*t);
      saturn_x_1+=     0.00000926410 * Math.cos( 1.35857315584 +      625.67019231240*t);
      saturn_x_1+=     0.00000820497 * Math.cos( 4.74555084219 +      223.59403617650*t);
      saturn_x_1+=     0.00000767156 * Math.cos( 6.23090265966 +     1059.38193018920*t);
      saturn_x_1+=     0.00000811096 * Math.cos( 0.03213863705 +       21.34064100240*t);
      saturn_x_1+=     0.00000718572 * Math.cos( 6.12727675623 +      430.53034413910*t);
      saturn_x_1+=     0.00000625842 * Math.cos( 3.88265851906 +       88.86568021700*t);
      saturn_x_1+=     0.00000608389 * Math.cos( 2.50870660945 +      309.27832265580*t);
      saturn_x_1+=     0.00000551394 * Math.cos( 1.55261956835 +      515.46387109300*t);
      saturn_x_1+=     0.00000596169 * Math.cos( 5.09975163823 +      124.43341522100*t);
      saturn_x_1+=     0.00000472201 * Math.cos( 3.60914985488 +      654.12438031560*t);
      saturn_x_1+=     0.00000465734 * Math.cos( 0.21394106678 +      203.00415469950*t);
      saturn_x_1+=     0.00000456065 * Math.cos( 1.11956024618 +      735.87651353180*t);
      saturn_x_1+=     0.00000401729 * Math.cos( 4.42679334519 +       85.82729883120*t);
      saturn_x_1+=     0.00000376922 * Math.cos( 3.71246802705 +       76.26607127560*t);
      saturn_x_1+=     0.00000339360 * Math.cos( 0.74274349867 +     1155.36115740700*t);
      saturn_x_1+=     0.00000340385 * Math.cos( 1.78611648518 +      302.16477565500*t);
      saturn_x_1+=     0.00000323376 * Math.cos( 0.09844912589 +      191.95845443560*t);
      saturn_x_1+=     0.00000339649 * Math.cos( 2.73823062550 +      217.96496188400*t);
      saturn_x_1+=     0.00000304968 * Math.cos( 0.18416896544 +      231.45834270270*t);
      saturn_x_1+=     0.00000314938 * Math.cos( 0.28470065322 +      728.76296653100*t);
      saturn_x_1+=     0.00000311511 * Math.cos( 2.36484349864 +      628.85158605010*t);
      saturn_x_1+=     0.00000311154 * Math.cos( 1.91113927732 +      942.06206196900*t);
      saturn_x_1+=     0.00000298227 * Math.cos( 2.16364374640 +      208.63322899200*t);
      saturn_x_1+=     0.00000270658 * Math.cos( 2.70265519361 +      288.08069400530*t);
      saturn_x_1+=     0.00000259894 * Math.cos( 0.87228358124 +       18.15924726470*t);
      saturn_x_1+=     0.00000334303 * Math.cos( 3.07818702918 +      203.73786788240*t);
      saturn_x_1+=     0.00000259515 * Math.cos( 6.01660018486 +       10.29494073850*t);
      saturn_x_1+=     0.00000264173 * Math.cos( 3.55307126150 +      362.86229257260*t);
      saturn_x_1+=     0.00000290607 * Math.cos( 1.81179534417 +      222.86032299360*t);
      saturn_x_1+=     0.00000214859 * Math.cos( 6.03196961182 +      207.88246946660*t);
      saturn_x_1+=     0.00000208996 * Math.cos( 5.16442120392 +      218.71572140940*t);
      saturn_x_1+=     0.00000208264 * Math.cos( 4.40981297916 +      408.43894361130*t);
      saturn_x_1+=     0.00000211170 * Math.cos( 2.12698775082 +      138.51749687070*t);
      saturn_x_1+=     0.00000195809 * Math.cos( 0.35649768849 +       52.69019803950*t);
      saturn_x_1+=     0.00000190687 * Math.cos( 6.22000152508 +      200.76892246580*t);
      saturn_x_1+=     0.00000188529 * Math.cos( 0.45283523313 +      340.77089204480*t);
      saturn_x_1+=     0.00000171733 * Math.cos( 1.12897848901 +      831.85574074960*t);
      saturn_x_1+=     0.00000170838 * Math.cos( 1.17439205178 +      350.33211960040*t);
      saturn_x_1+=     0.00000167203 * Math.cos( 5.00292045290 +      225.82926841020*t);
      saturn_x_1+=     0.00000171646 * Math.cos( 2.30457163571 +      127.47179660680*t);
      saturn_x_1+=     0.00000177509 * Math.cos( 4.94085879824 +      210.37833413120*t);
      saturn_x_1+=     0.00000177688 * Math.cos( 6.22097530726 +      216.21985674480*t);
      saturn_x_1+=     0.00000162566 * Math.cos( 6.12524634729 +      956.28915597060*t);
      saturn_x_1+=     0.00000212499 * Math.cos( 5.39034664048 +      949.17560896980*t);
      saturn_x_1+=     0.00000163339 * Math.cos( 1.48827637108 +      195.13984817330*t);
      saturn_x_1+=     0.00000149570 * Math.cos( 0.31719520948 +        9.56122755560*t);
      saturn_x_1+=     0.00000177151 * Math.cos( 6.26962608163 +      160.60889739850*t);
      saturn_x_1+=     0.00000170347 * Math.cos( 2.63698505108 +      207.67002114550*t);
      saturn_x_1+=     0.00000140654 * Math.cos( 0.48104293652 +     1471.75302706360*t);
      saturn_x_1+=     0.00000150812 * Math.cos( 3.13878111760 +      635.96513305090*t);
      saturn_x_1+=     0.00000136646 * Math.cos( 4.51630236837 +      543.91805909620*t);
      saturn_x_1+=     0.00000163889 * Math.cos( 2.23920379694 +      218.92816973050*t);
      saturn_x_1+=     0.00000164968 * Math.cos( 4.62059482677 +       22.09140052780*t);
      saturn_x_1+=     0.00000145469 * Math.cos( 4.63713942585 +      265.98929347750*t);
      saturn_x_1+=     0.00000134755 * Math.cos( 3.92461654777 +      750.10360753340*t);
      saturn_x_1+=     0.00000133754 * Math.cos( 1.25928209722 +      703.63318461740*t);
      saturn_x_1+=     0.00000152766 * Math.cos( 4.26935902156 +       56.62235130260*t);
      saturn_x_1+=     0.00000137507 * Math.cos( 1.65880730547 +     1258.45393162560*t);
      saturn_x_1+=     0.00000125541 * Math.cos( 4.29077908509 +      447.93883187840*t);
      saturn_x_1+=     0.00000140716 * Math.cos( 4.40833694034 +      142.44965013380*t);
      saturn_x_1+=     0.00000146194 * Math.cos( 4.20275390128 +       70.84944530420*t);
      saturn_x_1+=     0.00000134558 * Math.cos( 0.84258328591 +      490.33408917940*t);
      saturn_x_1+=     0.00000117954 * Math.cos( 2.15227719526 +      618.55664531160*t);
      saturn_x_1+=     0.00000106790 * Math.cos( 2.74587720126 +      565.11568774670*t);
      saturn_x_1+=     0.00000105456 * Math.cos( 3.58458171176 +      209.10630974400*t);
      saturn_x_1+=     0.00000123096 * Math.cos( 2.84869686434 +      483.22054217860*t);
      saturn_x_1+=     0.00000104216 * Math.cos( 1.30367057574 +      217.49188113200*t);
      saturn_x_1+=     0.00000108048 * Math.cos( 6.25104484742 +     1045.15483618760*t);
      saturn_x_1+=     0.00000103680 * Math.cos( 0.13827521003 +      106.27416795630*t);
      saturn_x_1+=     0.00000122664 * Math.cos( 1.73647954150 +       12.53017297220*t);
      saturn_x_1+=     0.00000107530 * Math.cos( 2.04781654923 +      424.15051032120*t);
      saturn_x_1+=     0.00000111568 * Math.cos( 3.50500638623 +      269.92144674060*t);
      saturn_x_1=saturn_x_1 * t;

      let saturn_x_2=0.0;
      saturn_x_2+=     0.00560746334 * Math.cos( 1.26401632282 +      206.18554843720*t);
      saturn_x_2+=     0.00545834518 * Math.cos( 3.62343709657 +      220.41264243880*t);
      saturn_x_2+=     0.00443342186 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_x_2+=     0.00336109713 * Math.cos( 2.42547432460 +      213.29909543800*t);
      saturn_x_2+=     0.00224302269 * Math.cos( 2.49151203519 +      426.59819087600*t);
      saturn_x_2+=     0.00087170924 * Math.cos( 4.89048951691 +        7.11354700080*t);
      saturn_x_2+=     0.00050028094 * Math.cos( 2.70119046081 +      433.71173787680*t);
      saturn_x_2+=     0.00045122590 * Math.cos( 0.36735068943 +      419.48464387520*t);
      saturn_x_2+=     0.00032847824 * Math.cos( 1.59210153669 +      639.89728631400*t);
      saturn_x_2+=     0.00027153555 * Math.cos( 3.49804002218 +      227.52618943960*t);
      saturn_x_2+=     0.00012676167 * Math.cos( 1.45465729530 +      199.07200143640*t);
      saturn_x_2+=     0.00010330738 * Math.cos( 4.76949531290 +       14.22709400160*t);
      saturn_x_2+=     0.00007249149 * Math.cos( 5.70264553247 +      110.20632121940*t);
      saturn_x_2+=     0.00004653214 * Math.cos( 1.83710048213 +      647.01083331480*t);
      saturn_x_2+=     0.00004923585 * Math.cos( 3.08463039042 +      216.48048917570*t);
      saturn_x_2+=     0.00004777358 * Math.cos( 1.81695155349 +      210.11770170030*t);
      saturn_x_2+=     0.00004166633 * Math.cos( 5.32887874226 +      316.39186965660*t);
      saturn_x_2+=     0.00003508385 * Math.cos( 0.78251653369 +      853.19638175200*t);
      saturn_x_2+=     0.00002660470 * Math.cos( 3.16731393212 +      209.36694217490*t);
      saturn_x_2+=     0.00002538027 * Math.cos( 2.65097612407 +      440.82528487760*t);
      saturn_x_2+=     0.00002568114 * Math.cos( 1.74024228572 +      217.23124870110*t);
      saturn_x_2+=     0.00002503277 * Math.cos( 4.69450368911 +      117.31986822020*t);
      saturn_x_2+=     0.00002506986 * Math.cos( 1.74781817701 +      103.09277421860*t);
      saturn_x_2+=     0.00002129256 * Math.cos( 0.28453141367 +      632.78373931320*t);
      saturn_x_2+=     0.00001841989 * Math.cos( 3.99269872894 +      323.50541665740*t);
      saturn_x_2+=     0.00001228511 * Math.cos( 0.42906039519 +      412.37109687440*t);
      saturn_x_2+=     0.00000804732 * Math.cos( 3.35740706049 +      234.63973644040*t);
      saturn_x_2+=     0.00000796407 * Math.cos( 1.09483823163 +      202.25339517410*t);
      saturn_x_2+=     0.00000545426 * Math.cos( 5.78793713141 +       95.97922721780*t);
      saturn_x_2+=     0.00000732525 * Math.cos( 3.86150260922 +      224.34479570190*t);
      saturn_x_2+=     0.00000440358 * Math.cos( 3.59840290265 +      330.61896365820*t);
      saturn_x_2+=     0.00000426791 * Math.cos( 1.00483231522 +      860.30992875280*t);
      saturn_x_2+=     0.00000391974 * Math.cos( 0.69006482495 +       11.04570026390*t);
      saturn_x_2+=     0.00000455657 * Math.cos( 3.49866480518 +      522.57741809380*t);
      saturn_x_2+=     0.00000440217 * Math.cos( 4.62429695267 +       21.34064100240*t);
      saturn_x_2+=     0.00000403719 * Math.cos( 2.95386471404 +      223.59403617650*t);
      saturn_x_2+=     0.00000399321 * Math.cos( 2.21962287963 +      429.77958461370*t);
      saturn_x_2+=     0.00000456586 * Math.cos( 5.31237952032 +      529.69096509460*t);
      saturn_x_2+=     0.00000337931 * Math.cos( 0.01742527415 +     1066.49547719000*t);
      saturn_x_2+=     0.00000306480 * Math.cos( 4.44235835495 +        3.18139373770*t);
      saturn_x_2+=     0.00000353827 * Math.cos( 2.08574838147 +      422.66603761290*t);
      saturn_x_2+=     0.00000277766 * Math.cos( 3.99263414764 +        3.93215326310*t);
      saturn_x_2+=     0.00000266087 * Math.cos( 1.10605005957 +      423.41679713830*t);
      saturn_x_2+=     0.00000244552 * Math.cos( 1.81855172211 +      654.12438031560*t);
      saturn_x_2+=     0.00000252757 * Math.cos( 5.58633314063 +       88.86568021700*t);
      saturn_x_2+=     0.00000263461 * Math.cos( 3.32945622126 +      124.43341522100*t);
      saturn_x_2+=     0.00000198166 * Math.cos( 1.75391782582 +      191.95845443560*t);
      saturn_x_2+=     0.00000193213 * Math.cos( 2.35512750520 +      149.56319713460*t);
      saturn_x_2+=     0.00000223879 * Math.cos( 2.03081321297 +      203.00415469950*t);
      saturn_x_2+=     0.00000168136 * Math.cos( 2.77171654378 +      536.80451209540*t);
      saturn_x_2+=     0.00000194617 * Math.cos( 2.64597558735 +      625.67019231240*t);
      saturn_x_2+=     0.00000163324 * Math.cos( 3.33300066749 +      515.46387109300*t);
      saturn_x_2+=     0.00000165093 * Math.cos( 4.45996436178 +      742.99006053260*t);
      saturn_x_2+=     0.00000132687 * Math.cos( 3.18963228913 +      302.16477565500*t);
      saturn_x_2+=     0.00000171957 * Math.cos( 1.26865256659 +      309.27832265580*t);
      saturn_x_2+=     0.00000117070 * Math.cos( 2.50733253747 +      277.03499374140*t);
      saturn_x_2+=     0.00000105122 * Math.cos( 4.21584969999 +       10.29494073850*t);
      saturn_x_2+=     0.00000123227 * Math.cos( 3.28227189007 +      437.64389113990*t);
      saturn_x_2+=     0.00000125141 * Math.cos( 2.95191338477 +      735.87651353180*t);
      saturn_x_2=saturn_x_2 * t * t;

      let saturn_x_3=0.0;
      saturn_x_3+=     0.00077115952 * Math.cos( 2.97714385362 +      206.18554843720*t);
      saturn_x_3+=     0.00075340436 * Math.cos( 1.89208005248 +      220.41264243880*t);
      saturn_x_3+=     0.00018450895 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_x_3+=     0.00010527244 * Math.cos( 0.66368256891 +      426.59819087600*t);
      saturn_x_3+=     0.00008994946 * Math.cos( 0.91696559755 +      433.71173787680*t);
      saturn_x_3+=     0.00007403594 * Math.cos( 1.78627385870 +      227.52618943960*t);
      saturn_x_3+=     0.00008045160 * Math.cos( 3.12864412887 +        7.11354700080*t);
      saturn_x_3+=     0.00004505149 * Math.cos( 2.24531319187 +      419.48464387520*t);
      saturn_x_3+=     0.00003468010 * Math.cos( 3.14590544446 +      199.07200143640*t);
      saturn_x_3+=     0.00002974601 * Math.cos( 6.00030641555 +      639.89728631400*t);
      saturn_x_3+=     0.00002342089 * Math.cos( 3.06091771643 +       14.22709400160*t);
      saturn_x_3+=     0.00001230715 * Math.cos( 4.38196130069 +      213.29909543800*t);
      saturn_x_3+=     0.00001023888 * Math.cos( 0.01138655869 +      647.01083331480*t);
      saturn_x_3+=     0.00000788529 * Math.cos( 0.89850292553 +      440.82528487760*t);
      saturn_x_3+=     0.00000806346 * Math.cos( 1.28205831043 +      216.48048917570*t);
      saturn_x_3+=     0.00000768731 * Math.cos( 3.61309275908 +      210.11770170030*t);
      saturn_x_3+=     0.00000384249 * Math.cos( 3.06233558203 +      117.31986822020*t);
      saturn_x_3+=     0.00000431624 * Math.cos( 3.77909555661 +      110.20632121940*t);
      saturn_x_3+=     0.00000456158 * Math.cos( 5.14235391148 +      853.19638175200*t);
      saturn_x_3+=     0.00000323749 * Math.cos( 1.65135986090 +      234.63973644040*t);
      saturn_x_3+=     0.00000279312 * Math.cos( 2.09194739376 +      412.37109687440*t);
      saturn_x_3+=     0.00000242325 * Math.cos( 3.37263291828 +      103.09277421860*t);
      saturn_x_3+=     0.00000194820 * Math.cos( 0.79561075453 +      316.39186965660*t);
      saturn_x_3+=     0.00000197473 * Math.cos( 2.29502750567 +      632.78373931320*t);
      saturn_x_3+=     0.00000153539 * Math.cos( 2.32058023635 +      323.50541665740*t);
      saturn_x_3+=     0.00000153890 * Math.cos( 2.88170193491 +       21.34064100240*t);
      saturn_x_3+=     0.00000125210 * Math.cos( 1.45557479064 +      209.36694217490*t);
      saturn_x_3+=     0.00000112760 * Math.cos( 3.40679000015 +      217.23124870110*t);
      saturn_x_3+=     0.00000111243 * Math.cos( 5.41745722736 +      860.30992875280*t);
      saturn_x_3+=     0.00000114540 * Math.cos( 1.16490445103 +      223.59403617650*t);
      saturn_x_3=saturn_x_3 * t * t * t;

      let saturn_x_4=0.0;
      saturn_x_4+=     0.00007959921 * Math.cos( 4.70523623364 +      206.18554843720*t);
      saturn_x_4+=     0.00007836652 * Math.cos( 0.13981693631 +      220.41264243880*t);
      saturn_x_4+=     0.00001511196 * Math.cos( 0.06561560462 +      227.52618943960*t);
      saturn_x_4+=     0.00001223066 * Math.cos( 5.41618485361 +      433.71173787680*t);
      saturn_x_4+=     0.00000702780 * Math.cos( 4.84941923986 +      199.07200143640*t);
      saturn_x_4+=     0.00000861569 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_x_4+=     0.00000550606 * Math.cos( 1.37376296077 +        7.11354700080*t);
      saturn_x_4+=     0.00000353954 * Math.cos( 4.14510701125 +      419.48464387520*t);
      saturn_x_4+=     0.00000386476 * Math.cos( 1.33814676867 +       14.22709400160*t);
      saturn_x_4+=     0.00000386632 * Math.cos( 5.00698289959 +      426.59819087600*t);
      saturn_x_4+=     0.00000185617 * Math.cos( 5.43394463245 +      440.82528487760*t);
      saturn_x_4+=     0.00000208917 * Math.cos( 4.14160968677 +      639.89728631400*t);
      saturn_x_4+=     0.00000171842 * Math.cos( 4.47453630580 +      647.01083331480*t);
      saturn_x_4+=     0.00000107628 * Math.cos( 3.12066785242 +      213.29909543800*t);
      saturn_x_4=saturn_x_4 * t * t * t * t;

      let saturn_x_5=0.0;
      saturn_x_5+=     0.00000589250 * Math.cos( 0.13910544483 +      206.18554843720*t);
      saturn_x_5+=     0.00000585873 * Math.cos( 4.66559223624 +      220.41264243880*t);
      saturn_x_5+=     0.00000225585 * Math.cos( 4.60652710308 +      227.52618943960*t);
      saturn_x_5+=     0.00000130928 * Math.cos( 3.62464025902 +      433.71173787680*t);
      saturn_x_5=saturn_x_5 * t * t * t * t * t;

      return saturn_x_0+saturn_x_1+saturn_x_2+saturn_x_3+saturn_x_4+saturn_x_5;
   }

   static saturn_y(t){
      let saturn_y_0=0.0;
      saturn_y_0+=     9.52986882699 * Math.cos( 5.58600556665 +      213.29909543800*t);
      saturn_y_0+=     0.79387988806 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_y_0+=     0.26441781302 * Math.cos( 4.83528061849 +      426.59819087600*t);
      saturn_y_0+=     0.06916653915 * Math.cos( 2.55279408706 +      206.18554843720*t);
      saturn_y_0+=     0.06633570703 * Math.cos( 5.46258848288 +      220.41264243880*t);
      saturn_y_0+=     0.02345609742 * Math.cos( 0.44652132519 +        7.11354700080*t);
      saturn_y_0+=     0.01183874652 * Math.cos( 1.34638298371 +      419.48464387520*t);
      saturn_y_0+=     0.01245790434 * Math.cos( 0.60367177975 +      110.20632121940*t);
      saturn_y_0+=     0.01098751131 * Math.cos( 4.08608782813 +      639.89728631400*t);
      saturn_y_0+=     0.00700849336 * Math.cos( 1.13611298025 +      316.39186965660*t);
      saturn_y_0+=     0.00434466176 * Math.cos( 5.42474696262 +      529.69096509460*t);
      saturn_y_0+=     0.00373327342 * Math.cos( 4.71308726958 +      433.71173787680*t);
      saturn_y_0+=     0.00335162363 * Math.cos( 0.66422253983 +      103.09277421860*t);
      saturn_y_0+=     0.00097837745 * Math.cos( 5.72844290173 +      323.50541665740*t);
      saturn_y_0+=     0.00080571808 * Math.cos( 4.05295449910 +       11.04570026390*t);
      saturn_y_0+=     0.00083899691 * Math.cos( 5.33204070267 +      227.52618943960*t);
      saturn_y_0+=     0.00070158491 * Math.cos( 5.59777963629 +      209.36694217490*t);
      saturn_y_0+=     0.00065937657 * Math.cos( 1.25969608208 +      202.25339517410*t);
      saturn_y_0+=     0.00070957225 * Math.cos( 0.88888207567 +      632.78373931320*t);
      saturn_y_0+=     0.00068985859 * Math.cos( 2.44460312617 +      217.23124870110*t);
      saturn_y_0+=     0.00058382264 * Math.cos( 0.58978766922 +      224.34479570190*t);
      saturn_y_0+=     0.00054049836 * Math.cos( 3.33757904879 +      853.19638175200*t);
      saturn_y_0+=     0.00045790930 * Math.cos( 0.30331527632 +       14.22709400160*t);
      saturn_y_0+=     0.00041976402 * Math.cos( 2.62591355948 +      199.07200143640*t);
      saturn_y_0+=     0.00044697175 * Math.cos( 0.90661238256 +       63.73589830340*t);
      saturn_y_0+=     0.00025199575 * Math.cos( 5.08963506006 +      216.48048917570*t);
      saturn_y_0+=     0.00024640836 * Math.cos( 2.95445247282 +      210.11770170030*t);
      saturn_y_0+=     0.00024835151 * Math.cos( 4.02630190571 +      415.55249061210*t);
      saturn_y_0+=     0.00025545907 * Math.cos( 0.06626229252 +      117.31986822020*t);
      saturn_y_0+=     0.00029666833 * Math.cos( 6.09910638345 +      735.87651353180*t);
      saturn_y_0+=     0.00023396742 * Math.cos( 3.96337393635 +      647.01083331480*t);
      saturn_y_0+=     0.00023380691 * Math.cos( 4.90051072276 +      149.56319713460*t);
      saturn_y_0+=     0.00020272215 * Math.cos( 2.34319548198 +      309.27832265580*t);
      saturn_y_0+=     0.00020099552 * Math.cos( 0.98365186365 +      522.57741809380*t);
      saturn_y_0+=     0.00024827950 * Math.cos( 3.92681428900 +       74.78159856730*t);
      saturn_y_0+=     0.00015383927 * Math.cos( 3.10227822627 +      277.03499374140*t);
      saturn_y_0+=     0.00011629210 * Math.cos( 5.74108283772 +     1059.38193018920*t);
      saturn_y_0+=     0.00012422966 * Math.cos( 2.62557865743 +      490.33408917940*t);
      saturn_y_0+=     0.00012048048 * Math.cos( 4.09265980116 +      351.81659230870*t);
      saturn_y_0+=     0.00009551796 * Math.cos( 3.48788042094 +       95.97922721780*t);
      saturn_y_0+=     0.00007670379 * Math.cos( 1.16594276164 +      742.99006053260*t);
      saturn_y_0+=     0.00006919946 * Math.cos( 1.17090063883 +      412.37109687440*t);
      saturn_y_0+=     0.00009034877 * Math.cos( 5.86816144198 +     1052.26838318840*t);
      saturn_y_0+=     0.00006536751 * Math.cos( 0.84246459392 +      838.96928775040*t);
      saturn_y_0+=     0.00006082097 * Math.cos( 4.58758280729 +      440.82528487760*t);
      saturn_y_0+=     0.00005027211 * Math.cos( 0.93213690546 +      846.08283475120*t);
      saturn_y_0+=     0.00004838146 * Math.cos( 4.98563812475 +      536.80451209540*t);
      saturn_y_0+=     0.00005768897 * Math.cos( 3.73776690402 +       38.13303563780*t);
      saturn_y_0+=     0.00005201849 * Math.cos( 2.97482802430 +      210.85141488320*t);
      saturn_y_0+=     0.00005156578 * Math.cos( 5.05796998564 +      215.74677599280*t);
      saturn_y_0+=     0.00003792348 * Math.cos( 4.41806046981 +      422.66603761290*t);
      saturn_y_0+=     0.00003881104 * Math.cos( 3.38026646963 +        3.93215326310*t);
      saturn_y_0+=     0.00003768751 * Math.cos( 2.14954247360 +      212.33588759150*t);
      saturn_y_0+=     0.00003752010 * Math.cos( 5.88125434018 +      214.26230328450*t);
      saturn_y_0+=     0.00003118938 * Math.cos( 5.55799397159 +      213.25091132820*t);
      saturn_y_0+=     0.00003118056 * Math.cos( 2.47259780102 +      213.34727954780*t);
      saturn_y_0+=     0.00003815691 * Math.cos( 2.44166851155 +      625.67019231240*t);
      saturn_y_0+=     0.00004042463 * Math.cos( 1.24471211016 +      137.03302416240*t);
      saturn_y_0+=     0.00002829944 * Math.cos( 5.44434225998 +      330.61896365820*t);
      saturn_y_0+=     0.00003367270 * Math.cos( 6.13298847057 +      437.64389113990*t);
      saturn_y_0+=     0.00002891352 * Math.cos( 5.85313497106 +       85.82729883120*t);
      saturn_y_0+=     0.00002774595 * Math.cos( 5.61594351302 +      203.73786788240*t);
      saturn_y_0+=     0.00002638715 * Math.cos( 3.83678156812 +      288.08069400530*t);
      saturn_y_0+=     0.00003171680 * Math.cos( 4.19553075395 +       76.26607127560*t);
      saturn_y_0+=     0.00002532374 * Math.cos( 3.52629372341 +      628.85158605010*t);
      saturn_y_0+=     0.00002533632 * Math.cos( 3.89788590926 +      138.51749687070*t);
      saturn_y_0+=     0.00002982174 * Math.cos( 2.58535107213 +     1066.49547719000*t);
      saturn_y_0+=     0.00002620642 * Math.cos( 0.69751279148 +      127.47179660680*t);
      saturn_y_0+=     0.00002501775 * Math.cos( 6.19929274396 +        9.56122755560*t);
      saturn_y_0+=     0.00002448467 * Math.cos( 0.54179432209 +     1155.36115740700*t);
      saturn_y_0+=     0.00002431496 * Math.cos( 2.40122451395 +      222.86032299360*t);
      saturn_y_0+=     0.00003138628 * Math.cos( 5.63058455924 +     1368.66025284500*t);
      saturn_y_0+=     0.00002269226 * Math.cos( 2.12401905105 +      430.53034413910*t);
      saturn_y_0+=     0.00002078049 * Math.cos( 1.95682348964 +      423.41679713830*t);
      saturn_y_0+=     0.00002670750 * Math.cos( 0.18165311734 +        3.18139373770*t);
      saturn_y_0+=     0.00002339764 * Math.cos( 4.29619053852 +      388.46515523820*t);
      saturn_y_0+=     0.00001636580 * Math.cos( 2.97440139727 +       12.53017297220*t);
      saturn_y_0+=     0.00001639181 * Math.cos( 0.62823227849 +      212.77783057620*t);
      saturn_y_0+=     0.00001634235 * Math.cos( 1.12043073218 +      213.82036029980*t);
      saturn_y_0+=     0.00001499665 * Math.cos( 5.16865990579 +       52.69019803950*t);
      saturn_y_0+=     0.00001462908 * Math.cos( 4.35285690993 +      429.77958461370*t);
      saturn_y_0+=     0.00001678952 * Math.cos( 2.07211719214 +      949.17560896980*t);
      saturn_y_0+=     0.00001989253 * Math.cos( 0.42496478369 +        1.48447270830*t);
      saturn_y_0+=     0.00001540242 * Math.cos( 3.21449770483 +      860.30992875280*t);
      saturn_y_0+=     0.00001437063 * Math.cos( 3.84293543293 +      350.33211960040*t);
      saturn_y_0+=     0.00001276377 * Math.cos( 2.98728987770 +      340.77089204480*t);
      saturn_y_0+=     0.00001152164 * Math.cos( 1.78736848302 +      942.06206196900*t);
      saturn_y_0+=     0.00001112617 * Math.cos( 5.19114183145 +      234.63973644040*t);
      saturn_y_0+=     0.00001011023 * Math.cos( 0.27242160432 +     1471.75302706360*t);
      saturn_y_0+=     0.00001162807 * Math.cos( 2.35040840317 +      200.76892246580*t);
      saturn_y_0+=     0.00001091025 * Math.cos( 4.25638370205 +      362.86229257260*t);
      saturn_y_0+=     0.00001090678 * Math.cos( 5.85086226218 +      173.94221952280*t);
      saturn_y_0+=     0.00000979441 * Math.cos( 4.38030362500 +     1162.47470440780*t);
      saturn_y_0+=     0.00001186647 * Math.cos( 5.38323620554 +     1685.05212250160*t);
      saturn_y_0+=     0.00000870366 * Math.cos( 1.66373573347 +      210.37833413120*t);
      saturn_y_0+=     0.00001120819 * Math.cos( 1.89478696683 +      703.63318461740*t);
      saturn_y_0+=     0.00000868815 * Math.cos( 0.08028652697 +      216.21985674480*t);
      saturn_y_0+=     0.00000831989 * Math.cos( 5.29292222262 +      212.54833591260*t);
      saturn_y_0+=     0.00000825849 * Math.cos( 2.73629728926 +      214.04985496340*t);
      saturn_y_0+=     0.00000880943 * Math.cos( 6.17830049665 +      209.10630974400*t);
      saturn_y_0+=     0.00000867622 * Math.cos( 1.84353750811 +      217.49188113200*t);
      saturn_y_0+=     0.00000789747 * Math.cos( 4.95200793900 +      223.59403617650*t);
      saturn_y_0+=     0.00000787760 * Math.cos( 1.09636920769 +      515.46387109300*t);
      saturn_y_0+=     0.00001008898 * Math.cos( 5.80110302450 +      225.82926841020*t);
      saturn_y_0+=     0.00000852348 * Math.cos( 3.77492026990 +       88.86568021700*t);
      saturn_y_0+=     0.00000919742 * Math.cos( 3.29098397009 +      565.11568774670*t);
      saturn_y_0+=     0.00000861896 * Math.cos( 2.13214810643 +      252.65597135320*t);
      saturn_y_0+=     0.00000707797 * Math.cos( 1.00092256988 +     1265.56747862640*t);
      saturn_y_0+=     0.00000935830 * Math.cos( 2.78325753863 +      302.16477565500*t);
      saturn_y_0+=     0.00000711560 * Math.cos( 1.83909913013 +      417.03696332040*t);
      saturn_y_0+=     0.00000918735 * Math.cos( 3.00604517701 +      563.63121503840*t);
      saturn_y_0+=     0.00000714428 * Math.cos( 5.61336775536 +      207.67002114550*t);
      saturn_y_0+=     0.00000686040 * Math.cos( 0.30753112959 +      956.28915597060*t);
      saturn_y_0+=     0.00000795907 * Math.cos( 0.44249466780 +      207.88246946660*t);
      saturn_y_0+=     0.00000664618 * Math.cos( 0.18239901113 +      479.28838891550*t);
      saturn_y_0+=     0.00000770829 * Math.cos( 1.32128949558 +      218.71572140940*t);
      saturn_y_0+=     0.00000693714 * Math.cos( 2.40549437556 +      218.92816973050*t);
      saturn_y_0+=     0.00000798909 * Math.cos( 6.06695893725 +       22.09140052780*t);
      saturn_y_0+=     0.00000835476 * Math.cos( 1.39152622883 +      160.60889739850*t);
      saturn_y_0+=     0.00000739834 * Math.cos( 6.27747531964 +      728.76296653100*t);
      saturn_y_0+=     0.00000594013 * Math.cos( 1.31598713165 +      265.98929347750*t);
      saturn_y_0+=     0.00000764611 * Math.cos( 0.14564177629 +       21.34064100240*t);
      saturn_y_0+=     0.00000581261 * Math.cos( 2.38872797383 +      554.06998748280*t);
      saturn_y_0+=     0.00000629049 * Math.cos( 1.22858809314 +       18.15924726470*t);
      saturn_y_0+=     0.00000702089 * Math.cos( 1.97508934614 +       62.25142559510*t);
      saturn_y_0+=     0.00000698631 * Math.cos( 5.28259133162 +      124.43341522100*t);
      saturn_y_0+=     0.00000614460 * Math.cos( 2.85212173127 +      217.96496188400*t);
      saturn_y_0+=     0.00000667918 * Math.cos( 1.25225067905 +      425.11371816770*t);
      saturn_y_0+=     0.00000581376 * Math.cos( 0.50782281722 +      231.45834270270*t);
      saturn_y_0+=     0.00000520344 * Math.cos( 5.09622518839 +      414.06801790380*t);
      saturn_y_0+=     0.00000519835 * Math.cos( 1.70911972460 +       99.16062095550*t);
      saturn_y_0+=     0.00000500788 * Math.cos( 1.47836685639 +     1258.45393162560*t);
      saturn_y_0+=     0.00000533532 * Math.cos( 0.96174816662 +      214.78356814630*t);
      saturn_y_0+=     0.00000483256 * Math.cos( 0.91737302115 +      408.43894361130*t);
      saturn_y_0+=     0.00000553256 * Math.cos( 5.17631306517 +      208.63322899200*t);
      saturn_y_0+=     0.00000629756 * Math.cos( 2.95386700663 +       65.22037101170*t);
      saturn_y_0+=     0.00000465386 * Math.cos( 3.05786362626 +      203.00415469950*t);
      saturn_y_0+=     0.00000528826 * Math.cos( 0.65918491217 +      211.81462272970*t);
      saturn_y_0+=     0.00000465526 * Math.cos( 3.83793669928 +      654.12438031560*t);
      saturn_y_0+=     0.00000503180 * Math.cos( 2.80008494039 +      251.43213107580*t);
      saturn_y_0+=     0.00000443674 * Math.cos( 0.00736496644 +     1788.14489672020*t);
      saturn_y_0+=     0.00000426214 * Math.cos( 6.01089625149 +     1589.07289528380*t);
      saturn_y_0+=     0.00000414514 * Math.cos( 2.06430786088 +      148.07872442630*t);
      saturn_y_0+=     0.00000454911 * Math.cos( 4.17704716573 +     1478.86657406440*t);
      saturn_y_0+=     0.00000398382 * Math.cos( 0.07909774752 +      213.41097002260*t);
      saturn_y_0+=     0.00000398382 * Math.cos( 1.66925524906 +      213.18722085340*t);
      saturn_y_0+=     0.00000473403 * Math.cos( 5.14050822265 +     2001.44399215820*t);
      saturn_y_0+=     0.00000358919 * Math.cos( 4.93878023673 +        2.44768055480*t);
      saturn_y_0+=     0.00000465061 * Math.cos( 1.45302862836 +      142.44965013380*t);
      saturn_y_0+=     0.00000376562 * Math.cos( 0.54829635117 +     1581.95934828300*t);
      saturn_y_0+=     0.00000341585 * Math.cos( 3.45264409045 +      198.32124191100*t);
      saturn_y_0+=     0.00000433316 * Math.cos( 3.20558404998 +      312.19908396260*t);
      saturn_y_0+=     0.00000350436 * Math.cos( 1.14513501672 +       98.89998852460*t);
      saturn_y_0+=     0.00000334759 * Math.cos( 2.28889729136 +      213.08664711690*t);
      saturn_y_0+=     0.00000334759 * Math.cos( 5.74264101239 +      213.51154375910*t);
      saturn_y_0+=     0.00000370173 * Math.cos( 3.82861856132 +      151.04766984290*t);
      saturn_y_0+=     0.00000357143 * Math.cos( 5.33211408348 +      175.16605980020*t);
      saturn_y_0+=     0.00000367605 * Math.cos( 4.36445046507 +      750.10360753340*t);
      saturn_y_0+=     0.00000319024 * Math.cos( 4.57593199965 +      228.27694896500*t);
      saturn_y_0+=     0.00000312590 * Math.cos( 0.96110658139 +      831.85574074960*t);
      saturn_y_0+=     0.00000306586 * Math.cos( 4.93996479979 +      195.13984817330*t);
      saturn_y_0+=     0.00000384780 * Math.cos( 4.14880260454 +       56.62235130260*t);
      saturn_y_0+=     0.00000421807 * Math.cos( 5.63268242725 +       70.84944530420*t);
      saturn_y_0+=     0.00000400030 * Math.cos( 2.71207125945 +      177.87437278590*t);
      saturn_y_0+=     0.00000327733 * Math.cos( 2.69309432564 +      191.95845443560*t);
      saturn_y_0+=     0.00000273993 * Math.cos( 5.98830026684 +      278.51946644970*t);
      saturn_y_0+=     0.00000270202 * Math.cos( 3.57098211820 +      635.96513305090*t);
      saturn_y_0+=     0.00000336412 * Math.cos( 3.29741235332 +      114.13847448250*t);
      saturn_y_0+=     0.00000269943 * Math.cos( 0.56914501964 +      327.43756992050*t);
      saturn_y_0+=     0.00000265070 * Math.cos( 4.06900450863 +      205.22234059070*t);
      saturn_y_0+=     0.00000348765 * Math.cos( 5.33112172130 +      248.72381809010*t);
      saturn_y_0+=     0.00000296845 * Math.cos( 6.22357485953 +       10.29494073850*t);
      saturn_y_0+=     0.00000251697 * Math.cos( 1.64343434992 +      213.03846300710*t);
      saturn_y_0+=     0.00000251697 * Math.cos( 0.10491824010 +      213.55972786890*t);
      saturn_y_0+=     0.00000253052 * Math.cos( 2.67224328276 +      404.50679034820*t);
      saturn_y_0+=     0.00000307227 * Math.cos( 5.83295899287 +      483.22054217860*t);
      saturn_y_0+=     0.00000236798 * Math.cos( 1.18644808787 +     1574.84580128220*t);
      saturn_y_0+=     0.00000251354 * Math.cos( 5.49027488511 +      191.20769491020*t);
      saturn_y_0+=     0.00000269096 * Math.cos( 6.08409110657 +     1045.15483618760*t);
      saturn_y_0+=     0.00000241616 * Math.cos( 4.17757086737 +      221.37585028530*t);
      saturn_y_0+=     0.00000247351 * Math.cos( 4.14967259359 +      275.55052103310*t);
      saturn_y_0+=     0.00000292774 * Math.cos( 2.29160155390 +      424.15051032120*t);
      saturn_y_0+=     0.00000273849 * Math.cos( 0.48976257091 +      106.27416795630*t);
      saturn_y_0+=     0.00000305045 * Math.cos( 0.18263234556 +     6283.07584999140*t);
      saturn_y_0+=     0.00000237397 * Math.cos( 3.38925999152 +      235.39049596580*t);
      saturn_y_0+=     0.00000211029 * Math.cos( 4.73396446560 +      543.91805909620*t);
      saturn_y_0+=     0.00000206826 * Math.cos( 2.89687953034 +      842.15068148810*t);
      saturn_y_0+=     0.00000232878 * Math.cos( 1.32938721664 +       39.35687591520*t);
      saturn_y_0+=     0.00000269270 * Math.cos( 1.92392937845 +      121.25202148330*t);
      saturn_y_0+=     0.00000202662 * Math.cos( 6.03169886301 +     2104.53676637680*t);
      saturn_y_0+=     0.00000230906 * Math.cos( 2.46511266784 +      497.44763618020*t);
      saturn_y_0+=     0.00000218872 * Math.cos( 0.86295345782 +        8.07675484730*t);
      saturn_y_0+=     0.00000203946 * Math.cos( 1.38528238326 +      284.14854074220*t);
      saturn_y_0+=     0.00000216481 * Math.cos( 4.58190569482 +      429.04587143080*t);
      saturn_y_0+=     0.00000240544 * Math.cos( 0.08933614222 +      269.92144674060*t);
      saturn_y_0+=     0.00000212434 * Math.cos( 5.38637581028 +      650.94298657790*t);
      saturn_y_0+=     0.00000236820 * Math.cos( 2.00313603940 +      219.44943459230*t);
      saturn_y_0+=     0.00000214707 * Math.cos( 1.40555033199 +      425.63498302950*t);
      saturn_y_0+=     0.00000197134 * Math.cos( 0.24363457264 +     1898.35121793960*t);
      saturn_y_0+=     0.00000190659 * Math.cos( 2.72280889899 +      355.74874557180*t);
      saturn_y_0+=     0.00000173751 * Math.cos( 1.72051113398 +      426.64637498580*t);
      saturn_y_0+=     0.00000169750 * Math.cos( 3.20987625429 +      501.37978944330*t);
      saturn_y_0+=     0.00000173746 * Math.cos( 4.80590161850 +      426.55000676620*t);
      saturn_y_0+=     0.00000168051 * Math.cos( 5.46526862654 +      312.45971639350*t);
      saturn_y_0+=     0.00000181170 * Math.cos( 3.85220242553 +     1795.25844372100*t);
      saturn_y_0+=     0.00000182549 * Math.cos( 5.95923923503 +      210.59078245230*t);
      saturn_y_0+=     0.00000179528 * Math.cos( 2.07197179284 +      216.00740842370*t);
      saturn_y_0+=     0.00000188571 * Math.cos( 2.33544585541 +      618.55664531160*t);
      saturn_y_0+=     0.00000180830 * Math.cos( 1.50904200578 +       84.34282612290*t);
      saturn_y_0+=     0.00000186121 * Math.cos( 5.22455005386 +      427.56139872250*t);
      saturn_y_0+=     0.00000196312 * Math.cos( 4.90432953947 +     2317.83586181480*t);
      saturn_y_0+=     0.00000198340 * Math.cos( 3.69541361584 +      488.84961647110*t);
      saturn_y_0+=     0.00000156017 * Math.cos( 1.90383812302 +     1375.77379984580*t);
      saturn_y_0+=     0.00000151676 * Math.cos( 2.56675310055 +      213.45915413240*t);
      saturn_y_0+=     0.00000151676 * Math.cos( 5.46446571963 +      213.13903674360*t);
      saturn_y_0+=     0.00000151429 * Math.cos( 2.33434011196 +      220.46082654860*t);
      saturn_y_0+=     0.00000167545 * Math.cos( 1.83420005749 +     1279.79457262800*t);
      saturn_y_0+=     0.00000190528 * Math.cos( 6.02427347834 +      207.14875628370*t);
      saturn_y_0+=     0.00000180421 * Math.cos( 4.76213875112 +      491.81856188770*t);
      saturn_y_0+=     0.00000180390 * Math.cos( 1.05469577674 +      344.70304530790*t);
      saturn_y_0+=     0.00000146615 * Math.cos( 5.44168799419 +      220.36445832900*t);
      saturn_y_0+=     0.00000194447 * Math.cos( 2.62404840122 +      188.92007304980*t);
      saturn_y_0+=     0.00000136976 * Math.cos( 0.70428757869 +     1148.24761040620*t);
      saturn_y_0+=     0.00000185075 * Math.cos( 3.55365539139 +      601.76425067620*t);
      saturn_y_0+=     0.00000158868 * Math.cos( 1.84813378152 +      179.35884549420*t);
      saturn_y_0+=     0.00000145472 * Math.cos( 1.21853593658 +      636.71589257630*t);
      saturn_y_0+=     0.00000155991 * Math.cos( 3.42111288262 +      289.56516671360*t);
      saturn_y_0+=     0.00000159449 * Math.cos( 3.96675364143 +      358.93013930950*t);
      saturn_y_0+=     0.00000138962 * Math.cos( 1.62828990596 +      436.15941843160*t);
      saturn_y_0+=     0.00000163232 * Math.cos( 1.79954755413 +       73.29712585900*t);
      saturn_y_0+=     0.00000177559 * Math.cos( 1.60628671275 +    10213.28554621100*t);
      saturn_y_0+=     0.00000174048 * Math.cos( 5.38802135330 +      237.67811782620*t);
      saturn_y_0+=     0.00000125284 * Math.cos( 1.76243276586 +      643.82943957710*t);
      saturn_y_0+=     0.00000131798 * Math.cos( 0.93003850215 +      212.02707105080*t);
      saturn_y_0+=     0.00000147344 * Math.cos( 1.52448539161 +      617.80588578620*t);
      saturn_y_0+=     0.00000130710 * Math.cos( 0.81771148871 +      214.57111982520*t);
      saturn_y_0+=     0.00000123423 * Math.cos( 0.17360907837 +      621.73803904930*t);
      saturn_y_0+=     0.00000132653 * Math.cos( 4.08171658773 +        4.66586644600*t);
      saturn_y_0+=     0.00000116763 * Math.cos( 0.03834317084 +      113.38771495710*t);
      saturn_y_0+=     0.00000117597 * Math.cos( 0.90279986158 +     1891.23767093880*t);
      saturn_y_0+=     0.00000115112 * Math.cos( 3.65333095084 +        5.62907429250*t);
      saturn_y_0+=     0.00000112534 * Math.cos( 5.68635818339 +      206.13736432740*t);
      saturn_y_0+=     0.00000128649 * Math.cos( 6.16927510347 +      247.23934538180*t);
      saturn_y_0+=     0.00000111075 * Math.cos( 4.41850119615 +      107.02492748170*t);
      saturn_y_0+=     0.00000109023 * Math.cos( 3.90106019375 +      114.39910691340*t);
      saturn_y_0+=     0.00000114394 * Math.cos( 5.42454880430 +       32.24332891440*t);
      saturn_y_0+=     0.00000106221 * Math.cos( 0.24090572807 +      767.36908292080*t);
      saturn_y_0+=     0.00000126251 * Math.cos( 2.79961544501 +      181.05576652360*t);
      saturn_y_0+=     0.00000102514 * Math.cos( 5.96313041202 +        0.96320784650*t);
      saturn_y_0+=     0.00000107636 * Math.cos( 2.57069606934 +      206.23373254700*t);
      saturn_y_0+=     0.00000120584 * Math.cos( 0.17406709675 +      342.25536475310*t);
      saturn_y_0+=     0.00000134800 * Math.cos( 1.20576280285 +       35.42472265210*t);
      saturn_y_0+=     0.00000105828 * Math.cos( 6.16888247845 +      219.89137757700*t);
      saturn_y_0+=     0.00000104337 * Math.cos( 2.46235960097 +     1073.60902419080*t);
      saturn_y_0+=     0.00000104663 * Math.cos( 5.88419995684 +     1361.54670584420*t);
      saturn_y_0+=     0.00000130015 * Math.cos( 5.07630034396 +      245.54242435240*t);
      saturn_y_0+=     0.00000101365 * Math.cos( 6.23985111882 +     2214.74308759620*t);
      saturn_y_0+=     0.00000100483 * Math.cos( 1.98515948445 +      140.00196957900*t);

      let saturn_y_1=0.0;
      saturn_y_1+=     0.05373889135 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_y_1+=     0.03090575152 * Math.cos( 2.70346890906 +      426.59819087600*t);
      saturn_y_1+=     0.02741594312 * Math.cos( 4.26667636015 +      206.18554843720*t);
      saturn_y_1+=     0.02647489677 * Math.cos( 3.76132298889 +      220.41264243880*t);
      saturn_y_1+=     0.00631520527 * Math.cos( 5.03245505280 +        7.11354700080*t);
      saturn_y_1+=     0.00256799701 * Math.cos( 1.95351819758 +      639.89728631400*t);
      saturn_y_1+=     0.00312271930 * Math.cos( 3.25850205023 +      419.48464387520*t);
      saturn_y_1+=     0.00189433319 * Math.cos( 2.91501840819 +      433.71173787680*t);
      saturn_y_1+=     0.00164133553 * Math.cos( 5.29239290066 +      213.29909543800*t);
      saturn_y_1+=     0.00116791227 * Math.cos( 5.89146675760 +      110.20632121940*t);
      saturn_y_1+=     0.00067210919 * Math.cos( 2.17042636344 +      316.39186965660*t);
      saturn_y_1+=     0.00067003292 * Math.cos( 3.63101075514 +      227.52618943960*t);
      saturn_y_1+=     0.00033002406 * Math.cos( 4.35527405801 +      199.07200143640*t);
      saturn_y_1+=     0.00030628998 * Math.cos( 4.88861760772 +       14.22709400160*t);
      saturn_y_1+=     0.00022234714 * Math.cos( 4.62212779231 +      103.09277421860*t);
      saturn_y_1+=     0.00018945004 * Math.cos( 1.20412493845 +      853.19638175200*t);
      saturn_y_1+=     0.00018079959 * Math.cos( 3.51566153251 +      209.36694217490*t);
      saturn_y_1+=     0.00017791543 * Math.cos( 4.53214140649 +      217.23124870110*t);
      saturn_y_1+=     0.00016320701 * Math.cos( 3.29784030970 +      216.48048917570*t);
      saturn_y_1+=     0.00015944258 * Math.cos( 4.74503265169 +      210.11770170030*t);
      saturn_y_1+=     0.00016717122 * Math.cos( 3.00270792752 +      632.78373931320*t);
      saturn_y_1+=     0.00016149947 * Math.cos( 4.04186432517 +      323.50541665740*t);
      saturn_y_1+=     0.00014481431 * Math.cos( 2.10298298650 +      647.01083331480*t);
      saturn_y_1+=     0.00011084040 * Math.cos( 4.74073871754 +      117.31986822020*t);
      saturn_y_1+=     0.00009905491 * Math.cos( 3.60258599375 +      202.25339517410*t);
      saturn_y_1+=     0.00008726051 * Math.cos( 4.46341342877 +      224.34479570190*t);
      saturn_y_1+=     0.00006585597 * Math.cos( 4.07326320487 +      309.27832265580*t);
      saturn_y_1+=     0.00005505978 * Math.cos( 2.83207390240 +      440.82528487760*t);
      saturn_y_1+=     0.00005424041 * Math.cos( 1.03197684410 +       11.04570026390*t);
      saturn_y_1+=     0.00004178266 * Math.cos( 3.01038512076 +      412.37109687440*t);
      saturn_y_1+=     0.00004049905 * Math.cos( 5.17488767645 +       95.97922721780*t);
      saturn_y_1+=     0.00002735256 * Math.cos( 2.53975850409 +      149.56319713460*t);
      saturn_y_1+=     0.00002369024 * Math.cos( 2.40497927917 +      522.57741809380*t);
      saturn_y_1+=     0.00001745258 * Math.cos( 5.50576015456 +      277.03499374140*t);
      saturn_y_1+=     0.00001692790 * Math.cos( 2.39926502529 +      422.66603761290*t);
      saturn_y_1+=     0.00001546006 * Math.cos( 3.73156925599 +      330.61896365820*t);
      saturn_y_1+=     0.00001389354 * Math.cos( 0.46207025895 +     1066.49547719000*t);
      saturn_y_1+=     0.00001332553 * Math.cos( 3.49199812296 +      234.63973644040*t);
      saturn_y_1+=     0.00001300934 * Math.cos( 0.83727681906 +      415.55249061210*t);
      saturn_y_1+=     0.00001393622 * Math.cos( 4.62214277175 +        3.18139373770*t);
      saturn_y_1+=     0.00001174319 * Math.cos( 2.72609984335 +      846.08283475120*t);
      saturn_y_1+=     0.00001148010 * Math.cos( 3.04374738882 +      536.80451209540*t);
      saturn_y_1+=     0.00001314125 * Math.cos( 4.38891656600 +      625.67019231240*t);
      saturn_y_1+=     0.00001127952 * Math.cos( 3.87309692307 +      423.41679713830*t);
      saturn_y_1+=     0.00001127646 * Math.cos( 1.31088906213 +      860.30992875280*t);
      saturn_y_1+=     0.00001519732 * Math.cos( 6.12880664637 +        3.93215326310*t);
      saturn_y_1+=     0.00001102361 * Math.cos( 2.50535306014 +      429.77958461370*t);
      saturn_y_1+=     0.00001344891 * Math.cos( 1.41793593685 +      210.85141488320*t);
      saturn_y_1+=     0.00001331786 * Math.cos( 0.33834520814 +      215.74677599280*t);
      saturn_y_1+=     0.00000883058 * Math.cos( 3.84618360720 +      437.64389113990*t);
      saturn_y_1+=     0.00000845266 * Math.cos( 2.61037749001 +      838.96928775040*t);
      saturn_y_1+=     0.00000961358 * Math.cos( 4.02278025887 +      529.69096509460*t);
      saturn_y_1+=     0.00000821120 * Math.cos( 3.17476992262 +      223.59403617650*t);
      saturn_y_1+=     0.00000663718 * Math.cos( 5.44560261113 +      742.99006053260*t);
      saturn_y_1+=     0.00000690028 * Math.cos( 5.48656808690 +       88.86568021700*t);
      saturn_y_1+=     0.00000816193 * Math.cos( 4.73301735835 +       21.34064100240*t);
      saturn_y_1+=     0.00000711521 * Math.cos( 4.54955689543 +      430.53034413910*t);
      saturn_y_1+=     0.00000698870 * Math.cos( 4.56691908682 +      302.16477565500*t);
      saturn_y_1+=     0.00000536606 * Math.cos( 4.99753895831 +     1059.38193018920*t);
      saturn_y_1+=     0.00000597583 * Math.cos( 3.52687187533 +      124.43341522100*t);
      saturn_y_1+=     0.00000471839 * Math.cos( 2.03826977441 +      654.12438031560*t);
      saturn_y_1+=     0.00000479853 * Math.cos( 4.85897867518 +      203.00415469950*t);
      saturn_y_1+=     0.00000516670 * Math.cos( 5.88132040654 +      735.87651353180*t);
      saturn_y_1+=     0.00000402498 * Math.cos( 2.85466690529 +       85.82729883120*t);
      saturn_y_1+=     0.00000403624 * Math.cos( 2.71139052784 +      515.46387109300*t);
      saturn_y_1+=     0.00000376986 * Math.cos( 2.14076396290 +       76.26607127560*t);
      saturn_y_1+=     0.00000380146 * Math.cos( 4.42849645888 +      191.95845443560*t);
      saturn_y_1+=     0.00000329385 * Math.cos( 2.25090412205 +     1155.36115740700*t);
      saturn_y_1+=     0.00000339777 * Math.cos( 1.16732337173 +      217.96496188400*t);
      saturn_y_1+=     0.00000304932 * Math.cos( 4.89664555631 +      231.45834270270*t);
      saturn_y_1+=     0.00000313279 * Math.cos( 0.79690491776 +      628.85158605010*t);
      saturn_y_1+=     0.00000312508 * Math.cos( 3.52860936096 +      942.06206196900*t);
      saturn_y_1+=     0.00000299967 * Math.cos( 0.58486918119 +      208.63322899200*t);
      saturn_y_1+=     0.00000271553 * Math.cos( 1.13380715292 +      288.08069400530*t);
      saturn_y_1+=     0.00000261665 * Math.cos( 5.58043800182 +       18.15924726470*t);
      saturn_y_1+=     0.00000336751 * Math.cos( 1.51006955238 +      203.73786788240*t);
      saturn_y_1+=     0.00000259741 * Math.cos( 4.42049959331 +       10.29494073850*t);
      saturn_y_1+=     0.00000263792 * Math.cos( 1.98500737829 +      362.86229257260*t);
      saturn_y_1+=     0.00000288998 * Math.cos( 1.62421296562 +      728.76296653100*t);
      saturn_y_1+=     0.00000292480 * Math.cos( 0.24003627114 +      222.86032299360*t);
      saturn_y_1+=     0.00000213893 * Math.cos( 4.46025867511 +      207.88246946660*t);
      saturn_y_1+=     0.00000230876 * Math.cos( 5.80645007490 +      949.17560896980*t);
      saturn_y_1+=     0.00000208106 * Math.cos( 3.59333007773 +      218.71572140940*t);
      saturn_y_1+=     0.00000208355 * Math.cos( 2.79392574025 +      408.43894361130*t);
      saturn_y_1+=     0.00000212226 * Math.cos( 0.51516577794 +      138.51749687070*t);
      saturn_y_1+=     0.00000195753 * Math.cos( 1.92286511963 +       52.69019803950*t);
      saturn_y_1+=     0.00000194622 * Math.cos( 5.15592319826 +      340.77089204480*t);
      saturn_y_1+=     0.00000194009 * Math.cos( 4.64002206209 +      200.76892246580*t);
      saturn_y_1+=     0.00000169514 * Math.cos( 5.90010865240 +      350.33211960040*t);
      saturn_y_1+=     0.00000167903 * Math.cos( 3.43165870674 +      225.82926841020*t);
      saturn_y_1+=     0.00000165942 * Math.cos( 2.65915928084 +      831.85574074960*t);
      saturn_y_1+=     0.00000177511 * Math.cos( 3.37006150668 +      210.37833413120*t);
      saturn_y_1+=     0.00000177822 * Math.cos( 4.64970159848 +      216.21985674480*t);
      saturn_y_1+=     0.00000160353 * Math.cos( 0.38234469263 +      195.13984817330*t);
      saturn_y_1+=     0.00000163772 * Math.cos( 4.33810904454 +      956.28915597060*t);
      saturn_y_1+=     0.00000145034 * Math.cos( 5.01521877128 +        9.56122755560*t);
      saturn_y_1+=     0.00000178118 * Math.cos( 4.70008509025 +      160.60889739850*t);
      saturn_y_1+=     0.00000170270 * Math.cos( 1.06169886425 +      207.67002114550*t);
      saturn_y_1+=     0.00000151139 * Math.cos( 1.56897925752 +      635.96513305090*t);
      saturn_y_1+=     0.00000137032 * Math.cos( 2.94671384771 +      543.91805909620*t);
      saturn_y_1+=     0.00000163974 * Math.cos( 0.66806989122 +      218.92816973050*t);
      saturn_y_1+=     0.00000136838 * Math.cos( 1.98352486919 +     1471.75302706360*t);
      saturn_y_1+=     0.00000164874 * Math.cos( 3.04584528801 +       22.09140052780*t);
      saturn_y_1+=     0.00000134654 * Math.cos( 5.96927335823 +      703.63318461740*t);
      saturn_y_1+=     0.00000151556 * Math.cos( 3.67396623947 +      127.47179660680*t);
      saturn_y_1+=     0.00000153277 * Math.cos( 5.85394341815 +       56.62235130260*t);
      saturn_y_1+=     0.00000131057 * Math.cos( 2.45918482900 +      750.10360753340*t);
      saturn_y_1+=     0.00000135752 * Math.cos( 3.20181584059 +     1258.45393162560*t);
      saturn_y_1+=     0.00000124428 * Math.cos( 2.71560761485 +      447.93883187840*t);
      saturn_y_1+=     0.00000135909 * Math.cos( 2.82497232885 +      142.44965013380*t);
      saturn_y_1+=     0.00000137107 * Math.cos( 5.58034331705 +      490.33408917940*t);
      saturn_y_1+=     0.00000108222 * Math.cos( 1.17614128037 +      565.11568774670*t);
      saturn_y_1+=     0.00000122931 * Math.cos( 1.28638505576 +      483.22054217860*t);
      saturn_y_1+=     0.00000105358 * Math.cos( 2.01086087701 +      209.10630974400*t);
      saturn_y_1+=     0.00000105077 * Math.cos( 6.01394978397 +      217.49188113200*t);
      saturn_y_1+=     0.00000123632 * Math.cos( 0.14236071000 +       12.53017297220*t);
      saturn_y_1+=     0.00000117145 * Math.cos( 1.93408241498 +      269.92144674060*t);
      saturn_y_1+=     0.00000107531 * Math.cos( 0.47701573313 +      424.15051032120*t);
      saturn_y_1+=     0.00000105031 * Math.cos( 1.46162172146 +     1045.15483618760*t);
      saturn_y_1+=     0.00000128853 * Math.cos( 4.09081439424 +      618.55664531160*t);
      saturn_y_1+=     0.00000109631 * Math.cos( 3.58034902833 +      265.98929347750*t);
      saturn_y_1=saturn_y_1 * t;

      let saturn_y_2=0.0;
      saturn_y_2+=     0.00563706537 * Math.cos( 5.97115878242 +      206.18554843720*t);
      saturn_y_2+=     0.00547012116 * Math.cos( 2.05154973426 +      220.41264243880*t);
      saturn_y_2+=     0.00458518613 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_y_2+=     0.00362294249 * Math.cos( 0.89540100509 +      213.29909543800*t);
      saturn_y_2+=     0.00225521642 * Math.cos( 0.91699821445 +      426.59819087600*t);
      saturn_y_2+=     0.00088390611 * Math.cos( 3.30289449917 +        7.11354700080*t);
      saturn_y_2+=     0.00050101314 * Math.cos( 1.12976163835 +      433.71173787680*t);
      saturn_y_2+=     0.00045516403 * Math.cos( 5.07669466539 +      419.48464387520*t);
      saturn_y_2+=     0.00032896745 * Math.cos( 0.02089057938 +      639.89728631400*t);
      saturn_y_2+=     0.00027199743 * Math.cos( 1.92638417640 +      227.52618943960*t);
      saturn_y_2+=     0.00013251505 * Math.cos( 6.07693099404 +      199.07200143640*t);
      saturn_y_2+=     0.00010425984 * Math.cos( 3.18246869028 +       14.22709400160*t);
      saturn_y_2+=     0.00006673556 * Math.cos( 4.24747633887 +      110.20632121940*t);
      saturn_y_2+=     0.00004658591 * Math.cos( 0.26557833758 +      647.01083331480*t);
      saturn_y_2+=     0.00004934094 * Math.cos( 1.51301179516 +      216.48048917570*t);
      saturn_y_2+=     0.00004789554 * Math.cos( 0.24337901916 +      210.11770170030*t);
      saturn_y_2+=     0.00004167268 * Math.cos( 3.73203671391 +      316.39186965660*t);
      saturn_y_2+=     0.00003509537 * Math.cos( 5.49281440568 +      853.19638175200*t);
      saturn_y_2+=     0.00002743470 * Math.cos( 6.21939083886 +      103.09277421860*t);
      saturn_y_2+=     0.00002661172 * Math.cos( 1.58795412736 +      209.36694217490*t);
      saturn_y_2+=     0.00002541191 * Math.cos( 1.07964653574 +      440.82528487760*t);
      saturn_y_2+=     0.00002568018 * Math.cos( 0.16811216098 +      217.23124870110*t);
      saturn_y_2+=     0.00002507738 * Math.cos( 3.11882746290 +      117.31986822020*t);
      saturn_y_2+=     0.00002159089 * Math.cos( 4.99912567024 +      632.78373931320*t);
      saturn_y_2+=     0.00001828412 * Math.cos( 2.43368650590 +      323.50541665740*t);
      saturn_y_2+=     0.00001351629 * Math.cos( 4.81673889364 +      412.37109687440*t);
      saturn_y_2+=     0.00001177305 * Math.cos( 5.84484412189 +      309.27832265580*t);
      saturn_y_2+=     0.00000804912 * Math.cos( 1.78663050298 +      234.63973644040*t);
      saturn_y_2+=     0.00000891561 * Math.cos( 0.57880622764 +       95.97922721780*t);
      saturn_y_2+=     0.00000806554 * Math.cos( 5.80160560511 +      202.25339517410*t);
      saturn_y_2+=     0.00000737518 * Math.cos( 2.29009633302 +      224.34479570190*t);
      saturn_y_2+=     0.00000439328 * Math.cos( 2.02776827506 +      330.61896365820*t);
      saturn_y_2+=     0.00000427442 * Math.cos( 5.71757576099 +      860.30992875280*t);
      saturn_y_2+=     0.00000377116 * Math.cos( 5.39638432405 +       11.04570026390*t);
      saturn_y_2+=     0.00000438738 * Math.cos( 3.04003133763 +       21.34064100240*t);
      saturn_y_2+=     0.00000404595 * Math.cos( 1.38253517416 +      223.59403617650*t);
      saturn_y_2+=     0.00000400049 * Math.cos( 0.64827543918 +      429.77958461370*t);
      saturn_y_2+=     0.00000335529 * Math.cos( 4.72223792972 +     1066.49547719000*t);
      saturn_y_2+=     0.00000313557 * Math.cos( 2.87420547669 +        3.18139373770*t);
      saturn_y_2+=     0.00000356011 * Math.cos( 0.49515346590 +      422.66603761290*t);
      saturn_y_2+=     0.00000283801 * Math.cos( 0.92471217472 +       88.86568021700*t);
      saturn_y_2+=     0.00000276664 * Math.cos( 0.06759886827 +      625.67019231240*t);
      saturn_y_2+=     0.00000274267 * Math.cos( 0.07990244299 +      302.16477565500*t);
      saturn_y_2+=     0.00000265498 * Math.cos( 5.80586423553 +      423.41679713830*t);
      saturn_y_2+=     0.00000243984 * Math.cos( 0.24814637625 +      654.12438031560*t);
      saturn_y_2+=     0.00000263236 * Math.cos( 1.75838078242 +      124.43341522100*t);
      saturn_y_2+=     0.00000234804 * Math.cos( 1.98441386459 +        3.93215326310*t);
      saturn_y_2+=     0.00000322970 * Math.cos( 3.74692518093 +      529.69096509460*t);
      saturn_y_2+=     0.00000222884 * Math.cos( 6.17115980346 +      191.95845443560*t);
      saturn_y_2+=     0.00000229042 * Math.cos( 0.40578151728 +      203.00415469950*t);
      saturn_y_2+=     0.00000194066 * Math.cos( 0.77928033729 +      149.56319713460*t);
      saturn_y_2+=     0.00000175058 * Math.cos( 3.24791503390 +      522.57741809380*t);
      saturn_y_2+=     0.00000158535 * Math.cos( 1.24843935837 +      536.80451209540*t);
      saturn_y_2+=     0.00000115588 * Math.cos( 0.89164509195 +      277.03499374140*t);
      saturn_y_2+=     0.00000109123 * Math.cos( 2.57234111431 +       10.29494073850*t);
      saturn_y_2+=     0.00000104167 * Math.cos( 4.29243802959 +      515.46387109300*t);
      saturn_y_2+=     0.00000123782 * Math.cos( 1.71078775140 +      437.64389113990*t);
      saturn_y_2+=     0.00000102074 * Math.cos( 5.33636424684 +      846.08283475120*t);
      saturn_y_2=saturn_y_2 * t * t;

      let saturn_y_3=0.0;
      saturn_y_3+=     0.00077376615 * Math.cos( 1.40391048961 +      206.18554843720*t);
      saturn_y_3+=     0.00075564351 * Math.cos( 0.31962896379 +      220.41264243880*t);
      saturn_y_3+=     0.00022843837 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_y_3+=     0.00010672263 * Math.cos( 5.36495663820 +      426.59819087600*t);
      saturn_y_3+=     0.00009010175 * Math.cos( 5.62865146645 +      433.71173787680*t);
      saturn_y_3+=     0.00007418018 * Math.cos( 0.21442310101 +      227.52618943960*t);
      saturn_y_3+=     0.00008298723 * Math.cos( 1.52262563519 +        7.11354700080*t);
      saturn_y_3+=     0.00004507061 * Math.cos( 0.67248969480 +      419.48464387520*t);
      saturn_y_3+=     0.00003581682 * Math.cos( 1.51466786030 +      199.07200143640*t);
      saturn_y_3+=     0.00002981969 * Math.cos( 4.42868951627 +      639.89728631400*t);
      saturn_y_3+=     0.00002376221 * Math.cos( 1.46232779180 +       14.22709400160*t);
      saturn_y_3+=     0.00001024263 * Math.cos( 4.72337917196 +      647.01083331480*t);
      saturn_y_3+=     0.00000788826 * Math.cos( 5.61078104123 +      440.82528487760*t);
      saturn_y_3+=     0.00000807916 * Math.cos( 5.99385575552 +      216.48048917570*t);
      saturn_y_3+=     0.00000770831 * Math.cos( 2.04234808917 +      210.11770170030*t);
      saturn_y_3+=     0.00000384210 * Math.cos( 1.48542445090 +      117.31986822020*t);
      saturn_y_3+=     0.00000456443 * Math.cos( 3.56523371093 +      853.19638175200*t);
      saturn_y_3+=     0.00000324148 * Math.cos( 0.08074667476 +      234.63973644040*t);
      saturn_y_3+=     0.00000338016 * Math.cos( 2.47226721573 +      110.20632121940*t);
      saturn_y_3+=     0.00000355769 * Math.cos( 5.40701066557 +      213.29909543800*t);
      saturn_y_3+=     0.00000296603 * Math.cos( 0.32077836251 +      412.37109687440*t);
      saturn_y_3+=     0.00000241378 * Math.cos( 1.79772375424 +      103.09277421860*t);
      saturn_y_3+=     0.00000198202 * Math.cos( 5.51857978716 +      316.39186965660*t);
      saturn_y_3+=     0.00000195234 * Math.cos( 0.72153771655 +      632.78373931320*t);
      saturn_y_3+=     0.00000150777 * Math.cos( 0.77624311648 +      323.50541665740*t);
      saturn_y_3+=     0.00000154028 * Math.cos( 1.31543626425 +       21.34064100240*t);
      saturn_y_3+=     0.00000151698 * Math.cos( 1.38281351365 +      309.27832265580*t);
      saturn_y_3+=     0.00000131653 * Math.cos( 2.26722574599 +       95.97922721780*t);
      saturn_y_3+=     0.00000125170 * Math.cos( 6.14972338278 +      209.36694217490*t);
      saturn_y_3+=     0.00000113221 * Math.cos( 1.84141052645 +      217.23124870110*t);
      saturn_y_3+=     0.00000111239 * Math.cos( 3.84668749918 +      860.30992875280*t);
      saturn_y_3+=     0.00000114537 * Math.cos( 5.87729837758 +      223.59403617650*t);
      saturn_y_3=saturn_y_3 * t * t * t;

      let saturn_y_4=0.0;
      saturn_y_4+=     0.00007978886 * Math.cos( 3.13229268011 +      206.18554843720*t);
      saturn_y_4+=     0.00007868379 * Math.cos( 4.84940260021 +      220.41264243880*t);
      saturn_y_4+=     0.00001514835 * Math.cos( 4.77675733867 +      227.52618943960*t);
      saturn_y_4+=     0.00001225569 * Math.cos( 3.84500138574 +      433.71173787680*t);
      saturn_y_4+=     0.00000720573 * Math.cos( 3.23773181595 +      199.07200143640*t);
      saturn_y_4+=     0.00000609979 * Math.cos( 5.96461769948 +        7.11354700080*t);
      saturn_y_4+=     0.00000353860 * Math.cos( 2.57548318224 +      419.48464387520*t);
      saturn_y_4+=     0.00000382994 * Math.cos( 6.00399581554 +       14.22709400160*t);
      saturn_y_4+=     0.00000469340 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_y_4+=     0.00000403662 * Math.cos( 3.41614173802 +      426.59819087600*t);
      saturn_y_4+=     0.00000185465 * Math.cos( 3.86274212431 +      440.82528487760*t);
      saturn_y_4+=     0.00000208259 * Math.cos( 2.57791157635 +      639.89728631400*t);
      saturn_y_4+=     0.00000172118 * Math.cos( 2.90478987674 +      647.01083331480*t);
      saturn_y_4=saturn_y_4 * t * t * t * t;

      let saturn_y_5=0.0;
      saturn_y_5+=     0.00000589080 * Math.cos( 4.84910386986 +      206.18554843720*t);
      saturn_y_5+=     0.00000590114 * Math.cos( 3.08953743297 +      220.41264243880*t);
      saturn_y_5+=     0.00000226448 * Math.cos( 3.03832080293 +      227.52618943960*t);
      saturn_y_5+=     0.00000131513 * Math.cos( 2.04967560816 +      433.71173787680*t);
      saturn_y_5=saturn_y_5 * t * t * t * t * t;

      return saturn_y_0+saturn_y_1+saturn_y_2+saturn_y_3+saturn_y_4+saturn_y_5;
   }

   static saturn_z(t){
      let saturn_z_0=0.0;
      saturn_z_0+=     0.41356950940 * Math.cos( 3.60234142982 +      213.29909543800*t);
      saturn_z_0+=     0.01148283576 * Math.cos( 2.85128367469 +      426.59819087600*t);
      saturn_z_0+=     0.01214249867 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_z_0+=     0.00329280791 * Math.cos( 0.57121407104 +      206.18554843720*t);
      saturn_z_0+=     0.00286934048 * Math.cos( 3.48073526693 +      220.41264243880*t);
      saturn_z_0+=     0.00099076584 * Math.cos( 4.73369511264 +        7.11354700080*t);
      saturn_z_0+=     0.00057361820 * Math.cos( 4.92611225093 +      110.20632121940*t);
      saturn_z_0+=     0.00047738127 * Math.cos( 2.10039779728 +      639.89728631400*t);
      saturn_z_0+=     0.00043458803 * Math.cos( 5.84904978051 +      419.48464387520*t);
      saturn_z_0+=     0.00034565673 * Math.cos( 5.42614229590 +      316.39186965660*t);
      saturn_z_0+=     0.00016185391 * Math.cos( 2.72987173675 +      433.71173787680*t);
      saturn_z_0+=     0.00009001270 * Math.cos( 1.38140102737 +      103.09277421860*t);
      saturn_z_0+=     0.00011433574 * Math.cos( 3.71662021072 +      529.69096509460*t);
      saturn_z_0+=     0.00005398708 * Math.cos( 5.13204892363 +      202.25339517410*t);
      saturn_z_0+=     0.00003902467 * Math.cos( 3.71499738796 +      323.50541665740*t);
      saturn_z_0+=     0.00003709212 * Math.cos( 5.05549348785 +      632.78373931320*t);
      saturn_z_0+=     0.00003614100 * Math.cos( 3.35210451276 +      227.52618943960*t);
      saturn_z_0+=     0.00003379953 * Math.cos( 2.13868919206 +       11.04570026390*t);
      saturn_z_0+=     0.00003089874 * Math.cos( 3.62572857085 +      209.36694217490*t);
      saturn_z_0+=     0.00002683064 * Math.cos( 4.87689555581 +      224.34479570190*t);
      saturn_z_0+=     0.00002963493 * Math.cos( 0.46490184985 +      217.23124870110*t);
      saturn_z_0+=     0.00002343367 * Math.cos( 1.34558278340 +      853.19638175200*t);
      saturn_z_0+=     0.00002423663 * Math.cos( 2.92907094760 +       63.73589830340*t);
      saturn_z_0+=     0.00001701916 * Math.cos( 1.89892525654 +      735.87651353180*t);
      saturn_z_0+=     0.00001941205 * Math.cos( 4.59421314662 +       14.22709400160*t);
      saturn_z_0+=     0.00001990145 * Math.cos( 0.73166053611 +      199.07200143640*t);
      saturn_z_0+=     0.00001460265 * Math.cos( 3.12851339724 +      522.57741809380*t);
      saturn_z_0+=     0.00001148341 * Math.cos( 4.41139213915 +      117.31986822020*t);
      saturn_z_0+=     0.00001092809 * Math.cos( 3.10679381209 +      216.48048917570*t);
      saturn_z_0+=     0.00001015179 * Math.cos( 1.97897195994 +      647.01083331480*t);
      saturn_z_0+=     0.00001098254 * Math.cos( 0.96097709156 +      210.11770170030*t);
      saturn_z_0+=     0.00000991030 * Math.cos( 2.99610026682 +      846.08283475120*t);
      saturn_z_0+=     0.00001028743 * Math.cos( 2.11933059243 +      415.55249061210*t);
      saturn_z_0+=     0.00000907817 * Math.cos( 4.68576278610 +      309.27832265580*t);
      saturn_z_0+=     0.00000818092 * Math.cos( 2.91497656196 +      149.56319713460*t);
      saturn_z_0+=     0.00000733443 * Math.cos( 2.10018715614 +       74.78159856730*t);
      saturn_z_0+=     0.00000631275 * Math.cos( 1.30557255814 +      277.03499374140*t);
      saturn_z_0+=     0.00000574266 * Math.cos( 0.63353925382 +      490.33408917940*t);
      saturn_z_0+=     0.00000471645 * Math.cos( 1.62329782277 +     1052.26838318840*t);
      saturn_z_0+=     0.00000416292 * Math.cos( 5.88171380023 +       95.97922721780*t);
      saturn_z_0+=     0.00000412467 * Math.cos( 2.56322277221 +     1162.47470440780*t);
      saturn_z_0+=     0.00000381934 * Math.cos( 2.83850532211 +      838.96928775040*t);
      saturn_z_0+=     0.00000370902 * Math.cos( 2.22356953874 +      351.81659230870*t);
      saturn_z_0+=     0.00000337338 * Math.cos( 4.12487690436 +        3.93215326310*t);
      saturn_z_0+=     0.00000263173 * Math.cos( 2.60594324261 +      440.82528487760*t);
      saturn_z_0+=     0.00000245414 * Math.cos( 3.87716027424 +     1059.38193018920*t);
      saturn_z_0+=     0.00000231186 * Math.cos( 2.79137518143 +      127.47179660680*t);
      saturn_z_0+=     0.00000232835 * Math.cos( 1.69429632635 +       38.13303563780*t);
      saturn_z_0+=     0.00000226218 * Math.cos( 0.98981012262 +      210.85141488320*t);
      saturn_z_0+=     0.00000252287 * Math.cos( 3.04205345262 +      137.03302416240*t);
      saturn_z_0+=     0.00000213656 * Math.cos( 3.00046819587 +      536.80451209540*t);
      saturn_z_0+=     0.00000223924 * Math.cos( 3.07498346391 +      215.74677599280*t);
      saturn_z_0+=     0.00000189917 * Math.cos( 5.75255233102 +      742.99006053260*t);
      saturn_z_0+=     0.00000162873 * Math.cos( 3.89762690585 +      214.26230328450*t);
      saturn_z_0+=     0.00000164510 * Math.cos( 2.45697452905 +      422.66603761290*t);
      saturn_z_0+=     0.00000158304 * Math.cos( 2.31306407231 +     1478.86657406440*t);
      saturn_z_0+=     0.00000156454 * Math.cos( 1.35680198123 +     1368.66025284500*t);
      saturn_z_0+=     0.00000202699 * Math.cos( 3.85581899880 +      949.17560896980*t);
      saturn_z_0+=     0.00000150079 * Math.cos( 4.14045329244 +      437.64389113990*t);
      saturn_z_0+=     0.00000142705 * Math.cos( 2.58383947868 +     1155.36115740700*t);
      saturn_z_0+=     0.00000163551 * Math.cos( 0.16578976592 +      212.33588759150*t);
      saturn_z_0+=     0.00000135335 * Math.cos( 0.48883402314 +      213.34727954780*t);
      saturn_z_0+=     0.00000129140 * Math.cos( 2.17035714121 +       76.26607127560*t);
      saturn_z_0+=     0.00000128206 * Math.cos( 0.59415255592 +     1066.49547719000*t);
      saturn_z_0+=     0.00000140534 * Math.cos( 3.97289861748 +      625.67019231240*t);
      saturn_z_0+=     0.00000121564 * Math.cos( 4.51381049808 +        3.18139373770*t);
      saturn_z_0+=     0.00000119190 * Math.cos( 1.61391416177 +      628.85158605010*t);
      saturn_z_0+=     0.00000115147 * Math.cos( 3.43459040245 +      330.61896365820*t);
      saturn_z_0+=     0.00000135375 * Math.cos( 3.57424025701 +      213.25091132820*t);
      saturn_z_0+=     0.00000103727 * Math.cos( 6.17639441368 +      200.76892246580*t);
      saturn_z_0+=     0.00000107498 * Math.cos( 3.52498564069 +      138.51749687070*t);
      saturn_z_0+=     0.00000107560 * Math.cos( 3.99837836470 +       85.82729883120*t);
      saturn_z_0+=     0.00000113808 * Math.cos( 0.43922136441 +      222.86032299360*t);
      saturn_z_0+=     0.00000110037 * Math.cos( 3.51152757685 +     1265.56747862640*t);
      saturn_z_0+=     0.00000101425 * Math.cos( 0.14126238472 +      430.53034413910*t);
      saturn_z_0+=     0.00000101928 * Math.cos( 0.21047731069 +      412.37109687440*t);
      saturn_z_0+=     0.00000104973 * Math.cos( 4.19518394917 +        9.56122755560*t);

      let saturn_z_1=0.0;
      saturn_z_1+=     0.01906503283 * Math.cos( 4.94544746116 +      213.29909543800*t);
      saturn_z_1+=     0.00528301265 * Math.cos( 3.14159265359 +        0.00000000000*t);
      saturn_z_1+=     0.00130262284 * Math.cos( 2.26140980879 +      206.18554843720*t);
      saturn_z_1+=     0.00101466332 * Math.cos( 1.79095829545 +      220.41264243880*t);
      saturn_z_1+=     0.00085947578 * Math.cos( 0.51612788497 +      426.59819087600*t);
      saturn_z_1+=     0.00022257446 * Math.cos( 3.07684015656 +        7.11354700080*t);
      saturn_z_1+=     0.00016179946 * Math.cos( 1.19987517506 +      419.48464387520*t);
      saturn_z_1+=     0.00009117402 * Math.cos( 6.17205626814 +      639.89728631400*t);
      saturn_z_1+=     0.00007470703 * Math.cos( 0.93135621171 +      433.71173787680*t);
      saturn_z_1+=     0.00004966668 * Math.cos( 0.19044864213 +      316.39186965660*t);
      saturn_z_1+=     0.00003816564 * Math.cos( 4.38284565245 +      110.20632121940*t);
      saturn_z_1+=     0.00002724120 * Math.cos( 1.65580138665 +      227.52618943960*t);
      saturn_z_1+=     0.00001734540 * Math.cos( 3.51628075636 +      103.09277421860*t);
      saturn_z_1+=     0.00001541995 * Math.cos( 2.42323572812 +      199.07200143640*t);
      saturn_z_1+=     0.00001209302 * Math.cos( 2.91140089093 +       14.22709400160*t);
      saturn_z_1+=     0.00000866838 * Math.cos( 0.73856780280 +      632.78373931320*t);
      saturn_z_1+=     0.00000879041 * Math.cos( 2.44338509079 +      217.23124870110*t);
      saturn_z_1+=     0.00000734372 * Math.cos( 2.73478985417 +      210.11770170030*t);
      saturn_z_1+=     0.00000722775 * Math.cos( 5.44726167811 +      853.19638175200*t);
      saturn_z_1+=     0.00000651363 * Math.cos( 1.48968855554 +      209.36694217490*t);
      saturn_z_1+=     0.00000582461 * Math.cos( 0.11224949820 +      647.01083331480*t);
      saturn_z_1+=     0.00000657945 * Math.cos( 1.31442181621 +      216.48048917570*t);
      saturn_z_1+=     0.00000510204 * Math.cos( 1.75579678660 +      202.25339517410*t);
      saturn_z_1+=     0.00000467826 * Math.cos( 2.04967300315 +      323.50541665740*t);
      saturn_z_1+=     0.00000449108 * Math.cos( 2.82333930488 +      117.31986822020*t);
      saturn_z_1+=     0.00000309971 * Math.cos( 2.20380300055 +      224.34479570190*t);
      saturn_z_1+=     0.00000226192 * Math.cos( 0.85233380252 +      440.82528487760*t);
      saturn_z_1+=     0.00000185756 * Math.cos( 1.27629128235 +      529.69096509460*t);
      saturn_z_1+=     0.00000177430 * Math.cos( 0.67755587853 +      309.27832265580*t);
      saturn_z_1+=     0.00000214346 * Math.cos( 4.69288132929 +       11.04570026390*t);
      saturn_z_1+=     0.00000142289 * Math.cos( 1.34444047746 +       95.97922721780*t);
      saturn_z_1+=     0.00000121733 * Math.cos( 1.54733882587 +       63.73589830340*t);
      saturn_z_1+=     0.00000124732 * Math.cos( 4.78897151261 +      522.57741809380*t);
      saturn_z_1+=     0.00000117048 * Math.cos( 0.50415140377 +      735.87651353180*t);
      saturn_z_1+=     0.00000126962 * Math.cos( 1.40560397506 +      412.37109687440*t);
      saturn_z_1+=     0.00000118129 * Math.cos( 4.62838752214 +      846.08283475120*t);
      saturn_z_1=saturn_z_1 * t;

      let saturn_z_2=0.0;
      saturn_z_2+=     0.00131275155 * Math.cos( 0.08868998101 +      213.29909543800*t);
      saturn_z_2+=     0.00030147649 * Math.cos( 3.91396203887 +      206.18554843720*t);
      saturn_z_2+=     0.00019322173 * Math.cos( 0.09228748624 +      220.41264243880*t);
      saturn_z_2+=     0.00006868926 * Math.cos( 5.48420255395 +      426.59819087600*t);
      saturn_z_2+=     0.00002826107 * Math.cos( 1.36583318555 +        7.11354700080*t);
      saturn_z_2+=     0.00002646332 * Math.cos( 2.94607395955 +      419.48464387520*t);
      saturn_z_2+=     0.00003138233 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_z_2+=     0.00001844798 * Math.cos( 5.43612062856 +      433.71173787680*t);
      saturn_z_2+=     0.00001055383 * Math.cos( 6.23890785179 +      227.52618943960*t);
      saturn_z_2+=     0.00001036435 * Math.cos( 4.33916308552 +      639.89728631400*t);
      saturn_z_2+=     0.00000634611 * Math.cos( 4.10413821983 +      199.07200143640*t);
      saturn_z_2+=     0.00000493127 * Math.cos( 1.74516983084 +      316.39186965660*t);
      saturn_z_2+=     0.00000384993 * Math.cos( 1.22066829531 +       14.22709400160*t);
      saturn_z_2+=     0.00000239476 * Math.cos( 4.47935921474 +      210.11770170030*t);
      saturn_z_2+=     0.00000205194 * Math.cos( 1.76728126877 +      110.20632121940*t);
      saturn_z_2+=     0.00000176308 * Math.cos( 4.56317761920 +      647.01083331480*t);
      saturn_z_2+=     0.00000150033 * Math.cos( 4.33649711181 +      103.09277421860*t);
      saturn_z_2+=     0.00000148023 * Math.cos( 4.28188112046 +      217.23124870110*t);
      saturn_z_2+=     0.00000184735 * Math.cos( 5.81729679119 +      216.48048917570*t);
      saturn_z_2+=     0.00000128877 * Math.cos( 2.62827363828 +      632.78373931320*t);
      saturn_z_2+=     0.00000100020 * Math.cos( 5.38535854003 +      440.82528487760*t);
      saturn_z_2+=     0.00000121332 * Math.cos( 3.47780478719 +      853.19638175200*t);
      saturn_z_2=saturn_z_2 * t * t;

      let saturn_z_3=0.0;
      saturn_z_3+=     0.00004559419 * Math.cos( 1.70646871501 +      213.29909543800*t);
      saturn_z_3+=     0.00004779074 * Math.cos( 5.57723756330 +      206.18554843720*t);
      saturn_z_3+=     0.00003965402 * Math.cos( 0.00000000000 +        0.00000000000*t);
      saturn_z_3+=     0.00002508242 * Math.cos( 4.64959056313 +      220.41264243880*t);
      saturn_z_3+=     0.00000314334 * Math.cos( 3.65978364894 +      433.71173787680*t);
      saturn_z_3+=     0.00000276132 * Math.cos( 4.53051550901 +      227.52618943960*t);
      saturn_z_3+=     0.00000322702 * Math.cos( 4.70757024216 +      419.48464387520*t);
      saturn_z_3+=     0.00000327628 * Math.cos( 3.31597275465 +      426.59819087600*t);
      saturn_z_3+=     0.00000243745 * Math.cos( 5.87706678179 +        7.11354700080*t);
      saturn_z_3+=     0.00000174957 * Math.cos( 5.78592635050 +      199.07200143640*t);
      saturn_z_3=saturn_z_3 * t * t * t;

      let saturn_z_4=0.0;
      saturn_z_4+=     0.00000574306 * Math.cos( 0.96387396086 +      206.18554843720*t);
      saturn_z_4+=     0.00000252516 * Math.cos( 2.90188946355 +      220.41264243880*t);
      saturn_z_4+=     0.00000244875 * Math.cos( 2.96492296609 +      213.29909543800*t);
      saturn_z_4=saturn_z_4 * t * t * t * t;

      return saturn_z_0+saturn_z_1+saturn_z_2+saturn_z_3+saturn_z_4;
   }

   static uranus_x(t){
      let uranus_x_0=0.0;
      uranus_x_0+=    19.17370730359 * Math.cos( 5.48133416489 +       74.78159856730*t);
      uranus_x_0+=     1.32272523872 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_x_0+=     0.44402496796 * Math.cos( 1.65967519586 +      149.56319713460*t);
      uranus_x_0+=     0.14668209481 * Math.cos( 3.42395862804 +       73.29712585900*t);
      uranus_x_0+=     0.14130269479 * Math.cos( 4.39572927934 +       76.26607127560*t);
      uranus_x_0+=     0.06201106178 * Math.cos( 5.14043574125 +        1.48447270830*t);
      uranus_x_0+=     0.01542951343 * Math.cos( 4.12121838072 +      224.34479570190*t);
      uranus_x_0+=     0.01444216660 * Math.cos( 2.65117115201 +      148.07872442630*t);
      uranus_x_0+=     0.00944995563 * Math.cos( 1.65869338757 +       11.04570026390*t);
      uranus_x_0+=     0.00657524815 * Math.cos( 0.57595170636 +      151.04766984290*t);
      uranus_x_0+=     0.00621624676 * Math.cos( 3.05882246638 +       77.75054398390*t);
      uranus_x_0+=     0.00585182542 * Math.cos( 4.79934779678 +       71.81265315070*t);
      uranus_x_0+=     0.00634000270 * Math.cos( 4.09556589724 +       63.73589830340*t);
      uranus_x_0+=     0.00547699056 * Math.cos( 3.63127725056 +       85.82729883120*t);
      uranus_x_0+=     0.00458219984 * Math.cos( 3.90788284112 +        2.96894541660*t);
      uranus_x_0+=     0.00496087649 * Math.cos( 0.59947400861 +      529.69096509460*t);
      uranus_x_0+=     0.00383625535 * Math.cos( 6.18762010576 +      138.51749687070*t);
      uranus_x_0+=     0.00267938156 * Math.cos( 0.96885660137 +      213.29909543800*t);
      uranus_x_0+=     0.00215368005 * Math.cos( 5.30877641428 +       38.13303563780*t);
      uranus_x_0+=     0.00145505389 * Math.cos( 2.31759757085 +       70.84944530420*t);
      uranus_x_0+=     0.00135340032 * Math.cos( 5.51062460816 +       78.71375183040*t);
      uranus_x_0+=     0.00119593859 * Math.cos( 4.10138544267 +       39.61750834610*t);
      uranus_x_0+=     0.00125105686 * Math.cos( 2.51455273063 +      111.43016149680*t);
      uranus_x_0+=     0.00111260244 * Math.cos( 5.12252784325 +      222.86032299360*t);
      uranus_x_0+=     0.00104619827 * Math.cos( 3.90538916334 +      146.59425171800*t);
      uranus_x_0+=     0.00110125387 * Math.cos( 4.45473528724 +       35.16409022120*t);
      uranus_x_0+=     0.00063584588 * Math.cos( 0.29966233158 +      299.12639426920*t);
      uranus_x_0+=     0.00053904041 * Math.cos( 3.92590422507 +        3.93215326310*t);
      uranus_x_0+=     0.00065066905 * Math.cos( 3.73008452906 +      109.94568878850*t);
      uranus_x_0+=     0.00039181662 * Math.cos( 2.68841280769 +        4.45341812490*t);
      uranus_x_0+=     0.00034341683 * Math.cos( 3.03781661928 +      225.82926841020*t);
      uranus_x_0+=     0.00033134636 * Math.cos( 2.54201591218 +       65.22037101170*t);
      uranus_x_0+=     0.00034555652 * Math.cos( 1.84699329257 +       79.23501669220*t);
      uranus_x_0+=     0.00033867050 * Math.cos( 5.98418436103 +       70.32818044240*t);
      uranus_x_0+=     0.00028371614 * Math.cos( 2.58026657123 +      127.47179660680*t);
      uranus_x_0+=     0.00035943348 * Math.cos( 4.08754543016 +      202.25339517410*t);
      uranus_x_0+=     0.00025208833 * Math.cos( 5.30272144657 +        9.56122755560*t);
      uranus_x_0+=     0.00023467802 * Math.cos( 4.09729860322 +      145.63104387150*t);
      uranus_x_0+=     0.00022963939 * Math.cos( 5.51475073655 +       84.34282612290*t);
      uranus_x_0+=     0.00031823951 * Math.cos( 5.53948583244 +      152.53214255120*t);
      uranus_x_0+=     0.00028384953 * Math.cos( 6.01785430306 +      184.72728735580*t);
      uranus_x_0+=     0.00026657176 * Math.cos( 6.11027939727 +      160.60889739850*t);
      uranus_x_0+=     0.00019676762 * Math.cos( 5.53431398332 +       74.66972398270*t);
      uranus_x_0+=     0.00019653873 * Math.cos( 2.28660913421 +       74.89347315190*t);
      uranus_x_0+=     0.00019954280 * Math.cos( 0.57450958037 +       12.53017297220*t);
      uranus_x_0+=     0.00018565067 * Math.cos( 0.62225019017 +       52.69019803950*t);
      uranus_x_0+=     0.00020084756 * Math.cos( 4.47297488471 +       22.09140052780*t);
      uranus_x_0+=     0.00019926329 * Math.cos( 1.39878194708 +      112.91463420510*t);
      uranus_x_0+=     0.00018575632 * Math.cos( 5.70217475790 +       33.67961751290*t);
      uranus_x_0+=     0.00016587870 * Math.cos( 4.86920309163 +      108.46121608020*t);
      uranus_x_0+=     0.00015171194 * Math.cos( 2.88415453399 +       41.10198105440*t);
      uranus_x_0+=     0.00011245800 * Math.cos( 6.11597016146 +       71.60020482960*t);
      uranus_x_0+=     0.00013948521 * Math.cos( 6.27545694160 +      221.37585028530*t);
      uranus_x_0+=     0.00010798350 * Math.cos( 1.70031857078 +       77.96299230500*t);
      uranus_x_0+=     0.00013593955 * Math.cos( 2.55407820633 +       87.31177153950*t);
      uranus_x_0+=     0.00011997848 * Math.cos( 0.94875212305 +     1059.38193018920*t);
      uranus_x_0+=     0.00012884351 * Math.cos( 5.08737999470 +      145.10977900970*t);
      uranus_x_0+=     0.00012394786 * Math.cos( 6.21892878850 +       72.33391801250*t);
      uranus_x_0+=     0.00012253318 * Math.cos( 0.19452856525 +       36.64856292950*t);
      uranus_x_0+=     0.00011538642 * Math.cos( 1.77241794539 +       77.22927912210*t);
      uranus_x_0+=     0.00008738409 * Math.cos( 4.96956808452 +      186.21176006410*t);
      uranus_x_0+=     0.00007095608 * Math.cos( 1.30384750044 +      297.64192156090*t);
      uranus_x_0+=     0.00006262602 * Math.cos( 1.71385983783 +      153.49535039770*t);
      uranus_x_0+=     0.00007487302 * Math.cos( 0.11408470667 +      426.59819087600*t);
      uranus_x_0+=     0.00007798974 * Math.cos( 5.82410372587 +      340.77089204480*t);
      uranus_x_0+=     0.00006669249 * Math.cos( 5.08626589612 +       62.25142559510*t);
      uranus_x_0+=     0.00005505358 * Math.cos( 3.31282108025 +      140.00196957900*t);
      uranus_x_0+=     0.00005372927 * Math.cos( 4.12498282863 +       75.30286342910*t);
      uranus_x_0+=     0.00005354242 * Math.cos( 3.69263973447 +       74.26033370550*t);
      uranus_x_0+=     0.00004478123 * Math.cos( 1.11838191479 +       66.70484372000*t);
      uranus_x_0+=     0.00004233075 * Math.cos( 3.94913608184 +      265.98929347750*t);
      uranus_x_0+=     0.00005038353 * Math.cos( 4.68664376918 +       18.15924726470*t);
      uranus_x_0+=     0.00004570470 * Math.cos( 0.97536665751 +      183.24281464750*t);
      uranus_x_0+=     0.00004751325 * Math.cos( 4.95762395337 +       73.81839072080*t);
      uranus_x_0+=     0.00004448651 * Math.cos( 0.29436142982 +      114.39910691340*t);
      uranus_x_0+=     0.00003312340 * Math.cos( 0.52418923788 +       82.85835341460*t);
      uranus_x_0+=     0.00004515952 * Math.cos( 2.88576303120 +       75.74480641380*t);
      uranus_x_0+=     0.00003559276 * Math.cos( 1.47627607503 +        5.93789083320*t);
      uranus_x_0+=     0.00003268117 * Math.cos( 0.51827231333 +      220.41264243880*t);
      uranus_x_0+=     0.00003578235 * Math.cos( 1.11528903208 +      137.03302416240*t);
      uranus_x_0+=     0.00003004737 * Math.cos( 5.12122132051 +        7.11354700080*t);
      uranus_x_0+=     0.00002882392 * Math.cos( 2.76136583899 +      373.90799283650*t);
      uranus_x_0+=     0.00002579454 * Math.cos( 3.84784330333 +      277.03499374140*t);
      uranus_x_0+=     0.00002597765 * Math.cos( 0.22409539936 +       96.87299909510*t);
      uranus_x_0+=     0.00002560744 * Math.cos( 4.44236223450 +       80.19822453870*t);
      uranus_x_0+=     0.00002722745 * Math.cos( 6.09456175016 +      106.97674337190*t);
      uranus_x_0+=     0.00002528025 * Math.cos( 0.89508396542 +       68.84370773410*t);
      uranus_x_0+=     0.00002631138 * Math.cos( 0.04831552531 +      305.34616939270*t);
      uranus_x_0+=     0.00002541716 * Math.cos( 0.64495056482 +       32.19514480460*t);
      uranus_x_0+=     0.00002241129 * Math.cos( 5.22377697501 +        3.18139373770*t);
      uranus_x_0+=     0.00001965145 * Math.cos( 0.09207526632 +       20.60692781950*t);
      uranus_x_0+=     0.00002232022 * Math.cos( 0.63571664756 +       80.71948940050*t);
      uranus_x_0+=     0.00001933814 * Math.cos( 5.75490033864 +       74.73341445750*t);
      uranus_x_0+=     0.00001933817 * Math.cos( 2.06557585395 +       74.82978267710*t);
      uranus_x_0+=     0.00002138391 * Math.cos( 4.20897429922 +       74.52096613640*t);
      uranus_x_0+=     0.00002126427 * Math.cos( 3.61171465436 +       75.04223099820*t);
      uranus_x_0+=     0.00002215516 * Math.cos( 2.18613112875 +      259.50888592310*t);
      uranus_x_0+=     0.00001891213 * Math.cos( 5.49941424248 +      300.61086697750*t);
      uranus_x_0+=     0.00001927679 * Math.cos( 1.29228021932 +      159.12442469020*t);
      uranus_x_0+=     0.00001796558 * Math.cos( 5.73271543335 +       74.62153987290*t);
      uranus_x_0+=     0.00001792522 * Math.cos( 2.08789166984 +       74.94165726170*t);
      uranus_x_0+=     0.00001873542 * Math.cos( 4.23391867169 +      206.18554843720*t);
      uranus_x_0+=     0.00002182901 * Math.cos( 1.23755478345 +      479.28838891550*t);
      uranus_x_0+=     0.00001860591 * Math.cos( 1.67536711716 +       42.58645376270*t);
      uranus_x_0+=     0.00002075591 * Math.cos( 3.15586933464 +      131.40394986990*t);
      uranus_x_0+=     0.00001912582 * Math.cos( 5.83091918696 +       14.97785352700*t);
      uranus_x_0+=     0.00001529180 * Math.cos( 2.05204104820 +      191.20769491020*t);
      uranus_x_0+=     0.00002064173 * Math.cos( 3.60208606410 +      835.03713448730*t);
      uranus_x_0+=     0.00001768763 * Math.cos( 1.19254481620 +      219.89137757700*t);
      uranus_x_0+=     0.00001892359 * Math.cos( 4.32128621847 +      154.01661525950*t);
      uranus_x_0+=     0.00001797047 * Math.cos( 1.73417465594 +      227.31374111850*t);
      uranus_x_0+=     0.00001558489 * Math.cos( 6.16891070489 +       59.80374504030*t);
      uranus_x_0+=     0.00001672893 * Math.cos( 0.01232646186 +      143.62530630140*t);
      uranus_x_0+=     0.00001467268 * Math.cos( 2.10975578758 +        2.44768055480*t);
      uranus_x_0+=     0.00001677659 * Math.cos( 0.42525121334 +        8.07675484730*t);
      uranus_x_0+=     0.00001347303 * Math.cos( 5.46763140224 +      288.08069400530*t);
      uranus_x_0+=     0.00001744555 * Math.cos( 0.82022450313 +       56.62235130260*t);
      uranus_x_0+=     0.00001427180 * Math.cos( 0.38786175669 +       92.94084583200*t);
      uranus_x_0+=     0.00001263032 * Math.cos( 5.63689596853 +      404.50679034820*t);
      uranus_x_0+=     0.00001221506 * Math.cos( 5.20012455894 +       54.17467074780*t);
      uranus_x_0+=     0.00001574905 * Math.cos( 5.72297800263 +       39.35687591520*t);
      uranus_x_0+=     0.00001269686 * Math.cos( 2.66330104031 +      142.44965013380*t);
      uranus_x_0+=     0.00001438869 * Math.cos( 0.72633739717 +      522.57741809380*t);
      uranus_x_0+=     0.00001408997 * Math.cos( 3.61751904356 +      536.80451209540*t);
      uranus_x_0+=     0.00001418300 * Math.cos( 2.29718712012 +      235.39049596580*t);
      uranus_x_0+=     0.00001040948 * Math.cos( 2.74644165501 +        5.41662597140*t);
      uranus_x_0+=     0.00001256867 * Math.cos( 5.61684736425 +       67.66805156650*t);
      uranus_x_0+=     0.00001164218 * Math.cos( 2.08302637541 +       81.89514556810*t);
      uranus_x_0+=     0.00001009252 * Math.cos( 2.02320517037 +       74.03083904190*t);
      uranus_x_0+=     0.00001077810 * Math.cos( 1.05685900920 +      128.95626931510*t);
      uranus_x_0+=     0.00000995392 * Math.cos( 5.79703441041 +       75.53235809270*t);
      uranus_x_0+=     0.00001212025 * Math.cos( 3.41577832660 +      211.81462272970*t);
      uranus_x_0+=     0.00001223648 * Math.cos( 3.84373514640 +      187.69623277240*t);
      uranus_x_0+=     0.00001334371 * Math.cos( 2.17621743689 +      380.12776796000*t);
      uranus_x_0+=     0.00001144565 * Math.cos( 2.42148845239 +      296.15744885260*t);
      uranus_x_0+=     0.00001241589 * Math.cos( 1.81282962357 +      134.58534360760*t);
      uranus_x_0+=     0.00001192274 * Math.cos( 5.58661990233 +       50.40257617910*t);
      uranus_x_0+=     0.00001093678 * Math.cos( 3.94451812233 +      230.56457082540*t);
      uranus_x_0+=     0.00000866728 * Math.cos( 3.65638980673 +      125.98732389850*t);
      uranus_x_0+=     0.00000858603 * Math.cos( 6.06095240605 +       68.18931642830*t);
      uranus_x_0+=     0.00000913477 * Math.cos( 1.69392733805 +      149.45132255000*t);
      uranus_x_0+=     0.00001077916 * Math.cos( 5.01417740021 +      181.75834193920*t);
      uranus_x_0+=     0.00001166898 * Math.cos( 2.02955848543 +      110.20632121940*t);
      uranus_x_0+=     0.00000858335 * Math.cos( 1.50454807667 +       89.75945209430*t);
      uranus_x_0+=     0.00001056848 * Math.cos( 5.53440854164 +       14.01464568050*t);
      uranus_x_0+=     0.00000964091 * Math.cos( 2.66151436132 +       35.42472265210*t);
      uranus_x_0+=     0.00000909790 * Math.cos( 4.72919543782 +      149.67507171920*t);
      uranus_x_0+=     0.00000987956 * Math.cos( 6.20259453944 +      203.73786788240*t);
      uranus_x_0+=     0.00000704557 * Math.cos( 1.78667248384 +       81.37388070630*t);
      uranus_x_0+=     0.00000727979 * Math.cos( 1.68450966248 +       51.20572533120*t);
      uranus_x_0+=     0.00000895034 * Math.cos( 3.38678219821 +       23.57587323610*t);
      uranus_x_0+=     0.00000862050 * Math.cos( 5.03077008764 +      162.09337010680*t);
      uranus_x_0+=     0.00000870204 * Math.cos( 5.37263296164 +       81.00137369080*t);
      uranus_x_0+=     0.00000811437 * Math.cos( 5.17638099206 +      200.76892246580*t);
      uranus_x_0+=     0.00000598538 * Math.cos( 5.04735819055 +       24.37902238820*t);
      uranus_x_0+=     0.00000766812 * Math.cos( 2.46431370490 +       68.56182344380*t);
      uranus_x_0+=     0.00000620509 * Math.cos( 3.32340073105 +       69.36497259590*t);
      uranus_x_0+=     0.00000743561 * Math.cos( 1.22664998599 +      760.25553592000*t);
      uranus_x_0+=     0.00000643798 * Math.cos( 1.27173146057 +       88.79624424780*t);
      uranus_x_0+=     0.00000696351 * Math.cos( 0.45928521046 +      116.42609634290*t);
      uranus_x_0+=     0.00000528197 * Math.cos( 2.28043920518 +      146.38180339690*t);
      uranus_x_0+=     0.00000699542 * Math.cos( 2.93566905569 +      617.80588578620*t);
      uranus_x_0+=     0.00000674539 * Math.cos( 3.06005508910 +        6.21977512350*t);
      uranus_x_0+=     0.00000587451 * Math.cos( 3.90803174254 +      152.01087768940*t);
      uranus_x_0+=     0.00000578643 * Math.cos( 2.55597699269 +       28.57180808220*t);
      uranus_x_0+=     0.00000504865 * Math.cos( 2.53585718344 +      157.63995198190*t);
      uranus_x_0+=     0.00000551887 * Math.cos( 1.14420383033 +      260.99335863140*t);
      uranus_x_0+=     0.00000476325 * Math.cos( 4.08179949822 +      415.55249061210*t);
      uranus_x_0+=     0.00000580796 * Math.cos( 6.18692743051 +      258.02441321480*t);
      uranus_x_0+=     0.00000597694 * Math.cos( 5.21701637296 +      218.40690486870*t);
      uranus_x_0+=     0.00000524337 * Math.cos( 2.29605835514 +      351.81659230870*t);
      uranus_x_0+=     0.00000445140 * Math.cos( 5.84184650462 +      120.35824960600*t);
      uranus_x_0+=     0.00000442835 * Math.cos( 3.75400855881 +      329.72519178090*t);
      uranus_x_0+=     0.00000449040 * Math.cos( 1.03508146650 +      543.02428721890*t);
      uranus_x_0+=     0.00000484827 * Math.cos( 0.33092998607 +       73.40900044360*t);
      uranus_x_0+=     0.00000438492 * Math.cos( 1.29953105341 +     1589.07289528380*t);
      uranus_x_0+=     0.00000444042 * Math.cos( 4.74854436122 +       41.64449777560*t);
      uranus_x_0+=     0.00000542001 * Math.cos( 1.04883718038 +      195.13984817330*t);
      uranus_x_0+=     0.00000435208 * Math.cos( 3.76518154062 +      372.42352012820*t);
      uranus_x_0+=     0.00000419163 * Math.cos( 1.97405677459 +       95.38852638680*t);
      uranus_x_0+=     0.00000514155 * Math.cos( 5.40820017990 +      115.88357962170*t);
      uranus_x_0+=     0.00000387375 * Math.cos( 5.96869839758 +      152.74459087230*t);
      uranus_x_0+=     0.00000408499 * Math.cos( 3.42756156092 +        0.96320784650*t);
      uranus_x_0+=     0.00000374730 * Math.cos( 5.67831880744 +      144.14657116320*t);
      uranus_x_0+=     0.00000433546 * Math.cos( 4.11248357579 +      209.36694217490*t);
      uranus_x_0+=     0.00000384413 * Math.cos( 5.21546597177 +      114.13847448250*t);
      uranus_x_0+=     0.00000427408 * Math.cos( 2.47035624732 +      141.48644228730*t);
      uranus_x_0+=     0.00000371413 * Math.cos( 3.47157274946 +       73.18525127440*t);
      uranus_x_0+=     0.00000371243 * Math.cos( 1.03748816404 +      105.49227066360*t);
      uranus_x_0+=     0.00000318357 * Math.cos( 0.22505788913 +       33.13710079170*t);
      uranus_x_0+=     0.00000326002 * Math.cos( 4.18918332052 +      228.27694896500*t);
      uranus_x_0+=     0.00000416253 * Math.cos( 4.17578438146 +      490.33408917940*t);
      uranus_x_0+=     0.00000327618 * Math.cos( 0.75068049756 +       46.20979048510*t);
      uranus_x_0+=     0.00000351601 * Math.cos( 6.23854037301 +      214.78356814630*t);
      uranus_x_0+=     0.00000404322 * Math.cos( 2.13001764328 +       99.16062095550*t);
      uranus_x_0+=     0.00000295859 * Math.cos( 2.62881674222 +      103.09277421860*t);
      uranus_x_0+=     0.00000326652 * Math.cos( 0.26933343606 +        7.42236354150*t);
      uranus_x_0+=     0.00000314386 * Math.cos( 3.82461196975 +       45.57665103870*t);
      uranus_x_0+=     0.00000323118 * Math.cos( 1.86185830328 +       30.71067209630*t);
      uranus_x_0+=     0.00000300220 * Math.cos( 2.12651918134 +        6.59228213900*t);
      uranus_x_0+=     0.00000312412 * Math.cos( 3.02884222738 +      419.48464387520*t);
      uranus_x_0+=     0.00000311772 * Math.cos( 2.38235128420 +      147.11551657980*t);
      uranus_x_0+=     0.00000368105 * Math.cos( 5.45799824106 +      255.05546779820*t);
      uranus_x_0+=     0.00000346148 * Math.cos( 4.51747810137 +      454.90936652730*t);
      uranus_x_0+=     0.00000321808 * Math.cos( 0.08789094066 +      180.27386923090*t);
      uranus_x_0+=     0.00000337319 * Math.cos( 5.17833136955 +      150.52640498110*t);
      uranus_x_0+=     0.00000308588 * Math.cos( 5.63599850744 +      639.89728631400*t);
      uranus_x_0+=     0.00000251931 * Math.cos( 1.50053452494 +       19.12245511120*t);
      uranus_x_0+=     0.00000252403 * Math.cos( 0.29915395892 +      150.08446199640*t);
      uranus_x_0+=     0.00000278704 * Math.cos( 1.17271973925 +       29.20494752860*t);
      uranus_x_0+=     0.00000266863 * Math.cos( 5.73005045142 +       28.31117565130*t);
      uranus_x_0+=     0.00000238805 * Math.cos( 5.52577063741 +      554.06998748280*t);
      uranus_x_0+=     0.00000305829 * Math.cos( 1.75242813997 +     6283.07584999140*t);
      uranus_x_0+=     0.00000299247 * Math.cos( 1.99799825842 +      984.60033162190*t);
      uranus_x_0+=     0.00000226271 * Math.cos( 5.35719329331 +      120.99138905240*t);
      uranus_x_0+=     0.00000215050 * Math.cos( 2.10000017027 +       67.35923502580*t);
      uranus_x_0+=     0.00000198057 * Math.cos( 4.76361127500 +       69.67378913660*t);
      uranus_x_0+=     0.00000220399 * Math.cos( 0.46944876871 +       44.07092647100*t);
      uranus_x_0+=     0.00000219523 * Math.cos( 5.01086928137 +       47.69426319340*t);
      uranus_x_0+=     0.00000213140 * Math.cos( 4.90437681706 +        0.52126486180*t);
      uranus_x_0+=     0.00000258423 * Math.cos( 5.01692232937 +     1289.94650101460*t);
      uranus_x_0+=     0.00000185610 * Math.cos( 4.14658641505 +       55.65914345610*t);
      uranus_x_0+=     0.00000216839 * Math.cos( 2.64528788158 +      316.39186965660*t);
      uranus_x_0+=     0.00000241311 * Math.cos( 4.64092150995 +      756.32338265690*t);
      uranus_x_0+=     0.00000222625 * Math.cos( 1.63499247598 +      155.78297225810*t);
      uranus_x_0+=     0.00000204428 * Math.cos( 1.23043556439 +      142.14083359310*t);
      uranus_x_0+=     0.00000231243 * Math.cos( 4.34962187207 +       46.47042291600*t);
      uranus_x_0+=     0.00000231117 * Math.cos( 0.59598761086 +      339.28641933650*t);
      uranus_x_0+=     0.00000214402 * Math.cos( 2.75106858640 +      189.18070548070*t);
      uranus_x_0+=     0.00000240160 * Math.cos( 1.57472247802 +      342.25536475310*t);
      uranus_x_0+=     0.00000173507 * Math.cos( 3.07143937754 +       79.88940799800*t);
      uranus_x_0+=     0.00000175735 * Math.cos( 3.10617729573 +       57.25549074900*t);
      uranus_x_0+=     0.00000166885 * Math.cos( 0.92704904427 +       30.05628079050*t);
      uranus_x_0+=     0.00000173052 * Math.cos( 2.71901382868 +      681.54178408960*t);
      uranus_x_0+=     0.00000212210 * Math.cos( 2.48249922098 +      135.54855145410*t);
      uranus_x_0+=     0.00000164032 * Math.cos( 5.42438913166 +      468.24268865160*t);
      uranus_x_0+=     0.00000203487 * Math.cos( 1.11695843604 +      148.59998928810*t);
      uranus_x_0+=     0.00000156930 * Math.cos( 4.49200656712 +       92.30770638560*t);
      uranus_x_0+=     0.00000165255 * Math.cos( 0.65702015844 +      154.97982310600*t);
      uranus_x_0+=     0.00000185802 * Math.cos( 5.56639953504 +       73.88782669000*t);
      uranus_x_0+=     0.00000185802 * Math.cos( 2.25459555455 +       75.67537044460*t);
      uranus_x_0+=     0.00000174776 * Math.cos( 0.64896858671 +      103.35340664950*t);
      uranus_x_0+=     0.00000187624 * Math.cos( 6.19491337250 +      149.04193227280*t);
      uranus_x_0+=     0.00000193532 * Math.cos( 6.21234933839 +       60.76695288680*t);
      uranus_x_0+=     0.00000160061 * Math.cos( 5.01823584858 +      264.50482076920*t);
      uranus_x_0+=     0.00000185820 * Math.cos( 1.04769695695 +       76.15419669100*t);
      uranus_x_0+=     0.00000197311 * Math.cos( 1.21765365835 +      256.53994050650*t);
      uranus_x_0+=     0.00000175478 * Math.cos( 2.83270040396 +      333.65734504400*t);
      uranus_x_0+=     0.00000157905 * Math.cos( 5.70734466920 +       82.20396210880*t);
      uranus_x_0+=     0.00000182625 * Math.cos( 0.27259358854 +      216.92243216040*t);
      uranus_x_0+=     0.00000147918 * Math.cos( 1.82282570469 +       17.52610781830*t);
      uranus_x_0+=     0.00000177450 * Math.cos( 5.10372503690 +      685.47393735270*t);
      uranus_x_0+=     0.00000137789 * Math.cos( 5.22295277421 +      448.68959140380*t);
      uranus_x_0+=     0.00000189430 * Math.cos( 5.63043055528 +      291.70403072770*t);
      uranus_x_0+=     0.00000152602 * Math.cos( 3.60417761486 +      233.90602325750*t);
      uranus_x_0+=     0.00000141512 * Math.cos( 6.28314137970 +      130.44074202340*t);
      uranus_x_0+=     0.00000134010 * Math.cos( 3.97075396565 +      156.15547927360*t);
      uranus_x_0+=     0.00000136823 * Math.cos( 2.06403429379 +       16.67477455640*t);
      uranus_x_0+=     0.00000129045 * Math.cos( 6.13432221167 +       76.47851959670*t);
      uranus_x_0+=     0.00000146031 * Math.cos( 6.21320130613 +      294.67297614430*t);
      uranus_x_0+=     0.00000146362 * Math.cos( 4.63496106478 +      334.29048449040*t);
      uranus_x_0+=     0.00000177477 * Math.cos( 3.17856650199 +    10213.28554621100*t);
      uranus_x_0+=     0.00000153385 * Math.cos( 5.73024384991 +      347.88443904560*t);
      uranus_x_0+=     0.00000127869 * Math.cos( 1.20450690573 +       61.44827644300*t);
      uranus_x_0+=     0.00000150311 * Math.cos( 6.16854891408 +      173.94221952280*t);
      uranus_x_0+=     0.00000138900 * Math.cos( 6.09258539376 +      286.59622129700*t);
      uranus_x_0+=     0.00000141169 * Math.cos( 3.15247546979 +       24.11838995730*t);
      uranus_x_0+=     0.00000115436 * Math.cos( 3.64215841031 +       13.33332212430*t);
      uranus_x_0+=     0.00000111293 * Math.cos( 0.10667309735 +       88.11492069160*t);
      uranus_x_0+=     0.00000121087 * Math.cos( 0.17422963984 +       79.44746501330*t);
      uranus_x_0+=     0.00000108657 * Math.cos( 0.23419995878 +       66.91729204110*t);
      uranus_x_0+=     0.00000109513 * Math.cos( 1.37565056754 +       44.72531777680*t);
      uranus_x_0+=     0.00000128511 * Math.cos( 1.87873176315 +      254.94359321360*t);
      uranus_x_0+=     0.00000115349 * Math.cos( 0.88899033684 +      692.58748435350*t);
      uranus_x_0+=     0.00000135117 * Math.cos( 2.72548252468 +      171.65459766240*t);
      uranus_x_0+=     0.00000125714 * Math.cos( 5.43040501453 +       98.35747180340*t);
      uranus_x_0+=     0.00000104433 * Math.cos( 1.66540127359 +       54.33472944220*t);
      uranus_x_0+=     0.00000128791 * Math.cos( 3.10899630296 +      155.50108796780*t);
      uranus_x_0+=     0.00000105829 * Math.cos( 1.67999980378 +      375.39246554480*t);
      uranus_x_0+=     0.00000109272 * Math.cos( 3.18774824824 +      273.10284047830*t);
      uranus_x_0+=     0.00000100410 * Math.cos( 1.92606761482 +      362.86229257260*t);
      uranus_x_0+=     0.00000127008 * Math.cos( 5.83706831293 +      628.85158605010*t);
      uranus_x_0+=     0.00000102158 * Math.cos( 1.42491352478 +        0.11187458460*t);
      uranus_x_0+=     0.00000115884 * Math.cos( 5.55755283511 +      632.78373931320*t);
      uranus_x_0+=     0.00000106157 * Math.cos( 4.21108144267 +      302.09533968580*t);
      uranus_x_0+=     0.00000115494 * Math.cos( 2.79386838622 +      604.47256366190*t);
      uranus_x_0+=     0.00000109946 * Math.cos( 1.23547347355 +      100.38446123290*t);
      uranus_x_0+=     0.00000111791 * Math.cos( 3.59906622192 +       19.64371997300*t);
      uranus_x_0+=     0.00000104717 * Math.cos( 0.00910187496 +      433.71173787680*t);
      uranus_x_0+=     0.00000108044 * Math.cos( 0.47218816752 +      253.57099508990*t);
      uranus_x_0+=     0.00000115664 * Math.cos( 2.63306868216 +     1215.16490244730*t);
      uranus_x_0+=     0.00000112324 * Math.cos( 0.51418380423 +      228.79821382680*t);
      uranus_x_0+=     0.00000106858 * Math.cos( 3.13973175313 +       81.68269724700*t);
      uranus_x_0+=     0.00000108382 * Math.cos( 0.01637987560 +     1162.47470440780*t);
      uranus_x_0+=     0.00000100821 * Math.cos( 4.69066192585 +      210.33015002140*t);

      let uranus_x_1=0.0;
      uranus_x_1+=     0.00739730021 * Math.cos( 6.01067825116 +      149.56319713460*t);
      uranus_x_1+=     0.00526878306 * Math.cos( 3.14159265359 +        0.00000000000*t);
      uranus_x_1+=     0.00239840801 * Math.cos( 5.33657762707 +       73.29712585900*t);
      uranus_x_1+=     0.00229676787 * Math.cos( 2.48204455775 +       76.26607127560*t);
      uranus_x_1+=     0.00111045158 * Math.cos( 5.57157235960 +       11.04570026390*t);
      uranus_x_1+=     0.00096352822 * Math.cos( 0.35070389084 +       63.73589830340*t);
      uranus_x_1+=     0.00081511870 * Math.cos( 1.21058618039 +       85.82729883120*t);
      uranus_x_1+=     0.00045687564 * Math.cos( 2.29216583843 +      138.51749687070*t);
      uranus_x_1+=     0.00051382501 * Math.cos( 2.18935125260 +      224.34479570190*t);
      uranus_x_1+=     0.00038844330 * Math.cos( 0.30724575951 +       70.84944530420*t);
      uranus_x_1+=     0.00036158493 * Math.cos( 1.23634798757 +       78.71375183040*t);
      uranus_x_1+=     0.00032333094 * Math.cos( 5.06666556704 +       74.78159856730*t);
      uranus_x_1+=     0.00021685656 * Math.cos( 4.93710968392 +      151.04766984290*t);
      uranus_x_1+=     0.00019441970 * Math.cos( 1.30617490304 +       77.75054398390*t);
      uranus_x_1+=     0.00017376241 * Math.cos( 0.24607221230 +       71.81265315070*t);
      uranus_x_1+=     0.00015211071 * Math.cos( 5.53141633140 +        3.93215326310*t);
      uranus_x_1+=     0.00007735984 * Math.cos( 1.61349552789 +       71.60020482960*t);
      uranus_x_1+=     0.00007425078 * Math.cos( 6.20357977116 +       77.96299230500*t);
      uranus_x_1+=     0.00006995857 * Math.cos( 2.40633283814 +      145.63104387150*t);
      uranus_x_1+=     0.00007291691 * Math.cos( 2.23597571444 +        2.96894541660*t);
      uranus_x_1+=     0.00007585264 * Math.cos( 2.76074218330 +      148.07872442630*t);
      uranus_x_1+=     0.00004378335 * Math.cos( 3.74296322240 +      160.60889739850*t);
      uranus_x_1+=     0.00004127713 * Math.cos( 1.48475181305 +       22.09140052780*t);
      uranus_x_1+=     0.00003933541 * Math.cos( 4.73864204208 +       65.22037101170*t);
      uranus_x_1+=     0.00002910312 * Math.cos( 5.91941333050 +      127.47179660680*t);
      uranus_x_1+=     0.00002788434 * Math.cos( 4.90117297196 +      213.29909543800*t);
      uranus_x_1+=     0.00002802392 * Math.cos( 3.76505436434 +       52.69019803950*t);
      uranus_x_1+=     0.00002545264 * Math.cos( 3.36768337628 +        9.56122755560*t);
      uranus_x_1+=     0.00002647073 * Math.cos( 4.53813176345 +       12.53017297220*t);
      uranus_x_1+=     0.00003177614 * Math.cos( 4.65226634926 +      299.12639426920*t);
      uranus_x_1+=     0.00002228396 * Math.cos( 0.18087986338 +       87.31177153950*t);
      uranus_x_1+=     0.00002824668 * Math.cos( 3.40143685673 +       84.34282612290*t);
      uranus_x_1+=     0.00002525203 * Math.cos( 2.83821144961 +       18.15924726470*t);
      uranus_x_1+=     0.00002216987 * Math.cos( 4.78338909951 +       72.33391801250*t);
      uranus_x_1+=     0.00001624493 * Math.cos( 3.75817281127 +      153.49535039770*t);
      uranus_x_1+=     0.00001928881 * Math.cos( 2.39940180311 +       39.61750834610*t);
      uranus_x_1+=     0.00001555444 * Math.cos( 4.13741667297 +       73.81839072080*t);
      uranus_x_1+=     0.00001600865 * Math.cos( 0.08376247543 +       79.23501669220*t);
      uranus_x_1+=     0.00001476317 * Math.cos( 3.67283851029 +       75.74480641380*t);
      uranus_x_1+=     0.00001427088 * Math.cos( 1.45690759014 +       70.32818044240*t);
      uranus_x_1+=     0.00001533469 * Math.cos( 3.71776498048 +      152.53214255120*t);
      uranus_x_1+=     0.00001747266 * Math.cos( 3.24870046809 +       77.22927912210*t);
      uranus_x_1+=     0.00001716831 * Math.cos( 3.39415662657 +      222.86032299360*t);
      uranus_x_1+=     0.00001707504 * Math.cos( 1.11296012106 +      225.82926841020*t);
      uranus_x_1+=     0.00001734228 * Math.cos( 5.39619902298 +      146.59425171800*t);
      uranus_x_1+=     0.00001476617 * Math.cos( 3.53047075439 +        3.18139373770*t);
      uranus_x_1+=     0.00001179645 * Math.cos( 5.13953276367 +      220.41264243880*t);
      uranus_x_1+=     0.00001239315 * Math.cos( 0.98221206501 +        4.45341812490*t);
      uranus_x_1+=     0.00001099691 * Math.cos( 1.35138854505 +       62.25142559510*t);
      uranus_x_1+=     0.00000977123 * Math.cos( 1.01847642495 +       74.66972398270*t);
      uranus_x_1+=     0.00000975571 * Math.cos( 0.51903242150 +       74.89347315190*t);
      uranus_x_1+=     0.00001061312 * Math.cos( 5.00125105380 +      131.40394986990*t);
      uranus_x_1+=     0.00000891654 * Math.cos( 4.27405127452 +      426.59819087600*t);
      uranus_x_1+=     0.00001029261 * Math.cos( 5.42434597865 +      109.94568878850*t);
      uranus_x_1+=     0.00000868857 * Math.cos( 2.79792544805 +       56.62235130260*t);
      uranus_x_1+=     0.00000747420 * Math.cos( 4.78455200239 +       92.94084583200*t);
      uranus_x_1+=     0.00000743194 * Math.cos( 5.94179390589 +      206.18554843720*t);
      uranus_x_1+=     0.00000828266 * Math.cos( 3.32679639479 +        7.11354700080*t);
      uranus_x_1+=     0.00000647136 * Math.cos( 0.20307260484 +       80.19822453870*t);
      uranus_x_1+=     0.00000720965 * Math.cos( 0.28353896718 +        1.48447270830*t);
      uranus_x_1+=     0.00000605458 * Math.cos( 0.10335604387 +     1059.38193018920*t);
      uranus_x_1+=     0.00000666117 * Math.cos( 3.49754791028 +       96.87299909510*t);
      uranus_x_1+=     0.00000575550 * Math.cos( 2.42897662546 +      522.57741809380*t);
      uranus_x_1+=     0.00000497791 * Math.cos( 3.50054849965 +      137.03302416240*t);
      uranus_x_1+=     0.00000563791 * Math.cos( 1.91500933518 +      536.80451209540*t);
      uranus_x_1+=     0.00000477254 * Math.cos( 1.15791167960 +       41.10198105440*t);
      uranus_x_1+=     0.00000452889 * Math.cos( 1.09710482126 +       67.66805156650*t);
      uranus_x_1+=     0.00000412572 * Math.cos( 3.78953003468 +       66.70484372000*t);
      uranus_x_1+=     0.00000408503 * Math.cos( 0.33951833274 +       81.89514556810*t);
      uranus_x_1+=     0.00000369265 * Math.cos( 4.73183141111 +      202.25339517410*t);
      uranus_x_1+=     0.00000395742 * Math.cos( 1.58893964955 +       14.97785352700*t);
      uranus_x_1+=     0.00000377813 * Math.cos( 3.73353761428 +        2.44768055480*t);
      uranus_x_1+=     0.00000347012 * Math.cos( 6.15993155091 +      134.58534360760*t);
      uranus_x_1+=     0.00000347209 * Math.cos( 4.09740378576 +      146.38180339690*t);
      uranus_x_1+=     0.00000346276 * Math.cos( 3.88647750381 +       59.80374504030*t);
      uranus_x_1+=     0.00000343714 * Math.cos( 4.42446342755 +      142.44965013380*t);
      uranus_x_1+=     0.00000294160 * Math.cos( 4.42096282169 +        5.41662597140*t);
      uranus_x_1+=     0.00000329148 * Math.cos( 5.84103283969 +      112.91463420510*t);
      uranus_x_1+=     0.00000340830 * Math.cos( 1.84893689186 +       36.64856292950*t);
      uranus_x_1+=     0.00000306476 * Math.cos( 1.06590600726 +       33.67961751290*t);
      uranus_x_1+=     0.00000275437 * Math.cos( 4.10479793303 +       82.85835341460*t);
      uranus_x_1+=     0.00000293125 * Math.cos( 0.49846117327 +      145.10977900970*t);
      uranus_x_1+=     0.00000254628 * Math.cos( 6.25473678549 +      235.39049596580*t);
      uranus_x_1+=     0.00000246505 * Math.cos( 5.32024438086 +      159.12442469020*t);
      uranus_x_1+=     0.00000249949 * Math.cos( 0.67221714016 +      265.98929347750*t);
      uranus_x_1+=     0.00000235773 * Math.cos( 3.62653751252 +       20.60692781950*t);
      uranus_x_1+=     0.00000217183 * Math.cos( 4.25583219062 +      152.74459087230*t);
      uranus_x_1+=     0.00000210343 * Math.cos( 4.63336622628 +      140.00196957900*t);
      uranus_x_1+=     0.00000231137 * Math.cos( 0.38954829748 +      108.46121608020*t);
      uranus_x_1+=     0.00000183920 * Math.cos( 5.05228486550 +      191.20769491020*t);
      uranus_x_1+=     0.00000221484 * Math.cos( 2.71939746995 +      195.13984817330*t);
      uranus_x_1+=     0.00000192825 * Math.cos( 0.45904824372 +       23.57587323610*t);
      uranus_x_1+=     0.00000228031 * Math.cos( 5.73832504591 +      297.64192156090*t);
      uranus_x_1+=     0.00000181760 * Math.cos( 1.50820819426 +      120.35824960600*t);
      uranus_x_1+=     0.00000160927 * Math.cos( 4.77614458093 +        8.07675484730*t);
      uranus_x_1+=     0.00000154383 * Math.cos( 0.90699803576 +      288.08069400530*t);
      uranus_x_1+=     0.00000164982 * Math.cos( 6.03209867187 +        5.93789083320*t);
      uranus_x_1+=     0.00000153438 * Math.cos( 2.70088223137 +      162.09337010680*t);
      uranus_x_1+=     0.00000191778 * Math.cos( 0.83177362607 +      373.90799283650*t);
      uranus_x_1+=     0.00000154090 * Math.cos( 3.25708486897 +       14.01464568050*t);
      uranus_x_1+=     0.00000177817 * Math.cos( 2.38327279626 +      209.36694217490*t);
      uranus_x_1+=     0.00000150916 * Math.cos( 1.30817182471 +       69.36497259590*t);
      uranus_x_1+=     0.00000143519 * Math.cos( 5.80839382745 +      211.81462272970*t);
      uranus_x_1+=     0.00000140612 * Math.cos( 5.35931699754 +       29.20494752860*t);
      uranus_x_1+=     0.00000141703 * Math.cos( 2.64874298288 +       68.84370773410*t);
      uranus_x_1+=     0.00000134614 * Math.cos( 0.41866243813 +       39.35687591520*t);
      uranus_x_1+=     0.00000140275 * Math.cos( 5.15925110927 +       80.71948940050*t);
      uranus_x_1+=     0.00000148005 * Math.cos( 3.01901836595 +      186.21176006410*t);
      uranus_x_1+=     0.00000138435 * Math.cos( 0.38546052988 +       81.00137369080*t);
      uranus_x_1+=     0.00000156471 * Math.cos( 3.62049946715 +      116.42609634290*t);
      uranus_x_1+=     0.00000142032 * Math.cos( 4.72599483352 +      114.39910691340*t);
      uranus_x_1+=     0.00000132979 * Math.cos( 1.16919556561 +       68.56182344380*t);
      uranus_x_1+=     0.00000132271 * Math.cos( 3.93102400599 +       89.75945209430*t);
      uranus_x_1+=     0.00000117645 * Math.cos( 1.04577241570 +      277.03499374140*t);
      uranus_x_1+=     0.00000115855 * Math.cos( 3.50608314585 +       33.13710079170*t);
      uranus_x_1+=     0.00000116656 * Math.cos( 4.77768622576 +       99.16062095550*t);
      uranus_x_1+=     0.00000118667 * Math.cos( 0.97921601472 +      305.34616939270*t);
      uranus_x_1+=     0.00000141195 * Math.cos( 5.83532011809 +       45.57665103870*t);
      uranus_x_1+=     0.00000124069 * Math.cos( 1.48589888078 +       41.64449777560*t);
      uranus_x_1+=     0.00000110901 * Math.cos( 4.69277387714 +       51.20572533120*t);
      uranus_x_1+=     0.00000119992 * Math.cos( 2.88407866671 +       50.40257617910*t);
      uranus_x_1+=     0.00000121041 * Math.cos( 2.51714592201 +      154.01661525950*t);
      uranus_x_1+=     0.00000109540 * Math.cos( 5.23116357278 +       88.79624424780*t);
      uranus_x_1+=     0.00000103214 * Math.cos( 3.71629269070 +      144.14657116320*t);
      uranus_x_1+=     0.00000103776 * Math.cos( 2.10287854036 +       54.17467074780*t);
      uranus_x_1+=     0.00000116279 * Math.cos( 6.16263578313 +      227.31374111850*t);
      uranus_x_1+=     0.00000122915 * Math.cos( 3.57188972236 +      300.61086697750*t);
      uranus_x_1+=     0.00000102736 * Math.cos( 5.34763165471 +      152.01087768940*t);
      uranus_x_1=uranus_x_1 * t;

      let uranus_x_2=0.0;
      uranus_x_2+=     0.00016015732 * Math.cos( 3.83700026619 +       74.78159856730*t);
      uranus_x_2+=     0.00010915299 * Math.cos( 3.02987776270 +      149.56319713460*t);
      uranus_x_2+=     0.00007497619 * Math.cos( 3.83429136661 +       11.04570026390*t);
      uranus_x_2+=     0.00008053623 * Math.cos( 2.54646146122 +       63.73589830340*t);
      uranus_x_2+=     0.00005408033 * Math.cos( 4.78033642303 +       70.84944530420*t);
      uranus_x_2+=     0.00005021971 * Math.cos( 3.04632772928 +       78.71375183040*t);
      uranus_x_2+=     0.00006717313 * Math.cos( 5.31264214501 +       85.82729883120*t);
      uranus_x_2+=     0.00005284684 * Math.cos( 2.11901942097 +       73.29712585900*t);
      uranus_x_2+=     0.00004874936 * Math.cos( 5.68616132176 +       76.26607127560*t);
      uranus_x_2+=     0.00003002124 * Math.cos( 4.07944398452 +      138.51749687070*t);
      uranus_x_2+=     0.00002521797 * Math.cos( 3.36028253173 +       71.60020482960*t);
      uranus_x_2+=     0.00002413832 * Math.cos( 4.45865225690 +       77.96299230500*t);
      uranus_x_2+=     0.00002221373 * Math.cos( 0.87427485235 +        3.93215326310*t);
      uranus_x_2+=     0.00002291767 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_x_2+=     0.00001040250 * Math.cos( 0.73133408837 +      145.63104387150*t);
      uranus_x_2+=     0.00001046100 * Math.cos( 5.85311910228 +      224.34479570190*t);
      uranus_x_2+=     0.00000661586 * Math.cos( 1.01544505345 +       18.15924726470*t);
      uranus_x_2+=     0.00000497229 * Math.cos( 5.27733214183 +       22.09140052780*t);
      uranus_x_2+=     0.00000502471 * Math.cos( 2.22514214710 +      151.04766984290*t);
      uranus_x_2+=     0.00000478348 * Math.cos( 3.19107941219 +       72.33391801250*t);
      uranus_x_2+=     0.00000382454 * Math.cos( 5.20159531773 +       77.75054398390*t);
      uranus_x_2+=     0.00000469767 * Math.cos( 1.82481202242 +        3.18139373770*t);
      uranus_x_2+=     0.00000403174 * Math.cos( 1.56215178272 +      160.60889739850*t);
      uranus_x_2+=     0.00000329455 * Math.cos( 2.55333634094 +       71.81265315070*t);
      uranus_x_2+=     0.00000384741 * Math.cos( 4.73239324750 +       77.22927912210*t);
      uranus_x_2+=     0.00000335931 * Math.cos( 0.05377868960 +       65.22037101170*t);
      uranus_x_2+=     0.00000281380 * Math.cos( 0.54117101233 +      131.40394986990*t);
      uranus_x_2+=     0.00000266860 * Math.cos( 0.01657445784 +       52.69019803950*t);
      uranus_x_2+=     0.00000234876 * Math.cos( 4.75379495234 +       56.62235130260*t);
      uranus_x_2+=     0.00000247761 * Math.cos( 2.17938049654 +      127.47179660680*t);
      uranus_x_2+=     0.00000219378 * Math.cos( 3.47071742536 +      220.41264243880*t);
      uranus_x_2+=     0.00000301025 * Math.cos( 1.77677607945 +       84.34282612290*t);
      uranus_x_2+=     0.00000284485 * Math.cos( 5.80269050272 +      148.07872442630*t);
      uranus_x_2+=     0.00000205875 * Math.cos( 2.90044450656 +       92.94084583200*t);
      uranus_x_2+=     0.00000211227 * Math.cos( 5.58201664740 +      153.49535039770*t);
      uranus_x_2+=     0.00000198069 * Math.cos( 2.71231997005 +       12.53017297220*t);
      uranus_x_2+=     0.00000204743 * Math.cos( 4.25027722017 +       87.31177153950*t);
      uranus_x_2+=     0.00000152803 * Math.cos( 1.37513831090 +      206.18554843720*t);
      uranus_x_2+=     0.00000139847 * Math.cos( 1.67730385016 +        9.56122755560*t);
      uranus_x_2+=     0.00000138451 * Math.cos( 1.03809761305 +      213.29909543800*t);
      uranus_x_2+=     0.00000117677 * Math.cos( 4.12702744572 +      522.57741809380*t);
      uranus_x_2+=     0.00000114603 * Math.cos( 0.21128941925 +      536.80451209540*t);
      uranus_x_2+=     0.00000121438 * Math.cos( 1.52422428772 +        7.11354700080*t);
      uranus_x_2+=     0.00000106322 * Math.cos( 5.89383486521 +      146.38180339690*t);
      uranus_x_2+=     0.00000103834 * Math.cos( 3.59301778375 +       62.25142559510*t);
      uranus_x_2=uranus_x_2 * t * t;

      let uranus_x_3=0.0;
      uranus_x_3+=     0.00001307049 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_x_3+=     0.00000679651 * Math.cos( 2.93375081556 +       70.84944530420*t);
      uranus_x_3+=     0.00000631782 * Math.cos( 4.88998230611 +       78.71375183040*t);
      uranus_x_3+=     0.00000578540 * Math.cos( 0.78827411585 +      149.56319713460*t);
      uranus_x_3+=     0.00000555324 * Math.cos( 4.67554978713 +       63.73589830340*t);
      uranus_x_3+=     0.00000455887 * Math.cos( 3.17331985662 +       85.82729883120*t);
      uranus_x_3+=     0.00000428312 * Math.cos( 4.09419341772 +       73.29712585900*t);
      uranus_x_3+=     0.00000408432 * Math.cos( 3.72971926457 +       76.26607127560*t);
      uranus_x_3+=     0.00000446893 * Math.cos( 5.00810179500 +       71.60020482960*t);
      uranus_x_3+=     0.00000424302 * Math.cos( 2.81325875072 +       77.96299230500*t);
      uranus_x_3+=     0.00000344605 * Math.cos( 2.22416564687 +       11.04570026390*t);
      uranus_x_3+=     0.00000253001 * Math.cos( 2.51182572008 +        3.93215326310*t);
      uranus_x_3+=     0.00000188565 * Math.cos( 0.81232221065 +       74.78159856730*t);
      uranus_x_3+=     0.00000132014 * Math.cos( 5.73012783198 +      138.51749687070*t);
      uranus_x_3+=     0.00000120517 * Math.cos( 5.48054814455 +       18.15924726470*t);
      uranus_x_3+=     0.00000121340 * Math.cos( 5.32278814741 +      145.63104387150*t);
      uranus_x_3=uranus_x_3 * t * t * t;

      return uranus_x_0+uranus_x_1+uranus_x_2+uranus_x_3;
   }

   static uranus_y(t){
      let uranus_y_0=0.0;
      uranus_y_0+=    19.16518231584 * Math.cos( 3.91045677002 +       74.78159856730*t);
      uranus_y_0+=     0.44390465203 * Math.cos( 0.08884111329 +      149.56319713460*t);
      uranus_y_0+=     0.16256125476 * Math.cos( 3.14159265359 +        0.00000000000*t);
      uranus_y_0+=     0.14755940186 * Math.cos( 1.85423280679 +       73.29712585900*t);
      uranus_y_0+=     0.14123958128 * Math.cos( 2.82486076549 +       76.26607127560*t);
      uranus_y_0+=     0.06250078231 * Math.cos( 3.56960243857 +        1.48447270830*t);
      uranus_y_0+=     0.01542668264 * Math.cos( 2.55040539213 +      224.34479570190*t);
      uranus_y_0+=     0.01442356575 * Math.cos( 1.08004542712 +      148.07872442630*t);
      uranus_y_0+=     0.00938975501 * Math.cos( 0.09275714761 +       11.04570026390*t);
      uranus_y_0+=     0.00650331846 * Math.cos( 2.76142680222 +       63.73589830340*t);
      uranus_y_0+=     0.00657343120 * Math.cos( 5.28830704469 +      151.04766984290*t);
      uranus_y_0+=     0.00621326770 * Math.cos( 1.48795811387 +       77.75054398390*t);
      uranus_y_0+=     0.00541961958 * Math.cos( 3.24476486661 +       71.81265315070*t);
      uranus_y_0+=     0.00547472694 * Math.cos( 2.06037924573 +       85.82729883120*t);
      uranus_y_0+=     0.00459589120 * Math.cos( 2.33745536070 +        2.96894541660*t);
      uranus_y_0+=     0.00495936105 * Math.cos( 5.31205753740 +      529.69096509460*t);
      uranus_y_0+=     0.00387922853 * Math.cos( 4.62026923885 +      138.51749687070*t);
      uranus_y_0+=     0.00268363417 * Math.cos( 5.68085299020 +      213.29909543800*t);
      uranus_y_0+=     0.00216239629 * Math.cos( 3.73800767580 +       38.13303563780*t);
      uranus_y_0+=     0.00144032475 * Math.cos( 0.75015700920 +       70.84944530420*t);
      uranus_y_0+=     0.00135290820 * Math.cos( 3.93970260616 +       78.71375183040*t);
      uranus_y_0+=     0.00119670613 * Math.cos( 2.53058783780 +       39.61750834610*t);
      uranus_y_0+=     0.00124868545 * Math.cos( 0.94315917319 +      111.43016149680*t);
      uranus_y_0+=     0.00111204860 * Math.cos( 3.55163219419 +      222.86032299360*t);
      uranus_y_0+=     0.00104507929 * Math.cos( 2.33345675603 +      146.59425171800*t);
      uranus_y_0+=     0.00108584454 * Math.cos( 6.02234848388 +       35.16409022120*t);
      uranus_y_0+=     0.00063573747 * Math.cos( 5.01204967920 +      299.12639426920*t);
      uranus_y_0+=     0.00053289771 * Math.cos( 2.38437587876 +        3.93215326310*t);
      uranus_y_0+=     0.00063774261 * Math.cos( 2.15607602904 +      109.94568878850*t);
      uranus_y_0+=     0.00039218598 * Math.cos( 1.11841109252 +        4.45341812490*t);
      uranus_y_0+=     0.00034205426 * Math.cos( 0.92405922576 +       65.22037101170*t);
      uranus_y_0+=     0.00034334377 * Math.cos( 1.46696169843 +      225.82926841020*t);
      uranus_y_0+=     0.00034538316 * Math.cos( 0.27613780697 +       79.23501669220*t);
      uranus_y_0+=     0.00039256771 * Math.cos( 5.75956853703 +      202.25339517410*t);
      uranus_y_0+=     0.00026157754 * Math.cos( 3.74097610798 +        9.56122755560*t);
      uranus_y_0+=     0.00023427328 * Math.cos( 2.52740125551 +      145.63104387150*t);
      uranus_y_0+=     0.00022933138 * Math.cos( 3.94455540350 +       84.34282612290*t);
      uranus_y_0+=     0.00031816303 * Math.cos( 3.96860170484 +      152.53214255120*t);
      uranus_y_0+=     0.00025237176 * Math.cos( 4.45141413666 +       70.32818044240*t);
      uranus_y_0+=     0.00028372491 * Math.cos( 4.44714627097 +      184.72728735580*t);
      uranus_y_0+=     0.00026652859 * Math.cos( 4.53944395347 +      160.60889739850*t);
      uranus_y_0+=     0.00019666208 * Math.cos( 3.96350065335 +       74.66972398270*t);
      uranus_y_0+=     0.00019643845 * Math.cos( 0.71577796385 +       74.89347315190*t);
      uranus_y_0+=     0.00019838981 * Math.cos( 5.29113397354 +       12.53017297220*t);
      uranus_y_0+=     0.00021523908 * Math.cos( 4.93565132068 +       36.64856292950*t);
      uranus_y_0+=     0.00015537967 * Math.cos( 1.87863275460 +       52.69019803950*t);
      uranus_y_0+=     0.00020115100 * Math.cos( 3.45473780762 +      127.47179660680*t);
      uranus_y_0+=     0.00020051641 * Math.cos( 2.90386352937 +       22.09140052780*t);
      uranus_y_0+=     0.00019901477 * Math.cos( 6.11075402434 +      112.91463420510*t);
      uranus_y_0+=     0.00018126776 * Math.cos( 0.98478853787 +       33.67961751290*t);
      uranus_y_0+=     0.00015174962 * Math.cos( 1.31314034959 +       41.10198105440*t);
      uranus_y_0+=     0.00011239020 * Math.cos( 4.54508334011 +       71.60020482960*t);
      uranus_y_0+=     0.00013948849 * Math.cos( 4.70474945682 +      221.37585028530*t);
      uranus_y_0+=     0.00010819728 * Math.cos( 0.12807029856 +       77.96299230500*t);
      uranus_y_0+=     0.00013589665 * Math.cos( 0.98313719930 +       87.31177153950*t);
      uranus_y_0+=     0.00011996772 * Math.cos( 5.66129275335 +     1059.38193018920*t);
      uranus_y_0+=     0.00012407787 * Math.cos( 4.64945783340 +       72.33391801250*t);
      uranus_y_0+=     0.00011531140 * Math.cos( 0.20190074645 +       77.22927912210*t);
      uranus_y_0+=     0.00008736150 * Math.cos( 3.39874828293 +      186.21176006410*t);
      uranus_y_0+=     0.00007093587 * Math.cos( 6.01613487245 +      297.64192156090*t);
      uranus_y_0+=     0.00006408245 * Math.cos( 3.93246367895 +       62.25142559510*t);
      uranus_y_0+=     0.00006261153 * Math.cos( 0.14258542752 +      153.49535039770*t);
      uranus_y_0+=     0.00007494000 * Math.cos( 4.82565771386 +      426.59819087600*t);
      uranus_y_0+=     0.00007856014 * Math.cos( 1.12354254831 +      340.77089204480*t);
      uranus_y_0+=     0.00005516018 * Math.cos( 1.73758326119 +      140.00196957900*t);
      uranus_y_0+=     0.00005556643 * Math.cos( 3.68095215063 +      145.10977900970*t);
      uranus_y_0+=     0.00005368405 * Math.cos( 2.55422957958 +       75.30286342910*t);
      uranus_y_0+=     0.00005350948 * Math.cos( 2.12171493922 +       74.26033370550*t);
      uranus_y_0+=     0.00004508794 * Math.cos( 5.82224064821 +       66.70484372000*t);
      uranus_y_0+=     0.00004290374 * Math.cos( 5.54490766551 +      265.98929347750*t);
      uranus_y_0+=     0.00005013871 * Math.cos( 3.11907749268 +       18.15924726470*t);
      uranus_y_0+=     0.00004326138 * Math.cos( 5.70135056853 +      183.24281464750*t);
      uranus_y_0+=     0.00004750018 * Math.cos( 3.38678300054 +       73.81839072080*t);
      uranus_y_0+=     0.00004445347 * Math.cos( 5.00638490308 +      114.39910691340*t);
      uranus_y_0+=     0.00003314154 * Math.cos( 5.23054574329 +       82.85835341460*t);
      uranus_y_0+=     0.00004509054 * Math.cos( 1.31254342829 +       75.74480641380*t);
      uranus_y_0+=     0.00003553107 * Math.cos( 6.18906516846 +        5.93789083320*t);
      uranus_y_0+=     0.00003265634 * Math.cos( 5.23063560176 +      220.41264243880*t);
      uranus_y_0+=     0.00003575435 * Math.cos( 5.83994849224 +      137.03302416240*t);
      uranus_y_0+=     0.00002880734 * Math.cos( 1.19038424330 +      373.90799283650*t);
      uranus_y_0+=     0.00002885443 * Math.cos( 3.50279993038 +        7.11354700080*t);
      uranus_y_0+=     0.00002594155 * Math.cos( 4.93691413537 +       96.87299909510*t);
      uranus_y_0+=     0.00002559357 * Math.cos( 2.87184237678 +       80.19822453870*t);
      uranus_y_0+=     0.00002676616 * Math.cos( 1.61805362044 +      305.34616939270*t);
      uranus_y_0+=     0.00002246530 * Math.cos( 5.80081898763 +      108.46121608020*t);
      uranus_y_0+=     0.00002474483 * Math.cos( 2.21173751117 +       32.19514480460*t);
      uranus_y_0+=     0.00002060991 * Math.cos( 6.24178596384 +       56.62235130260*t);
      uranus_y_0+=     0.00001958711 * Math.cos( 4.80807045815 +       20.60692781950*t);
      uranus_y_0+=     0.00002227451 * Math.cos( 5.34765264557 +       80.71948940050*t);
      uranus_y_0+=     0.00001937874 * Math.cos( 0.49529839431 +       74.82978267710*t);
      uranus_y_0+=     0.00001937871 * Math.cos( 4.18462288684 +       74.73341445750*t);
      uranus_y_0+=     0.00002164382 * Math.cos( 0.47581392325 +        3.18139373770*t);
      uranus_y_0+=     0.00002138407 * Math.cos( 2.63817804331 +       74.52096613640*t);
      uranus_y_0+=     0.00002130909 * Math.cos( 2.04143912495 +       75.04223099820*t);
      uranus_y_0+=     0.00001787737 * Math.cos( 0.32096699926 +        2.44768055480*t);
      uranus_y_0+=     0.00002212861 * Math.cos( 0.61491281306 +      259.50888592310*t);
      uranus_y_0+=     0.00001889369 * Math.cos( 3.92852240171 +      300.61086697750*t);
      uranus_y_0+=     0.00002275258 * Math.cos( 1.55666401505 +      131.40394986990*t);
      uranus_y_0+=     0.00001925946 * Math.cos( 6.00527473515 +      159.12442469020*t);
      uranus_y_0+=     0.00001802494 * Math.cos( 4.16218259902 +       74.62153987290*t);
      uranus_y_0+=     0.00001796292 * Math.cos( 0.51761494342 +       74.94165726170*t);
      uranus_y_0+=     0.00002240648 * Math.cos( 0.47739127862 +      181.75834193920*t);
      uranus_y_0+=     0.00001924499 * Math.cos( 2.64284880495 +      206.18554843720*t);
      uranus_y_0+=     0.00001626134 * Math.cos( 3.70023731184 +      191.20769491020*t);
      uranus_y_0+=     0.00001860824 * Math.cos( 0.10445996392 +       42.58645376270*t);
      uranus_y_0+=     0.00002177437 * Math.cos( 2.80437422101 +      479.28838891550*t);
      uranus_y_0+=     0.00001896184 * Math.cos( 4.26975898003 +       14.97785352700*t);
      uranus_y_0+=     0.00002045249 * Math.cos( 5.17400788104 +      835.03713448730*t);
      uranus_y_0+=     0.00001887812 * Math.cos( 2.75000237791 +      154.01661525950*t);
      uranus_y_0+=     0.00001794754 * Math.cos( 0.16290844853 +      227.31374111850*t);
      uranus_y_0+=     0.00001347410 * Math.cos( 3.89237011696 +      288.08069400530*t);
      uranus_y_0+=     0.00001572826 * Math.cos( 5.93367812903 +      219.89137757700*t);
      uranus_y_0+=     0.00001424804 * Math.cos( 5.10004758033 +       92.94084583200*t);
      uranus_y_0+=     0.00001267766 * Math.cos( 0.92771324396 +      404.50679034820*t);
      uranus_y_0+=     0.00001588897 * Math.cos( 4.15115668974 +       39.35687591520*t);
      uranus_y_0+=     0.00001269786 * Math.cos( 1.09685727529 +      142.44965013380*t);
      uranus_y_0+=     0.00001291065 * Math.cos( 5.67425699047 +       68.84370773410*t);
      uranus_y_0+=     0.00001436850 * Math.cos( 5.44312198350 +      522.57741809380*t);
      uranus_y_0+=     0.00001405564 * Math.cos( 2.04677392527 +      536.80451209540*t);
      uranus_y_0+=     0.00001416917 * Math.cos( 0.72597245494 +      235.39049596580*t);
      uranus_y_0+=     0.00001165315 * Math.cos( 0.51071041452 +       81.89514556810*t);
      uranus_y_0+=     0.00001035262 * Math.cos( 1.20639876458 +        5.41662597140*t);
      uranus_y_0+=     0.00001009454 * Math.cos( 0.45375065997 +       74.03083904190*t);
      uranus_y_0+=     0.00001220696 * Math.cos( 1.84988185963 +      211.81462272970*t);
      uranus_y_0+=     0.00000997784 * Math.cos( 4.22640788890 +       75.53235809270*t);
      uranus_y_0+=     0.00001222886 * Math.cos( 2.27306099902 +      187.69623277240*t);
      uranus_y_0+=     0.00001336792 * Math.cos( 3.74888989756 +      380.12776796000*t);
      uranus_y_0+=     0.00001151803 * Math.cos( 0.46579056125 +      128.95626931510*t);
      uranus_y_0+=     0.00001149114 * Math.cos( 0.85101218281 +      296.15744885260*t);
      uranus_y_0+=     0.00001163762 * Math.cos( 5.51157783762 +      230.56457082540*t);
      uranus_y_0+=     0.00001192292 * Math.cos( 0.68084398426 +       99.16062095550*t);
      uranus_y_0+=     0.00001151286 * Math.cos( 4.01147735438 +       67.66805156650*t);
      uranus_y_0+=     0.00001189801 * Math.cos( 4.01778306134 +       50.40257617910*t);
      uranus_y_0+=     0.00001015998 * Math.cos( 1.00290501307 +       35.42472265210*t);
      uranus_y_0+=     0.00000923365 * Math.cos( 5.76874685766 +       54.17467074780*t);
      uranus_y_0+=     0.00000855559 * Math.cos( 4.49004561030 +       68.18931642830*t);
      uranus_y_0+=     0.00000911338 * Math.cos( 0.12254293382 +      149.45132255000*t);
      uranus_y_0+=     0.00001174953 * Math.cos( 0.45683512473 +      110.20632121940*t);
      uranus_y_0+=     0.00000856856 * Math.cos( 6.21758865027 +       89.75945209430*t);
      uranus_y_0+=     0.00001051606 * Math.cos( 3.96907647535 +       14.01464568050*t);
      uranus_y_0+=     0.00000835264 * Math.cos( 5.34437105960 +       59.80374504030*t);
      uranus_y_0+=     0.00000909788 * Math.cos( 3.15839878322 +      149.67507171920*t);
      uranus_y_0+=     0.00000742857 * Math.cos( 2.49216613688 +      277.03499374140*t);
      uranus_y_0+=     0.00000973381 * Math.cos( 0.64028748776 +      218.40690486870*t);
      uranus_y_0+=     0.00000952790 * Math.cos( 1.24773830053 +      106.97674337190*t);
      uranus_y_0+=     0.00000891414 * Math.cos( 1.82007872482 +       23.57587323610*t);
      uranus_y_0+=     0.00000896763 * Math.cos( 0.51927845768 +      200.76892246580*t);
      uranus_y_0+=     0.00000662758 * Math.cos( 0.25796780548 +       81.37388070630*t);
      uranus_y_0+=     0.00000863768 * Math.cos( 3.46041862039 +      162.09337010680*t);
      uranus_y_0+=     0.00000623013 * Math.cos( 2.99649402595 +       51.20572533120*t);
      uranus_y_0+=     0.00000597805 * Math.cos( 1.07147770615 +      134.58534360760*t);
      uranus_y_0+=     0.00000766040 * Math.cos( 0.89351020566 +       68.56182344380*t);
      uranus_y_0+=     0.00000626173 * Math.cos( 0.14763136288 +       24.37902238820*t);
      uranus_y_0+=     0.00000661316 * Math.cos( 3.91236554284 +        8.07675484730*t);
      uranus_y_0+=     0.00000746242 * Math.cos( 2.79717552793 +      760.25553592000*t);
      uranus_y_0+=     0.00000643424 * Math.cos( 5.98383236425 +       88.79624424780*t);
      uranus_y_0+=     0.00000703154 * Math.cos( 1.49852097954 +      203.73786788240*t);
      uranus_y_0+=     0.00000581277 * Math.cos( 0.83588836575 +       28.57180808220*t);
      uranus_y_0+=     0.00000528413 * Math.cos( 0.71044436153 +      146.38180339690*t);
      uranus_y_0+=     0.00000695636 * Math.cos( 4.49767435966 +      617.80588578620*t);
      uranus_y_0+=     0.00000604018 * Math.cos( 2.75780757245 +      195.13984817330*t);
      uranus_y_0+=     0.00000536175 * Math.cos( 1.52084605210 +      116.42609634290*t);
      uranus_y_0+=     0.00000560350 * Math.cos( 1.79729642400 +       69.36497259590*t);
      uranus_y_0+=     0.00000485627 * Math.cos( 5.77277696629 +      415.55249061210*t);
      uranus_y_0+=     0.00000587456 * Math.cos( 2.33741613601 +      152.01087768940*t);
      uranus_y_0+=     0.00000666586 * Math.cos( 4.63314190172 +        6.21977512350*t);
      uranus_y_0+=     0.00000505972 * Math.cos( 0.95984060933 +      157.63995198190*t);
      uranus_y_0+=     0.00000550782 * Math.cos( 5.85625308842 +      260.99335863140*t);
      uranus_y_0+=     0.00000588886 * Math.cos( 4.62064969642 +      258.02441321480*t);
      uranus_y_0+=     0.00000537829 * Math.cos( 5.54228018001 +      209.36694217490*t);
      uranus_y_0+=     0.00000445581 * Math.cos( 5.33271706288 +      329.72519178090*t);
      uranus_y_0+=     0.00000618901 * Math.cos( 4.52549231118 +      125.98732389850*t);
      uranus_y_0+=     0.00000513508 * Math.cos( 0.74576777970 +      351.81659230870*t);
      uranus_y_0+=     0.00000449585 * Math.cos( 2.60457386268 +      543.02428721890*t);
      uranus_y_0+=     0.00000488079 * Math.cos( 5.04403350813 +       73.40900044360*t);
      uranus_y_0+=     0.00000563065 * Math.cos( 3.08986059602 +      155.78297225810*t);
      uranus_y_0+=     0.00000435632 * Math.cos( 6.01152475622 +     1589.07289528380*t);
      uranus_y_0+=     0.00000537029 * Math.cos( 3.75711795413 +       81.00137369080*t);
      uranus_y_0+=     0.00000435630 * Math.cos( 2.19413803718 +      372.42352012820*t);
      uranus_y_0+=     0.00000472431 * Math.cos( 1.72063683793 +      180.27386923090*t);
      uranus_y_0+=     0.00000418634 * Math.cos( 0.40340567628 +       95.38852638680*t);
      uranus_y_0+=     0.00000514049 * Math.cos( 3.83742451002 +      115.88357962170*t);
      uranus_y_0+=     0.00000419613 * Math.cos( 6.21605224514 +       41.64449777560*t);
      uranus_y_0+=     0.00000390364 * Math.cos( 4.39316702257 +      152.74459087230*t);
      uranus_y_0+=     0.00000354100 * Math.cos( 5.26264151031 +       46.20979048510*t);
      uranus_y_0+=     0.00000369010 * Math.cos( 4.11078638826 +      144.14657116320*t);
      uranus_y_0+=     0.00000374623 * Math.cos( 1.90215093451 +       73.18525127440*t);
      uranus_y_0+=     0.00000426261 * Math.cos( 0.89836299897 +      141.48644228730*t);
      uranus_y_0+=     0.00000381449 * Math.cos( 3.63961245738 +      114.13847448250*t);
      uranus_y_0+=     0.00000317869 * Math.cos( 4.93937891025 +       33.13710079170*t);
      uranus_y_0+=     0.00000325976 * Math.cos( 2.61924421042 +      228.27694896500*t);
      uranus_y_0+=     0.00000306708 * Math.cos( 2.91911612770 +      103.09277421860*t);
      uranus_y_0+=     0.00000354526 * Math.cos( 4.66410291093 +      214.78356814630*t);
      uranus_y_0+=     0.00000405556 * Math.cos( 2.67339819968 +      490.33408917940*t);
      uranus_y_0+=     0.00000405067 * Math.cos( 0.76651664121 +      255.05546779820*t);
      uranus_y_0+=     0.00000324278 * Math.cos( 4.97703425119 +        7.42236354150*t);
      uranus_y_0+=     0.00000313668 * Math.cos( 1.39418130536 +      419.48464387520*t);
      uranus_y_0+=     0.00000316354 * Math.cos( 3.43209926093 +       30.71067209630*t);
      uranus_y_0+=     0.00000287093 * Math.cos( 5.24491427364 +       45.57665103870*t);
      uranus_y_0+=     0.00000277004 * Math.cos( 4.21620590877 +        6.59228213900*t);
      uranus_y_0+=     0.00000318464 * Math.cos( 0.45911675628 +      120.35824960600*t);
      uranus_y_0+=     0.00000311815 * Math.cos( 0.79978809612 +      147.11551657980*t);
      uranus_y_0+=     0.00000337472 * Math.cos( 3.60594773618 +      150.52640498110*t);
      uranus_y_0+=     0.00000255714 * Math.cos( 6.18037150203 +       19.12245511120*t);
      uranus_y_0+=     0.00000246583 * Math.cos( 1.17774433989 +      554.06998748280*t);
      uranus_y_0+=     0.00000307606 * Math.cos( 4.06279403542 +      639.89728631400*t);
      uranus_y_0+=     0.00000252403 * Math.cos( 5.01154358916 +      150.08446199640*t);
      uranus_y_0+=     0.00000230070 * Math.cos( 5.35619295971 +       60.76695288680*t);
      uranus_y_0+=     0.00000278047 * Math.cos( 5.88865683969 +       29.20494752860*t);
      uranus_y_0+=     0.00000306257 * Math.cos( 0.18368210739 +     6283.07584999140*t);
      uranus_y_0+=     0.00000302295 * Math.cos( 0.43076728879 +      984.60033162190*t);
      uranus_y_0+=     0.00000265211 * Math.cos( 1.11226453547 +       28.31117565130*t);
      uranus_y_0+=     0.00000227327 * Math.cos( 3.78561264808 +      120.99138905240*t);
      uranus_y_0+=     0.00000198785 * Math.cos( 3.18797196563 +       69.67378913660*t);
      uranus_y_0+=     0.00000222192 * Math.cos( 3.44393515493 +       47.69426319340*t);
      uranus_y_0+=     0.00000219949 * Math.cos( 5.18094249145 +       44.07092647100*t);
      uranus_y_0+=     0.00000210545 * Math.cos( 3.35124491126 +        0.52126486180*t);
      uranus_y_0+=     0.00000227699 * Math.cos( 1.88879274658 +      216.92243216040*t);
      uranus_y_0+=     0.00000257536 * Math.cos( 0.30399822270 +     1289.94650101460*t);
      uranus_y_0+=     0.00000231681 * Math.cos( 2.78093325899 +       46.47042291600*t);
      uranus_y_0+=     0.00000239720 * Math.cos( 6.19793297710 +      756.32338265690*t);
      uranus_y_0+=     0.00000214437 * Math.cos( 1.18016591525 +      189.18070548070*t);
      uranus_y_0+=     0.00000233297 * Math.cos( 2.18609372572 +      339.28641933650*t);
      uranus_y_0+=     0.00000210930 * Math.cos( 1.09786361796 +      316.39186965660*t);
      uranus_y_0+=     0.00000234130 * Math.cos( 3.14530755107 +      342.25536475310*t);
      uranus_y_0+=     0.00000175836 * Math.cos( 1.53408491826 +       57.25549074900*t);
      uranus_y_0+=     0.00000167756 * Math.cos( 5.59398995995 +       30.05628079050*t);
      uranus_y_0+=     0.00000216757 * Math.cos( 0.90936155593 +      135.54855145410*t);
      uranus_y_0+=     0.00000173749 * Math.cos( 4.28628512648 +      681.54178408960*t);
      uranus_y_0+=     0.00000164586 * Math.cos( 0.70747217893 +      468.24268865160*t);
      uranus_y_0+=     0.00000203490 * Math.cos( 5.82940017414 +      148.59998928810*t);
      uranus_y_0+=     0.00000163450 * Math.cos( 1.53200906891 +       79.88940799800*t);
      uranus_y_0+=     0.00000179581 * Math.cos( 5.36487860827 +      103.35340664950*t);
      uranus_y_0+=     0.00000159175 * Math.cos( 3.51044775078 +       17.52610781830*t);
      uranus_y_0+=     0.00000165292 * Math.cos( 5.36941198819 +      154.97982310600*t);
      uranus_y_0+=     0.00000192957 * Math.cos( 5.12177898736 +        0.96320784650*t);
      uranus_y_0+=     0.00000185802 * Math.cos( 3.99560320824 +       73.88782669000*t);
      uranus_y_0+=     0.00000185802 * Math.cos( 0.68379922776 +       75.67537044460*t);
      uranus_y_0+=     0.00000163127 * Math.cos( 0.33878389027 +      264.50482076920*t);
      uranus_y_0+=     0.00000187130 * Math.cos( 4.63207698177 +      149.04193227280*t);
      uranus_y_0+=     0.00000185821 * Math.cos( 5.76008843913 +       76.15419669100*t);
      uranus_y_0+=     0.00000175560 * Math.cos( 4.41849512958 +      333.65734504400*t);
      uranus_y_0+=     0.00000202867 * Math.cos( 0.92934842891 +      291.70403072770*t);
      uranus_y_0+=     0.00000157912 * Math.cos( 4.13655140282 +       82.20396210880*t);
      uranus_y_0+=     0.00000178492 * Math.cos( 0.39921147736 +      685.47393735270*t);
      uranus_y_0+=     0.00000137687 * Math.cos( 3.65255922607 +      448.68959140380*t);
      uranus_y_0+=     0.00000152639 * Math.cos( 2.03301679425 +      233.90602325750*t);
      uranus_y_0+=     0.00000154719 * Math.cos( 4.66548925160 +      294.67297614430*t);
      uranus_y_0+=     0.00000137993 * Math.cos( 0.49895867902 +       16.67477455640*t);
      uranus_y_0+=     0.00000161861 * Math.cos( 2.54166020189 +      105.49227066360*t);
      uranus_y_0+=     0.00000130404 * Math.cos( 4.56696904208 +       76.47851959670*t);
      uranus_y_0+=     0.00000128155 * Math.cos( 2.45134447197 +      156.15547927360*t);
      uranus_y_0+=     0.00000146437 * Math.cos( 3.06416525256 +      334.29048449040*t);
      uranus_y_0+=     0.00000176732 * Math.cos( 1.60845376428 +    10213.28554621100*t);
      uranus_y_0+=     0.00000157530 * Math.cos( 1.02260224406 +      347.88443904560*t);
      uranus_y_0+=     0.00000120105 * Math.cos( 5.04807417968 +      130.44074202340*t);
      uranus_y_0+=     0.00000127914 * Math.cos( 5.91612723274 +       61.44827644300*t);
      uranus_y_0+=     0.00000141971 * Math.cos( 4.67692245942 +      173.94221952280*t);
      uranus_y_0+=     0.00000116798 * Math.cos( 2.79975011606 +      692.58748435350*t);
      uranus_y_0+=     0.00000145866 * Math.cos( 4.72508344563 +       24.11838995730*t);
      uranus_y_0+=     0.00000140467 * Math.cos( 4.49862691968 +      286.59622129700*t);
      uranus_y_0+=     0.00000121897 * Math.cos( 4.89621303002 +       79.44746501330*t);
      uranus_y_0+=     0.00000113904 * Math.cos( 5.19950219884 +       13.33332212430*t);
      uranus_y_0+=     0.00000143684 * Math.cos( 4.38416731946 +      628.85158605010*t);
      uranus_y_0+=     0.00000128986 * Math.cos( 3.45591214307 +      254.94359321360*t);
      uranus_y_0+=     0.00000135174 * Math.cos( 1.15418631167 +      171.65459766240*t);
      uranus_y_0+=     0.00000125769 * Math.cos( 3.85907526779 +       98.35747180340*t);
      uranus_y_0+=     0.00000105739 * Math.cos( 5.13563496088 +       66.91729204110*t);
      uranus_y_0+=     0.00000107892 * Math.cos( 0.10090598897 +      375.39246554480*t);
      uranus_y_0+=     0.00000128792 * Math.cos( 1.53820246543 +      155.50108796780*t);
      uranus_y_0+=     0.00000103751 * Math.cos( 0.09858727182 +       54.33472944220*t);
      uranus_y_0+=     0.00000136546 * Math.cos( 4.44396318920 +      909.81873305460*t);
      uranus_y_0+=     0.00000114357 * Math.cos( 4.80183924958 +      273.10284047830*t);
      uranus_y_0+=     0.00000101658 * Math.cos( 0.35890468314 +      362.86229257260*t);
      uranus_y_0+=     0.00000109802 * Math.cos( 5.86019231369 +      143.62530630140*t);
      uranus_y_0+=     0.00000106158 * Math.cos( 2.64028524201 +      302.09533968580*t);
      uranus_y_0+=     0.00000112226 * Math.cos( 3.46253936917 +       92.30770638560*t);
      uranus_y_0+=     0.00000113609 * Math.cos( 3.99798751814 +      632.78373931320*t);
      uranus_y_0+=     0.00000113987 * Math.cos( 2.05059638924 +      253.57099508990*t);
      uranus_y_0+=     0.00000109155 * Math.cos( 3.69281386772 +       55.65914345610*t);
      uranus_y_0+=     0.00000113624 * Math.cos( 1.22774403773 +      604.47256366190*t);
      uranus_y_0+=     0.00000110540 * Math.cos( 2.03204732442 +       19.64371997300*t);
      uranus_y_0+=     0.00000104928 * Math.cos( 4.71621888596 +      433.71173787680*t);
      uranus_y_0+=     0.00000116258 * Math.cos( 4.19923354698 +     1215.16490244730*t);
      uranus_y_0+=     0.00000112324 * Math.cos( 5.22657359082 +      228.79821382680*t);
      uranus_y_0+=     0.00000106862 * Math.cos( 1.56894230537 +       81.68269724700*t);
      uranus_y_0+=     0.00000105689 * Math.cos( 5.90750871349 +      100.38446123290*t);
      uranus_y_0+=     0.00000107519 * Math.cos( 4.73121020405 +     1162.47470440780*t);
      uranus_y_0+=     0.00000104152 * Math.cos( 3.12500840636 +      210.33015002140*t);
      uranus_y_0+=     0.00000105110 * Math.cos( 1.09488557735 +      328.35259365720*t);

      let uranus_y_1=0.0;
      uranus_y_1+=     0.02157896385 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_y_1+=     0.00739227349 * Math.cos( 4.43963890935 +      149.56319713460*t);
      uranus_y_1+=     0.00238545685 * Math.cos( 3.76882493145 +       73.29712585900*t);
      uranus_y_1+=     0.00229396424 * Math.cos( 0.91090183978 +       76.26607127560*t);
      uranus_y_1+=     0.00110137111 * Math.cos( 4.00844441616 +       11.04570026390*t);
      uranus_y_1+=     0.00094979054 * Math.cos( 5.07141537066 +       63.73589830340*t);
      uranus_y_1+=     0.00081474163 * Math.cos( 5.92275367106 +       85.82729883120*t);
      uranus_y_1+=     0.00045457174 * Math.cos( 0.73292241207 +      138.51749687070*t);
      uranus_y_1+=     0.00051366974 * Math.cos( 0.61844114994 +      224.34479570190*t);
      uranus_y_1+=     0.00038296005 * Math.cos( 5.01873578671 +       70.84944530420*t);
      uranus_y_1+=     0.00036146116 * Math.cos( 5.94859452787 +       78.71375183040*t);
      uranus_y_1+=     0.00032420558 * Math.cos( 4.32617271732 +       74.78159856730*t);
      uranus_y_1+=     0.00021673269 * Math.cos( 3.36607263522 +      151.04766984290*t);
      uranus_y_1+=     0.00019425087 * Math.cos( 6.01842187783 +       77.75054398390*t);
      uranus_y_1+=     0.00017393206 * Math.cos( 4.96098895488 +       71.81265315070*t);
      uranus_y_1+=     0.00014991169 * Math.cos( 3.97176856758 +        3.93215326310*t);
      uranus_y_1+=     0.00007732367 * Math.cos( 0.04256630122 +       71.60020482960*t);
      uranus_y_1+=     0.00007438492 * Math.cos( 4.63165436478 +       77.96299230500*t);
      uranus_y_1+=     0.00006979238 * Math.cos( 0.83723520791 +      145.63104387150*t);
      uranus_y_1+=     0.00007321559 * Math.cos( 0.66348425538 +        2.96894541660*t);
      uranus_y_1+=     0.00007595636 * Math.cos( 1.19807643487 +      148.07872442630*t);
      uranus_y_1+=     0.00004376824 * Math.cos( 2.17182724016 +      160.60889739850*t);
      uranus_y_1+=     0.00003962568 * Math.cos( 3.18042711824 +       65.22037101170*t);
      uranus_y_1+=     0.00004117202 * Math.cos( 6.19931612790 +       22.09140052780*t);
      uranus_y_1+=     0.00002830313 * Math.cos( 3.34365222278 +      213.29909543800*t);
      uranus_y_1+=     0.00002690065 * Math.cos( 1.78946471198 +        9.56122755560*t);
      uranus_y_1+=     0.00002628159 * Math.cos( 2.97459067399 +       12.53017297220*t);
      uranus_y_1+=     0.00003174617 * Math.cos( 3.08131638838 +      299.12639426920*t);
      uranus_y_1+=     0.00002227510 * Math.cos( 4.89407437055 +       87.31177153950*t);
      uranus_y_1+=     0.00002821206 * Math.cos( 1.83130010947 +       84.34282612290*t);
      uranus_y_1+=     0.00002510693 * Math.cos( 1.27166561854 +       18.15924726470*t);
      uranus_y_1+=     0.00002224655 * Math.cos( 3.21541108798 +       72.33391801250*t);
      uranus_y_1+=     0.00001929662 * Math.cos( 4.68383962079 +       52.69019803950*t);
      uranus_y_1+=     0.00001707606 * Math.cos( 5.60415260609 +      127.47179660680*t);
      uranus_y_1+=     0.00001620819 * Math.cos( 2.18676505386 +      153.49535039770*t);
      uranus_y_1+=     0.00001926926 * Math.cos( 0.82821252139 +       39.61750834610*t);
      uranus_y_1+=     0.00001555611 * Math.cos( 2.56681954823 +       73.81839072080*t);
      uranus_y_1+=     0.00001595703 * Math.cos( 4.79558057860 +       79.23501669220*t);
      uranus_y_1+=     0.00001476550 * Math.cos( 2.10111459539 +       75.74480641380*t);
      uranus_y_1+=     0.00001531355 * Math.cos( 2.14701519407 +      152.53214255120*t);
      uranus_y_1+=     0.00001744564 * Math.cos( 1.67897185084 +       77.22927912210*t);
      uranus_y_1+=     0.00001713945 * Math.cos( 1.82334975258 +      222.86032299360*t);
      uranus_y_1+=     0.00001705184 * Math.cos( 5.82532917611 +      225.82926841020*t);
      uranus_y_1+=     0.00001739019 * Math.cos( 3.82452086292 +      146.59425171800*t);
      uranus_y_1+=     0.00001291753 * Math.cos( 6.19666243545 +       70.32818044240*t);
      uranus_y_1+=     0.00001458526 * Math.cos( 5.10147126404 +        3.18139373770*t);
      uranus_y_1+=     0.00001179966 * Math.cos( 3.56807126055 +      220.41264243880*t);
      uranus_y_1+=     0.00001234914 * Math.cos( 5.69239889831 +        4.45341812490*t);
      uranus_y_1+=     0.00001075108 * Math.cos( 1.76286452034 +       56.62235130260*t);
      uranus_y_1+=     0.00001035661 * Math.cos( 6.12642568708 +       62.25142559510*t);
      uranus_y_1+=     0.00000978675 * Math.cos( 5.23202231955 +       74.89347315190*t);
      uranus_y_1+=     0.00000977123 * Math.cos( 5.73086540533 +       74.66972398270*t);
      uranus_y_1+=     0.00001114523 * Math.cos( 3.41304662369 +      131.40394986990*t);
      uranus_y_1+=     0.00000888937 * Math.cos( 2.70132350527 +      426.59819087600*t);
      uranus_y_1+=     0.00001050191 * Math.cos( 3.84176879347 +      109.94568878850*t);
      uranus_y_1+=     0.00000764556 * Math.cos( 1.17341120063 +        1.48447270830*t);
      uranus_y_1+=     0.00000746231 * Math.cos( 3.21375560117 +       92.94084583200*t);
      uranus_y_1+=     0.00000752227 * Math.cos( 4.36686229005 +      206.18554843720*t);
      uranus_y_1+=     0.00000649263 * Math.cos( 4.91621635684 +       80.19822453870*t);
      uranus_y_1+=     0.00000762421 * Math.cos( 1.67864314047 +        7.11354700080*t);
      uranus_y_1+=     0.00000605052 * Math.cos( 4.82003168096 +     1059.38193018920*t);
      uranus_y_1+=     0.00000665473 * Math.cos( 1.92732409009 +       96.87299909510*t);
      uranus_y_1+=     0.00000576200 * Math.cos( 0.85782625562 +      522.57741809380*t);
      uranus_y_1+=     0.00000514504 * Math.cos( 2.01976952661 +        2.44768055480*t);
      uranus_y_1+=     0.00000562291 * Math.cos( 0.34610225486 +      536.80451209540*t);
      uranus_y_1+=     0.00000490123 * Math.cos( 1.93462283883 +      137.03302416240*t);
      uranus_y_1+=     0.00000477490 * Math.cos( 5.86979757700 +       41.10198105440*t);
      uranus_y_1+=     0.00000413484 * Math.cos( 2.21776453713 +       66.70484372000*t);
      uranus_y_1+=     0.00000408932 * Math.cos( 5.05029212723 +       81.89514556810*t);
      uranus_y_1+=     0.00000430008 * Math.cos( 5.76371058355 +       67.66805156650*t);
      uranus_y_1+=     0.00000390965 * Math.cos( 0.01692722229 +       14.97785352700*t);
      uranus_y_1+=     0.00000347208 * Math.cos( 2.52660480727 +      146.38180339690*t);
      uranus_y_1+=     0.00000343163 * Math.cos( 2.84832361417 +      142.44965013380*t);
      uranus_y_1+=     0.00000288668 * Math.cos( 2.84411301863 +        5.41662597140*t);
      uranus_y_1+=     0.00000326058 * Math.cos( 4.27079067798 +      112.91463420510*t);
      uranus_y_1+=     0.00000283888 * Math.cos( 2.51516272259 +       82.85835341460*t);
      uranus_y_1+=     0.00000295927 * Math.cos( 5.21796998105 +      145.10977900970*t);
      uranus_y_1+=     0.00000254703 * Math.cos( 4.68299688590 +      235.39049596580*t);
      uranus_y_1+=     0.00000262038 * Math.cos( 2.33202621667 +      265.98929347750*t);
      uranus_y_1+=     0.00000245126 * Math.cos( 3.09493330266 +      202.25339517410*t);
      uranus_y_1+=     0.00000281688 * Math.cos( 2.62609779716 +       33.67961751290*t);
      uranus_y_1+=     0.00000246615 * Math.cos( 3.74974069088 +      159.12442469020*t);
      uranus_y_1+=     0.00000238731 * Math.cos( 4.48116112932 +      195.13984817330*t);
      uranus_y_1+=     0.00000235460 * Math.cos( 2.06524150362 +       20.60692781950*t);
      uranus_y_1+=     0.00000217418 * Math.cos( 2.68089080319 +      152.74459087230*t);
      uranus_y_1+=     0.00000212386 * Math.cos( 0.50246377589 +      191.20769491020*t);
      uranus_y_1+=     0.00000233899 * Math.cos( 5.10353028418 +      108.46121608020*t);
      uranus_y_1+=     0.00000207801 * Math.cos( 3.08224092011 +      140.00196957900*t);
      uranus_y_1+=     0.00000209576 * Math.cos( 0.56985322873 +       36.64856292950*t);
      uranus_y_1+=     0.00000212509 * Math.cos( 3.85248583314 +      209.36694217490*t);
      uranus_y_1+=     0.00000192273 * Math.cos( 5.17224479052 +       23.57587323610*t);
      uranus_y_1+=     0.00000228062 * Math.cos( 4.16741377080 +      297.64192156090*t);
      uranus_y_1+=     0.00000170887 * Math.cos( 2.87499673493 +      128.95626931510*t);
      uranus_y_1+=     0.00000166214 * Math.cos( 4.46057308613 +        5.93789083320*t);
      uranus_y_1+=     0.00000153690 * Math.cos( 5.62788233695 +      288.08069400530*t);
      uranus_y_1+=     0.00000153433 * Math.cos( 1.12899903219 +      162.09337010680*t);
      uranus_y_1+=     0.00000192082 * Math.cos( 5.54389138204 +      373.90799283650*t);
      uranus_y_1+=     0.00000154183 * Math.cos( 1.68184245790 +       14.01464568050*t);
      uranus_y_1+=     0.00000151315 * Math.cos( 2.23944413846 +      120.35824960600*t);
      uranus_y_1+=     0.00000143602 * Math.cos( 4.22422388284 +      211.81462272970*t);
      uranus_y_1+=     0.00000140781 * Math.cos( 3.78365682991 +       29.20494752860*t);
      uranus_y_1+=     0.00000140280 * Math.cos( 3.58846256331 +       80.71948940050*t);
      uranus_y_1+=     0.00000132953 * Math.cos( 6.02568481572 +       69.36497259590*t);
      uranus_y_1+=     0.00000134104 * Math.cos( 5.15983441194 +       39.35687591520*t);
      uranus_y_1+=     0.00000148048 * Math.cos( 1.44770358695 +      186.21176006410*t);
      uranus_y_1+=     0.00000132976 * Math.cos( 5.88157760376 +       68.56182344380*t);
      uranus_y_1+=     0.00000141943 * Math.cos( 3.15577853409 +      114.39910691340*t);
      uranus_y_1+=     0.00000132366 * Math.cos( 2.36046311842 +       89.75945209430*t);
      uranus_y_1+=     0.00000116164 * Math.cos( 1.93633920538 +       33.13710079170*t);
      uranus_y_1+=     0.00000121388 * Math.cos( 2.55708768907 +      305.34616939270*t);
      uranus_y_1+=     0.00000120180 * Math.cos( 1.31156651928 +       50.40257617910*t);
      uranus_y_1+=     0.00000109658 * Math.cos( 3.65858083856 +       88.79624424780*t);
      uranus_y_1+=     0.00000121042 * Math.cos( 0.94635099828 +      154.01661525950*t);
      uranus_y_1+=     0.00000129679 * Math.cos( 5.11195868446 +      277.03499374140*t);
      uranus_y_1+=     0.00000103287 * Math.cos( 2.14115463817 +      144.14657116320*t);
      uranus_y_1+=     0.00000132665 * Math.cos( 0.92310657218 +       45.57665103870*t);
      uranus_y_1+=     0.00000133005 * Math.cos( 1.50572985923 +       54.17467074780*t);
      uranus_y_1+=     0.00000116279 * Math.cos( 4.59183976429 +      227.31374111850*t);
      uranus_y_1+=     0.00000122911 * Math.cos( 2.00108270900 +      300.61086697750*t);
      uranus_y_1+=     0.00000113171 * Math.cos( 2.92188560176 +       41.64449777560*t);
      uranus_y_1+=     0.00000102740 * Math.cos( 3.77682647354 +      152.01087768940*t);
      uranus_y_1=uranus_y_1 * t;

      let uranus_y_2=0.0;
      uranus_y_2+=     0.00034812647 * Math.cos( 3.14159265359 +        0.00000000000*t);
      uranus_y_2+=     0.00016589194 * Math.cos( 2.29556740620 +       74.78159856730*t);
      uranus_y_2+=     0.00010905147 * Math.cos( 1.45737963668 +      149.56319713460*t);
      uranus_y_2+=     0.00007484633 * Math.cos( 2.27968076918 +       11.04570026390*t);
      uranus_y_2+=     0.00007964298 * Math.cos( 0.97230247087 +       63.73589830340*t);
      uranus_y_2+=     0.00005307100 * Math.cos( 3.20519221878 +       70.84944530420*t);
      uranus_y_2+=     0.00005018595 * Math.cos( 1.47518527303 +       78.71375183040*t);
      uranus_y_2+=     0.00006713255 * Math.cos( 3.74148881189 +       85.82729883120*t);
      uranus_y_2+=     0.00005265170 * Math.cos( 0.54901216905 +       73.29712585900*t);
      uranus_y_2+=     0.00004864822 * Math.cos( 4.11367426823 +       76.26607127560*t);
      uranus_y_2+=     0.00002995853 * Math.cos( 2.49432193549 +      138.51749687070*t);
      uranus_y_2+=     0.00002519021 * Math.cos( 1.78896824345 +       71.60020482960*t);
      uranus_y_2+=     0.00002418371 * Math.cos( 2.88675006488 +       77.96299230500*t);
      uranus_y_2+=     0.00002185856 * Math.cos( 5.58862614977 +        3.93215326310*t);
      uranus_y_2+=     0.00001035578 * Math.cos( 5.44752448275 +      145.63104387150*t);
      uranus_y_2+=     0.00001044459 * Math.cos( 4.27972239360 +      224.34479570190*t);
      uranus_y_2+=     0.00000659180 * Math.cos( 5.73048296712 +       18.15924726470*t);
      uranus_y_2+=     0.00000496445 * Math.cos( 3.71294537420 +       22.09140052780*t);
      uranus_y_2+=     0.00000503264 * Math.cos( 0.65556547194 +      151.04766984290*t);
      uranus_y_2+=     0.00000477875 * Math.cos( 1.62059307105 +       72.33391801250*t);
      uranus_y_2+=     0.00000484216 * Math.cos( 3.45190804780 +        3.18139373770*t);
      uranus_y_2+=     0.00000381403 * Math.cos( 3.62830479384 +       77.75054398390*t);
      uranus_y_2+=     0.00000403003 * Math.cos( 6.27429134777 +      160.60889739850*t);
      uranus_y_2+=     0.00000333059 * Math.cos( 0.97920205195 +       71.81265315070*t);
      uranus_y_2+=     0.00000384754 * Math.cos( 3.16159208089 +       77.22927912210*t);
      uranus_y_2+=     0.00000336233 * Math.cos( 4.76282903544 +       65.22037101170*t);
      uranus_y_2+=     0.00000292404 * Math.cos( 3.58367735696 +       56.62235130260*t);
      uranus_y_2+=     0.00000289620 * Math.cos( 5.24475224875 +      131.40394986990*t);
      uranus_y_2+=     0.00000249990 * Math.cos( 1.37715629750 +      127.47179660680*t);
      uranus_y_2+=     0.00000220833 * Math.cos( 1.89936700362 +      220.41264243880*t);
      uranus_y_2+=     0.00000301291 * Math.cos( 0.20539719662 +       84.34282612290*t);
      uranus_y_2+=     0.00000213294 * Math.cos( 0.42767033738 +       52.69019803950*t);
      uranus_y_2+=     0.00000206036 * Math.cos( 1.32796659605 +       92.94084583200*t);
      uranus_y_2+=     0.00000284114 * Math.cos( 4.23135833063 +      148.07872442630*t);
      uranus_y_2+=     0.00000211339 * Math.cos( 4.01130147721 +      153.49535039770*t);
      uranus_y_2+=     0.00000198865 * Math.cos( 1.14978553110 +       12.53017297220*t);
      uranus_y_2+=     0.00000204876 * Math.cos( 2.67799239908 +       87.31177153950*t);
      uranus_y_2+=     0.00000151532 * Math.cos( 6.09078229943 +      206.18554843720*t);
      uranus_y_2+=     0.00000142723 * Math.cos( 0.10949652735 +        9.56122755560*t);
      uranus_y_2+=     0.00000133164 * Math.cos( 5.80840699437 +      213.29909543800*t);
      uranus_y_2+=     0.00000117885 * Math.cos( 2.56668410237 +      522.57741809380*t);
      uranus_y_2+=     0.00000114052 * Math.cos( 4.92349496195 +      536.80451209540*t);
      uranus_y_2+=     0.00000105990 * Math.cos( 6.11096017627 +        7.11354700080*t);
      uranus_y_2+=     0.00000106322 * Math.cos( 4.32303636127 +      146.38180339690*t);
      uranus_y_2+=     0.00000100445 * Math.cos( 2.04935236166 +       62.25142559510*t);
      uranus_y_2=uranus_y_2 * t * t;

      let uranus_y_3=0.0;
      uranus_y_3+=     0.00001211380 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_y_3+=     0.00000668539 * Math.cos( 1.35719575778 +       70.84944530420*t);
      uranus_y_3+=     0.00000634232 * Math.cos( 3.31949833714 +       78.71375183040*t);
      uranus_y_3+=     0.00000580282 * Math.cos( 5.50249893160 +      149.56319713460*t);
      uranus_y_3+=     0.00000554688 * Math.cos( 3.11230721382 +       63.73589830340*t);
      uranus_y_3+=     0.00000455522 * Math.cos( 1.60057962784 +       85.82729883120*t);
      uranus_y_3+=     0.00000428309 * Math.cos( 2.52339539695 +       73.29712585900*t);
      uranus_y_3+=     0.00000410924 * Math.cos( 2.15904083831 +       76.26607127560*t);
      uranus_y_3+=     0.00000446887 * Math.cos( 3.43730189985 +       71.60020482960*t);
      uranus_y_3+=     0.00000422459 * Math.cos( 1.24206088889 +       77.96299230500*t);
      uranus_y_3+=     0.00000354240 * Math.cos( 0.67890104591 +       11.04570026390*t);
      uranus_y_3+=     0.00000246686 * Math.cos( 0.94534563236 +        3.93215326310*t);
      uranus_y_3+=     0.00000213878 * Math.cos( 5.65915292036 +       74.78159856730*t);
      uranus_y_3+=     0.00000132364 * Math.cos( 4.15026512788 +      138.51749687070*t);
      uranus_y_3+=     0.00000119450 * Math.cos( 3.90585537641 +       18.15924726470*t);
      uranus_y_3+=     0.00000120394 * Math.cos( 3.74665637710 +      145.63104387150*t);
      uranus_y_3=uranus_y_3 * t * t * t;

      return uranus_y_0+uranus_y_1+uranus_y_2+uranus_y_3;
   }

   static uranus_z(t){
      let uranus_z_0=0.0;
      uranus_z_0+=     0.25878127698 * Math.cos( 2.61861272578 +       74.78159856730*t);
      uranus_z_0+=     0.01774318778 * Math.cos( 3.14159265359 +        0.00000000000*t);
      uranus_z_0+=     0.00599316131 * Math.cos( 5.08119500585 +      149.56319713460*t);
      uranus_z_0+=     0.00190281890 * Math.cos( 1.61643841193 +       76.26607127560*t);
      uranus_z_0+=     0.00190881685 * Math.cos( 0.57869575952 +       73.29712585900*t);
      uranus_z_0+=     0.00084626761 * Math.cos( 2.26030150166 +        1.48447270830*t);
      uranus_z_0+=     0.00030734257 * Math.cos( 0.23571721555 +       63.73589830340*t);
      uranus_z_0+=     0.00020842052 * Math.cos( 1.26054208091 +      224.34479570190*t);
      uranus_z_0+=     0.00019734273 * Math.cos( 6.04314677688 +      148.07872442630*t);
      uranus_z_0+=     0.00012537530 * Math.cos( 5.17169051466 +       11.04570026390*t);
      uranus_z_0+=     0.00014582864 * Math.cos( 6.14852037212 +       71.81265315070*t);
      uranus_z_0+=     0.00010407529 * Math.cos( 3.65320417038 +      213.29909543800*t);
      uranus_z_0+=     0.00011261541 * Math.cos( 3.55973769686 +      529.69096509460*t);
      uranus_z_0+=     0.00008855669 * Math.cos( 4.03774505739 +      151.04766984290*t);
      uranus_z_0+=     0.00008239460 * Math.cos( 0.34225652715 +       77.75054398390*t);
      uranus_z_0+=     0.00007950169 * Math.cos( 0.72564903051 +       85.82729883120*t);
      uranus_z_0+=     0.00006867469 * Math.cos( 0.81417174224 +        2.96894541660*t);
      uranus_z_0+=     0.00005648720 * Math.cos( 3.45324719543 +      138.51749687070*t);
      uranus_z_0+=     0.00004581938 * Math.cos( 1.69668682344 +       38.13303563780*t);
      uranus_z_0+=     0.00002578399 * Math.cos( 5.19696447390 +      111.43016149680*t);
      uranus_z_0+=     0.00002964070 * Math.cos( 6.14338802239 +       35.16409022120*t);
      uranus_z_0+=     0.00001884104 * Math.cos( 2.61192472648 +       78.71375183040*t);
      uranus_z_0+=     0.00002330304 * Math.cos( 5.72640226150 +       70.84944530420*t);
      uranus_z_0+=     0.00001985215 * Math.cos( 0.76408839812 +       39.61750834610*t);
      uranus_z_0+=     0.00001743154 * Math.cos( 1.20586281789 +      146.59425171800*t);
      uranus_z_0+=     0.00002037011 * Math.cos( 0.95353587037 +       70.32818044240*t);
      uranus_z_0+=     0.00001508924 * Math.cos( 2.26195448553 +      222.86032299360*t);
      uranus_z_0+=     0.00001082736 * Math.cos( 2.62872874057 +      108.46121608020*t);
      uranus_z_0+=     0.00001051968 * Math.cos( 0.75560753840 +      109.94568878850*t);
      uranus_z_0+=     0.00000860142 * Math.cos( 3.72285572975 +      299.12639426920*t);
      uranus_z_0+=     0.00000816182 * Math.cos( 3.95303779460 +       52.69019803950*t);
      uranus_z_0+=     0.00000661249 * Math.cos( 3.83459160939 +       36.64856292950*t);
      uranus_z_0+=     0.00000712421 * Math.cos( 1.08343941878 +        3.93215326310*t);
      uranus_z_0+=     0.00000561959 * Math.cos( 1.87601204328 +      351.81659230870*t);
      uranus_z_0+=     0.00000618657 * Math.cos( 5.77033241076 +        4.45341812490*t);
      uranus_z_0+=     0.00000526378 * Math.cos( 3.88178280084 +      112.91463420510*t);
      uranus_z_0+=     0.00000624327 * Math.cos( 5.55998063360 +      202.25339517410*t);
      uranus_z_0+=     0.00000464130 * Math.cos( 0.20598822419 +      225.82926841020*t);
      uranus_z_0+=     0.00000448110 * Math.cos( 2.70547740286 +      145.10977900970*t);
      uranus_z_0+=     0.00000421562 * Math.cos( 3.66721349765 +      184.72728735580*t);
      uranus_z_0+=     0.00000458133 * Math.cos( 5.49113221489 +       79.23501669220*t);
      uranus_z_0+=     0.00000437386 * Math.cos( 1.24892718921 +       33.67961751290*t);
      uranus_z_0+=     0.00000393617 * Math.cos( 1.25018492386 +       62.25142559510*t);
      uranus_z_0+=     0.00000424721 * Math.cos( 2.73945218102 +      152.53214255120*t);
      uranus_z_0+=     0.00000465359 * Math.cos( 3.24015058631 +      127.47179660680*t);
      uranus_z_0+=     0.00000350450 * Math.cos( 2.57788261436 +       84.34282612290*t);
      uranus_z_0+=     0.00000346833 * Math.cos( 2.91261394620 +      426.59819087600*t);
      uranus_z_0+=     0.00000375747 * Math.cos( 3.20459646801 +      160.60889739850*t);
      uranus_z_0+=     0.00000313152 * Math.cos( 1.32117543131 +      145.63104387150*t);
      uranus_z_0+=     0.00000284456 * Math.cos( 1.70356835837 +       22.09140052780*t);
      uranus_z_0+=     0.00000265517 * Math.cos( 2.67172684401 +       74.66972398270*t);
      uranus_z_0+=     0.00000258948 * Math.cos( 4.12921582346 +       12.53017297220*t);
      uranus_z_0+=     0.00000274419 * Math.cos( 3.90646620441 +     1059.38193018920*t);
      uranus_z_0+=     0.00000325409 * Math.cos( 2.48214857847 +        9.56122755560*t);
      uranus_z_0+=     0.00000260666 * Math.cos( 5.78699886075 +       41.10198105440*t);
      uranus_z_0+=     0.00000237721 * Math.cos( 0.80288483705 +       65.22037101170*t);
      uranus_z_0+=     0.00000223998 * Math.cos( 3.91250165407 +      221.37585028530*t);
      uranus_z_0+=     0.00000220626 * Math.cos( 3.93529110558 +      106.97674337190*t);
      uranus_z_0+=     0.00000265210 * Math.cos( 5.70721287265 +       74.89347315190*t);
      uranus_z_0+=     0.00000260727 * Math.cos( 0.26432051819 +      277.03499374140*t);
      uranus_z_0+=     0.00000201268 * Math.cos( 5.94906398723 +       87.31177153950*t);
      uranus_z_0+=     0.00000165472 * Math.cos( 3.54108848226 +      490.33408917940*t);
      uranus_z_0+=     0.00000216763 * Math.cos( 2.14355016573 +       68.84370773410*t);
      uranus_z_0+=     0.00000166510 * Math.cos( 3.37208863092 +       72.33391801250*t);
      uranus_z_0+=     0.00000144942 * Math.cos( 3.24374054293 +       56.62235130260*t);
      uranus_z_0+=     0.00000151752 * Math.cos( 3.25335981894 +       71.60020482960*t);
      uranus_z_0+=     0.00000145795 * Math.cos( 5.12147352849 +       77.96299230500*t);
      uranus_z_0+=     0.00000155998 * Math.cos( 5.19284812595 +       77.22927912210*t);
      uranus_z_0+=     0.00000123397 * Math.cos( 2.06100256833 +      186.21176006410*t);
      uranus_z_0+=     0.00000123620 * Math.cos( 1.96019194023 +      288.08069400530*t);
      uranus_z_0+=     0.00000100136 * Math.cos( 2.82301109906 +      114.39910691340*t);
      uranus_z_0+=     0.00000109824 * Math.cos( 3.74385247499 +       67.66805156650*t);
      uranus_z_0+=     0.00000107550 * Math.cos( 1.08025777979 +      340.77089204480*t);

      let uranus_z_1=0.0;
      uranus_z_1+=     0.00655916626 * Math.cos( 0.01271947660 +       74.78159856730*t);
      uranus_z_1+=     0.00049648951 * Math.cos( 0.00000000000 +        0.00000000000*t);
      uranus_z_1+=     0.00023874178 * Math.cos( 2.73870491220 +      149.56319713460*t);
      uranus_z_1+=     0.00007552177 * Math.cos( 5.49304207700 +       76.26607127560*t);
      uranus_z_1+=     0.00005941304 * Math.cos( 3.61254073304 +       73.29712585900*t);
      uranus_z_1+=     0.00002868429 * Math.cos( 4.17954157878 +       63.73589830340*t);
      uranus_z_1+=     0.00002087455 * Math.cos( 5.97858625817 +        1.48447270830*t);
      uranus_z_1+=     0.00001827697 * Math.cos( 2.71810813335 +       11.04570026390*t);
      uranus_z_1+=     0.00001305063 * Math.cos( 4.52337002195 +       85.82729883120*t);
      uranus_z_1+=     0.00001158250 * Math.cos( 5.31913504112 +      224.34479570190*t);
      uranus_z_1+=     0.00000734112 * Math.cos( 3.81331728220 +       70.84944530420*t);
      uranus_z_1+=     0.00000690304 * Math.cos( 0.01086319936 +      138.51749687070*t);
      uranus_z_1+=     0.00000497091 * Math.cos( 4.70518667311 +       78.71375183040*t);
      uranus_z_1+=     0.00000525934 * Math.cos( 4.22790148916 +       71.81265315070*t);
      uranus_z_1+=     0.00000429414 * Math.cos( 4.87681143526 +      213.29909543800*t);
      uranus_z_1+=     0.00000489133 * Math.cos( 1.79190013789 +      151.04766984290*t);
      uranus_z_1+=     0.00000429528 * Math.cos( 4.40758343368 +       77.75054398390*t);
      uranus_z_1+=     0.00000390025 * Math.cos( 3.59458303816 +      148.07872442630*t);
      uranus_z_1+=     0.00000386442 * Math.cos( 1.52709843729 +      529.69096509460*t);
      uranus_z_1+=     0.00000225115 * Math.cos( 5.02814647582 +        2.96894541660*t);
      uranus_z_1+=     0.00000193252 * Math.cos( 2.74882587378 +        3.93215326310*t);
      uranus_z_1+=     0.00000102785 * Math.cos( 3.31502760721 +       77.96299230500*t);
      uranus_z_1+=     0.00000103227 * Math.cos( 5.06943606258 +       71.60020482960*t);
      uranus_z_1+=     0.00000106981 * Math.cos( 1.10631744127 +       52.69019803950*t);
      uranus_z_1=uranus_z_1 * t;

      let uranus_z_2=0.0;
      uranus_z_2+=     0.00014697858 * Math.cos( 1.75149165003 +       74.78159856730*t);
      uranus_z_2+=     0.00001600044 * Math.cos( 3.14159265359 +        0.00000000000*t);
      uranus_z_2+=     0.00000257139 * Math.cos( 5.91766895295 +       73.29712585900*t);
      uranus_z_2+=     0.00000247413 * Math.cos( 5.67197956903 +      149.56319713460*t);
      uranus_z_2+=     0.00000121840 * Math.cos( 0.75865025350 +       11.04570026390*t);
      uranus_z_2+=     0.00000113629 * Math.cos( 2.28365428558 +       85.82729883120*t);
      uranus_z_2=uranus_z_2 * t * t;

      let uranus_z_3=0.0;
      uranus_z_3+=     0.00000406961 * Math.cos( 3.16314034460 +       74.78159856730*t);
      uranus_z_3=uranus_z_3 * t * t * t;

      return uranus_z_0+uranus_z_1+uranus_z_2+uranus_z_3;
   }

   static venus_x(t){
      let venus_x_0=0.0;
      venus_x_0+=     0.72211281391 * Math.cos( 3.17575836361 +    10213.28554621100*t);
      venus_x_0+=     0.00486448018 * Math.cos( 0.00000000000 +        0.00000000000*t);
      venus_x_0+=     0.00244500474 * Math.cos( 4.05566613861 +    20426.57109242200*t);
      venus_x_0+=     0.00002800281 * Math.cos( 0.33147492492 +     2352.86615377180*t);
      venus_x_0+=     0.00001949669 * Math.cos( 4.23196016801 +     1577.34354244780*t);
      venus_x_0+=     0.00001241717 * Math.cos( 4.93573787058 +    30639.85663863300*t);
      venus_x_0+=     0.00001162258 * Math.cos( 2.87958246189 +    18073.70493865020*t);
      venus_x_0+=     0.00001046690 * Math.cos( 1.75434920413 +     6283.07584999140*t);
      venus_x_0+=     0.00000764293 * Math.cos( 0.59379588767 +      529.69096509460*t);
      venus_x_0+=     0.00000669461 * Math.cos( 1.45721228842 +    14143.49524243060*t);
      venus_x_0+=     0.00000657195 * Math.cos( 0.50086450258 +     8635.94200376320*t);
      venus_x_0+=     0.00000476445 * Math.cos( 5.84309782840 +    10186.98722641120*t);
      venus_x_0+=     0.00000474466 * Math.cos( 3.64991163504 +    10239.58386601080*t);
      venus_x_0+=     0.00000559074 * Math.cos( 1.16554783301 +    22003.91463486980*t);
      venus_x_0+=     0.00000546778 * Math.cos( 2.71490884128 +    11790.62908865880*t);
      venus_x_0+=     0.00000408988 * Math.cos( 3.92725431993 +      775.52261132400*t);
      venus_x_0+=     0.00000287059 * Math.cos( 2.79578956958 +     9683.59458111640*t);
      venus_x_0+=     0.00000268822 * Math.cos( 0.42000307859 +    10742.97651130560*t);
      venus_x_0+=     0.00000297742 * Math.cos( 5.65655811166 +     5507.55323866740*t);
      venus_x_0+=     0.00000214149 * Math.cos( 0.74884072598 +    10021.83728009940*t);
      venus_x_0+=     0.00000241103 * Math.cos( 5.80627627098 +    10988.80815753500*t);
      venus_x_0+=     0.00000209303 * Math.cos( 2.47129919435 +    10404.73381232260*t);
      venus_x_0+=     0.00000271022 * Math.cos( 2.62377780320 +    19896.88012732740*t);
      venus_x_0+=     0.00000254480 * Math.cos( 5.09961413241 +     9153.90361602180*t);
      venus_x_0+=     0.00000174985 * Math.cos( 6.12704911391 +      191.44826611160*t);
      venus_x_0+=     0.00000175040 * Math.cos( 3.53163977560 +     9437.76293488700*t);
      venus_x_0+=     0.00000122990 * Math.cos( 1.58925439374 +     1059.38193018920*t);
      venus_x_0+=     0.00000154379 * Math.cos( 5.35607704390 +     4705.73230754360*t);
      venus_x_0+=     0.00000147455 * Math.cos( 5.55780022641 +    19651.04848109800*t);

      let venus_x_1=0.0;
      venus_x_1+=     0.00033862636 * Math.cos( 3.14159265359 +        0.00000000000*t);
      venus_x_1+=     0.00017234992 * Math.cos( 0.92721124604 +    20426.57109242200*t);
      venus_x_1+=     0.00006510416 * Math.cos( 2.19289889733 +    10213.28554621100*t);
      venus_x_1+=     0.00000175153 * Math.cos( 1.80662375856 +    30639.85663863300*t);
      venus_x_1=venus_x_1 * t;

      let venus_x_2=0.0;
      venus_x_2+=     0.00000704794 * Math.cos( 5.09874399916 +    20426.57109242200*t);
      venus_x_2+=     0.00000624477 * Math.cos( 3.86836776757 +    10213.28554621100*t);
      venus_x_2+=     0.00000649010 * Math.cos( 3.14159265359 +        0.00000000000*t);
      venus_x_2=venus_x_2 * t * t;

      return venus_x_0+venus_x_1+venus_x_2;
   }

   static venus_y(t){
      let venus_y_0=0.0;
      venus_y_0+=     0.72324820731 * Math.cos( 1.60573808356 +    10213.28554621100*t);
      venus_y_0+=     0.00549506273 * Math.cos( 3.14159265359 +        0.00000000000*t);
      venus_y_0+=     0.00244884790 * Math.cos( 2.48564954004 +    20426.57109242200*t);
      venus_y_0+=     0.00002789807 * Math.cos( 5.04214523606 +     2352.86615377180*t);
      venus_y_0+=     0.00001933868 * Math.cos( 5.80597990261 +     1577.34354244780*t);
      venus_y_0+=     0.00001243658 * Math.cos( 3.36573697344 +    30639.85663863300*t);
      venus_y_0+=     0.00001164480 * Math.cos( 1.30970620277 +    18073.70493865020*t);
      venus_y_0+=     0.00001041872 * Math.cos( 0.18129136925 +     6283.07584999140*t);
      venus_y_0+=     0.00000770549 * Math.cos( 5.30366680002 +      529.69096509460*t);
      venus_y_0+=     0.00000670527 * Math.cos( 6.17032430376 +    14143.49524243060*t);
      venus_y_0+=     0.00000657675 * Math.cos( 5.21360427049 +     8635.94200376320*t);
      venus_y_0+=     0.00000477182 * Math.cos( 4.27309387857 +    10186.98722641120*t);
      venus_y_0+=     0.00000475690 * Math.cos( 2.08026660779 +    10239.58386601080*t);
      venus_y_0+=     0.00000559632 * Math.cos( 5.87842445808 +    22003.91463486980*t);
      venus_y_0+=     0.00000542381 * Math.cos( 1.15040078193 +    11790.62908865880*t);
      venus_y_0+=     0.00000367778 * Math.cos( 2.17623939625 +     9437.76293488700*t);
      venus_y_0+=     0.00000407052 * Math.cos( 2.35411923107 +      775.52261132400*t);
      venus_y_0+=     0.00000275646 * Math.cos( 1.23968348521 +     9683.59458111640*t);
      venus_y_0+=     0.00000268898 * Math.cos( 5.13218653673 +    10742.97651130560*t);
      venus_y_0+=     0.00000302219 * Math.cos( 0.94310085463 +     5507.55323866740*t);
      venus_y_0+=     0.00000214465 * Math.cos( 5.46202116536 +    10021.83728009940*t);
      venus_y_0+=     0.00000241591 * Math.cos( 4.23657289457 +    10988.80815753500*t);
      venus_y_0+=     0.00000207456 * Math.cos( 0.88354754907 +    10404.73381232260*t);
      venus_y_0+=     0.00000274181 * Math.cos( 0.42777141449 +     9153.90361602180*t);
      venus_y_0+=     0.00000271427 * Math.cos( 1.05376720660 +    19896.88012732740*t);
      venus_y_0+=     0.00000175993 * Math.cos( 1.40721119359 +      191.44826611160*t);
      venus_y_0+=     0.00000123120 * Math.cos( 0.01710584424 +     1059.38193018920*t);
      venus_y_0+=     0.00000154080 * Math.cos( 3.78432893453 +     4705.73230754360*t);
      venus_y_0+=     0.00000146618 * Math.cos( 3.98848869231 +    19651.04848109800*t);

      let venus_y_1=0.0;
      venus_y_1+=     0.00039231430 * Math.cos( 0.00000000000 +        0.00000000000*t);
      venus_y_1+=     0.00017282326 * Math.cos( 5.63824735900 +    20426.57109242200*t);
      venus_y_1+=     0.00005968075 * Math.cos( 3.60854944086 +    10213.28554621100*t);
      venus_y_1+=     0.00000175529 * Math.cos( 0.23554665359 +    30639.85663863300*t);
      venus_y_1=venus_y_1 * t;

      let venus_y_2=0.0;
      venus_y_2+=     0.00002007155 * Math.cos( 3.14159265359 +        0.00000000000*t);
      venus_y_2+=     0.00000702052 * Math.cos( 3.52724964753 +    20426.57109242200*t);
      venus_y_2+=     0.00000265709 * Math.cos( 4.68091836985 +    10213.28554621100*t);
      venus_y_2=venus_y_2 * t * t;

      return venus_y_0+venus_y_1+venus_y_2;
   }

   static venus_z(t){
      let venus_z_0=0.0;
      venus_z_0+=     0.04282990302 * Math.cos( 0.26703856476 +    10213.28554621100*t);
      venus_z_0+=     0.00035588343 * Math.cos( 3.14159265359 +        0.00000000000*t);
      venus_z_0+=     0.00014501879 * Math.cos( 1.14696911390 +    20426.57109242200*t);
      venus_z_0+=     0.00000140675 * Math.cos( 0.85984113219 +     1577.34354244780*t);
      venus_z_0+=     0.00000134921 * Math.cos( 3.70465787853 +     2352.86615377180*t);

      let venus_z_1=0.0;
      venus_z_1+=     0.00208096402 * Math.cos( 1.88967278742 +    10213.28554621100*t);
      venus_z_1+=     0.00001264989 * Math.cos( 3.71037501321 +    20426.57109242200*t);
      venus_z_1+=     0.00001364144 * Math.cos( 0.00000000000 +        0.00000000000*t);
      venus_z_1=venus_z_1 * t;

      let venus_z_2=0.0;
      venus_z_2+=     0.00009148044 * Math.cos( 3.34791005272 +    10213.28554621100*t);
      venus_z_2+=     0.00000163977 * Math.cos( 0.00000000000 +        0.00000000000*t);
      venus_z_2=venus_z_2 * t * t;

      let venus_z_3=0.0;
      venus_z_3+=     0.00000272005 * Math.cos( 4.87648116140 +    10213.28554621100*t);
      venus_z_3=venus_z_3 * t * t * t;

      return venus_z_0+venus_z_1+venus_z_2+venus_z_3;
   }

}
</script>
<script>
vsop87a_full = vsop87a_xsmall;
</script>
<script>
/*
Sample astronomy library by Greg Miller (gmiller@gregmiller.net) 2019
Released as public domain

*/


class astrolib{

	//Returns an array containing the distance, declination, and right ascension (in that order) in radians.
	//BodyNum is passed to getBody() function below, see it for which body number to supply.  Constants appear at the end of this file
	//The positions are adjusted for the parallax of the Earth, and the offset of the observer from the Earth's center
	//All input and output angles are in radians!
	static getBodyRaDec(jd,bodyNum,lat,lon,precess){
		const jdTT = astrolib.convertUTCtoTT(jd);
		let t = astrolib.convertJDToJulianMilleniaSinceJ2000(jdTT);
		
		//Get current position of Earth
		const earth = astrolib.getBody(3,t);

		let body=astrolib.getBodyLightTimeAdjusted(t,earth,bodyNum);

		//Convert to Geocrntric position
		body = astrolib.sub(body, earth);
		
		//Rotate ecliptic coordinates to J2000 coordinates
		body = astrolib.rotvsop2J2000(body);

		//TODO: rotate body for precession, nutation and bias
		let precession;
		if(precess==true){
			precession=astrolib.getPrecessionMatrix(jdTT);
			body=astrolib.vecMatrixMul(body,precession);
		}

		//Convert to topocentric
		let observerXYZ=astrolib.getObserverGeocentric(jdTT,lat,lon);

		if(precess==true){
			//TODO: rotate observerXYZ for precession, nutation and bias
			const precessionInv=astrolib.transpose(precession);
			observerXYZ=astrolib.vecMatrixMul(observerXYZ,precessionInv);
		}

		body = astrolib.sub(body,observerXYZ);

		//Convert to topocentric RA DEC by converting from cartesian coordinates to polar coordinates
		let RaDec = astrolib.toPolar(body);
		
		RaDec[1]=Math.PI/2.0-RaDec[1];  //Dec.  Offset to make 0 the equator, and the poles +/-90 deg
		if(RaDec[2]<0){RaDec[2]+=2*Math.PI;} //Ensure RA is positive
		
		return(RaDec);
	}

	static getBodyLightTimeAdjusted(t,origin,bodyNum){
		//Get current position of body
		let body = astrolib.getBody(bodyNum,t);

		let newT=t;

		for(let i=0;i<2;i++){
			//Calculate light time to body
			body = astrolib.sub(body, origin);
			let distance = Math.sqrt(body[0] * body[0] + body[1] * body[1] + body[2] * body[2]);
			distance*=1.496e+11; //Convert from AU to meters
			const lightTime=distance/299792458.0;

			//Convert light time to Julian Millenia, and subtract it from the original value of t
			newT-=lightTime / 24.0 / 60.0 / 60.0 / 365250.0;  
			//Recalculate body position adjusted for light time
			body = astrolib.getBody(bodyNum,newT);
		}

		return body;
	}

	//Returns a body's cartesian coordinates centered on the Sun.
	//Requires vsop87a_full.js, if you wish to use a different version of VSOP87, replace the class name vsop87a_full below
	static getBody(bodyNum,et){
		switch(bodyNum){
			case 0: 
				return [0,0,0]; //Sun is at the center for vsop87a
				//return vsop87e_full.getSun(et);  // "E" is the only version the Sun is not always at [0,0,0]
			case 1:
				return vsop87a_full.getMercury(et);
			case 2:
				return vsop87a_full.getVenus(et);
			case 3:
				return vsop87a_full.getEarth(et);
			case 4:
				return vsop87a_full.getMars(et);
			case 5:
				return vsop87a_full.getJupiter(et);
			case 6:
				return vsop87a_full.getSaturn(et);
			case 7:
				return vsop87a_full.getUranus(et);
			case 8:
				return vsop87a_full.getNeptune(et);
			case 9:
				//return [0,0,0]; //Vsop87a is the only version which can compute the moon
				return vsop87a_full.getEmb(et);
			case 10:
				//return [0,0,0]; //Vsop87a is the only version which can compute the moon
				return vsop87a_full.getMoon(vsop87a_full.getEarth(et), vsop87a_full.getEmb(et));
		}
	}

	static transpose(m){
		let t=new Array();
		for(let i=0;i<m.length;i++){
			t[i]=new Array();
			for(let j=0;j<m[i].length;j++){
				t[i][j]=m[j][i];
			}
		}
		return t;
	}

	static vecMatrixMul(v,m){
		let t=new Array();
		t[0]=v[0]*m[0][0]+v[1]*m[0][1]+v[2]*m[0][2];
		t[1]=v[0]*m[1][0]+v[1]*m[1][1]+v[2]*m[1][2];
		t[2]=v[0]*m[2][0]+v[1]*m[2][1]+v[2]*m[2][2];

		return t;
	}

	//Subtracts two arrays (vectors), a-b
	static sub(a, b){
		let t = new Array();
		t[0] = a[0] - b[0];
		t[1] = a[1] - b[1];
		t[2] = a[2] - b[2];
		return t;
	}

	//Gets a rotation matrix about the x axis.  Angle R is in radians
	static getXRotationMatrix(r){
		let t=new Array();
		t[0]=new Array();
		t[1]=new Array();
		t[2]=new Array();

		t[0][0]=1;
		t[0][1]=0;
		t[0][2]=0;
		t[1][0]=0;
		t[1][1]=Math.cos(r);
		t[1][2]=Math.sin(r);
		t[2][0]=0;
		t[2][1]=-Math.sin(r);
		t[2][2]=Math.cos(r);

		return t;
	}

	//Gets a rotation matrix about the y axis.  Angle R is in radians
	static getYRotationMatrix(r){
		let t=new Array();
		t[0]=new Array();
		t[1]=new Array();
		t[2]=new Array();

		t[0][0]=Math.cos(r);
		t[0][1]=0;
		t[0][2]=-Math.sin(r);
		t[1][0]=0;
		t[1][1]=1;
		t[1][2]=0;
		t[2][0]=Math.sin(r);
		t[2][1]=0;
		t[2][2]=Math.cos(r);

		return t;
	}

	//Gets a rotation matrix about the z axis.  Angle R is in radians
	static getZRotationMatrix(r){
		let t=new Array();
		t[0]=new Array();
		t[1]=new Array();
		t[2]=new Array();

		t[0][0]=Math.cos(r);
		t[0][1]=Math.sin(r);
		t[0][2]=0;
		t[1][0]=-Math.sin(r);
		t[1][1]=Math.cos(r);
		t[1][2]=0;
		t[2][0]=0;
		t[2][1]=0;
		t[2][2]=1;

		return t;
	}

	//Matrix dot product
	static dot(a,b){
		let m=new Array();
		for(let i=0;i<a.length;i++){
			m[i]=new Array();
			for(let j=0;j<b[0].length;j++){
				let temp=0;
				for(let k=0;k<b.length;k++){
					temp+=a[i][k]*b[k][j];
				}
				m[i][j]=temp;
			}
		}
		return m;
	}

	//Special "Math.floor()" function used by convertDateToJulianDate()
	static INT(d){
		if(d>0){
			return Math.floor(d);
		}
		return Math.floor(d)-1;
	}

	//Converts a JavaScript Date object into a Julian Date
	//From Meeus p61 (7.1)
	static convertDateToJulianDate(date){
		let year=date.getUTCFullYear();
		let month=date.getUTCMonth()+1;
		let day=date.getUTCDate();
		let hour=date.getUTCHours();
		let min=date.getUTCMinutes();
		let sec=date.getUTCSeconds();

		if (month < 3){
			year = year - 1;
			month = month + 12;
		}

		let b = 0;
		if (!(year<1582 || (year == 1582 && (month < 10 || (month==10 && day < 5))))){
			let a = astrolib.INT(year / 100.0);
			b = 2 - a + astrolib.INT(a / 4.0);
		}

		let jd=astrolib.INT(365.25 * (year + 4716)) + astrolib.INT(30.6001 * (month + 1)) + day + b - 1524.5;
		jd+=hour/24.0;
		jd+=min/24.0/60.0;
		jd+=sec/24.0/60.0/60.0;
		return jd;
	}

	//Converts a Julan Date to Julian Millenia since J2000, which is what VSOP87 expects as input
	static convertJDToJulianMilleniaSinceJ2000(jd){
		return (jd - 2451545.0) / 365250.0;
	}

	//Converts cartesian XYZ coordinates to polar (e.g. J2000 xyz to Right Accention and Declication)
	static toPolar(xyz){
		let t = new Array();
		t[0] = Math.sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1] + xyz[2] * xyz[2]);
		t[1] = Math.acos(xyz[2] / t[0]);
		t[2] = Math.atan2(xyz[1], xyz[0]);

		if(t[1]<0){t[1]+=2*Math.PI;}
		if(t[2]<0){t[2]+=2*Math.PI;}

		return t;
	}

	static toDmsString(d){
		let t = d * 180 / Math.PI;
		let deg = Math.trunc(t);
		t = Math.abs(t) - Math.abs(deg);
		t *= 60;
		let min = Math.trunc(t);
		t -= min;
		let sec = t * 60;
		return(deg + "d " + min + "' " + sec + "\"\r\n");
	}

	static toHmsString(h){
		let t = h * 180 / Math.PI;
		if(t<0)t+=360;
		t /= 15.0;
		let hours = Math.trunc(t);
		t = Math.abs(t) - Math.abs(hours);
		t *= 60;
		let min = Math.trunc(t);
		t -= min;
		let sec = t * 60;
		return(hours + "h " + min + "m " + sec + "s\r\n");
	}

	//Performs the rotation from ecliptic coordinates to J2000 coordinates for the given vector x
	static rotvsop2J2000(x){
		/* From VSOP87.doc
		  X        +1.000000000000  +0.000000440360  -0.000000190919   X
		  Y     =  -0.000000479966  +0.917482137087  -0.397776982902   Y
		  Z FK5     0.000000000000  +0.397776982902  +0.917482137087   Z VSOP87A
		*/
		let t = new Array();
		t[0] = x[0] + x[1] * 0.000000440360 + x[2] * -0.000000190919;
		t[1] = x[0] * -0.000000479966 + x[1] * 0.917482137087 + x[2] * -0.397776982902;
		t[2] = x[1] * 0.397776982902 + x[2] * 0.917482137087;

		return t;
	}

	//Converts a Julian Date in UTC to Terrestrial Time (TT)
	static convertUTCtoTT(jd){
		//Leap seconds are hard coded, should be updated from the IERS website for other times
		
		//TAI = UTC + leap seconds (e.g. 32)
		//TT=TAI + 32.184

		//return jd + (32.0 + 32.184) / 24.0 / 60.0 / 60.0;
		return jd + (37.0 + 32.184) / 24.0 / 60.0 / 60.0;

		/*
		https://data.iana.org/time-zones/tzdb-2018a/leap-seconds.list
		2272060800	10	# 1 Jan 1972
		2287785600	11	# 1 Jul 1972
		2303683200	12	# 1 Jan 1973
		2335219200	13	# 1 Jan 1974
		2366755200	14	# 1 Jan 1975
		2398291200	15	# 1 Jan 1976
		2429913600	16	# 1 Jan 1977
		2461449600	17	# 1 Jan 1978
		2492985600	18	# 1 Jan 1979
		2524521600	19	# 1 Jan 1980
		2571782400	20	# 1 Jul 1981
		2603318400	21	# 1 Jul 1982
		2634854400	22	# 1 Jul 1983
		2698012800	23	# 1 Jul 1985
		2776982400	24	# 1 Jan 1988
		2840140800	25	# 1 Jan 1990
		2871676800	26	# 1 Jan 1991
		2918937600	27	# 1 Jul 1992
		2950473600	28	# 1 Jul 1993
		2982009600	29	# 1 Jul 1994
		3029443200	30	# 1 Jan 1996
		3076704000	31	# 1 Jul 1997
		3124137600	32	# 1 Jan 1999
		3345062400	33	# 1 Jan 2006
		3439756800	34	# 1 Jan 2009
		3550089600	35	# 1 Jul 2012
		3644697600	36	# 1 Jul 2015
		3692217600	37	# 1 Jan 2017
		*/
	}

	//Convert Geodedic Lat Lon to geocentric XYZ position vector
	//All angles are input as radians
	static convertGeodedicLatLonToITRFXYZ(lat,lon,height){
		//Algorithm from Explanatory Supplement to the Astronomical Almanac 3rd ed. P294
		const a=6378136.6;
		const f=1/298.25642;

		const C=Math.sqrt(((Math.cos(lat)*Math.cos(lat)) + (1.0-f)*(1.0-f) * (Math.sin(lat)*Math.sin(lat))));

		const S=(1-f)*(1-f)*C;
		
		const h=height;

		let r=new Array();
		r[0]=(a*C+h) * Math.cos(lat) * Math.cos(lon);
		r[1]=(a*C+h) * Math.cos(lat) * Math.sin(lon);
		r[2]=(a*S+h) * Math.sin(lat);
		
		return r;
	}


	static getGMST(ut1){
		const D=ut1 - 2451545.0;
		const T = D/36525.0;
		let gmst = (280.46061837 + 360.98564736629*D + 0.000387933*T*T - T*T*T/38710000.0) %360.0;
		if(gmst<0){gmst+=360;}
		return gmst/15;

	}

	//Convert position vector to celestial "of date" system.
	//g(t)=R3(-GAST) r
	//(Remember to use UT1 for GAST, not ET)
	//All angles are input and output as radians
	static convertITRFToGCRS(r,ut1){
		//This is a simple rotation matrix implemenation about the Z axis, rotation angle is -GMST

		let GMST=astrolib.getGMST(ut1);
		GMST=-GMST*15.0*Math.PI/180.0;

		let m=astrolib.getZRotationMatrix(GMST);
		let t=astrolib.vecMatrixMul(r,m);

		/*
		let t=new Array();
		t[0]=r[0]*Math.cos(GMST) + r[1]*(Math.sin(GMST));
		t[1]=r[0]*(-Math.sin(GMST)) + r[1]*Math.cos(GMST);
		t[2]=r[2];
		*/

		return t;
	}

	//Convert from meters to AU
	//Multiply g(t) by 1.49597870691E+11
	static convertFromMetersToAU(r){
		let t=new Array();
		
		t[0]=r[0]/1.49597870691E+11;
		t[1]=r[1]/1.49597870691E+11;
		t[2]=r[2]/1.49597870691E+11;
		
		return t;
	}

	//Returns an observer's position in GCRS/J2000 cartesian coordinates in astronomical units
	//All angles are input and output as radians
	static getObserverGeocentric(jd,lat,lon){
		let r=astrolib.convertGeodedicLatLonToITRFXYZ(lat, lon,0);
		r=astrolib.convertITRFToGCRS(r,jd);
		r=astrolib.convertFromMetersToAU(r);
		
		return r;
	}

	//Returns the Alt/Az polar coordinates based on RA/Dec coordinates for a given location on Earth's surface.
	//All angles are input and output as radians
	static convertRaDecToAltAz(jd,lat,lon,ra,dec){
		const GMST=astrolib.getGMST(jd)*Math.PI/180.0*15.0;
		let h=GMST + lon - ra;
		
		const sina=Math.sin(dec)*Math.sin(lat)+Math.cos(dec)*Math.cos(h)*Math.cos(lat);
		const a=Math.asin(sina);

		//const cosAz=(Math.sin(dec)-Math.sin(a)*Math.sin(lat))/(Math.cos(a)*Math.cos(lat));
		const cosAz=(Math.sin(dec)*Math.cos(lat)-Math.cos(dec)*Math.cos(h)*Math.sin(lat))/Math.cos(a);
		let Az=Math.acos(cosAz);

		if(Math.sin(h)>0){Az=2.0*Math.PI-Az;}

		let t=new Array();
		t[0]=Az;
		t[1]=a;
		
		return t;
	}

	static printmat(m){
		for(let i=0;i<m.length;i++){
			let s="";
			for(let j=0;j<m[i].length;j++){
				s=s+""+m[i][j]+"\t";
			}
			console.log(s);
		}
		console.log("");
	}

	static getPrecessionMatrix(jd){
		//2006 IAU Precession.  Implemented from IERS Technical Note No 36 ch5.
		//https://www.iers.org/SharedDocs/Publikationen/EN/IERS/Publications/tn/TechnNote36/tn36_043.pdf?__blob=publicationFile&v=1

		const t =(jd - 2451545.0)/36525.0;  //5.2
		const Arcsec2Radians=Math.PI/180.0/60.0/60.0; //Converts arc seconds used in equations below to radians

		const e0 = 84381.406 * Arcsec2Radians; //5.6.4
		const omegaA = e0 + ((-0.025754 + (0.0512623 +	(-0.00772503 + (-0.000000467 + 0.0000003337*t) * t) * t) * t) * t) * Arcsec2Radians; //5.39
		const psiA = ((5038.481507 +	(-1.0790069 + (-0.00114045 + (0.000132851 - 0.0000000951*t) * t) * t) * t) * t) * Arcsec2Radians; //5.39
		const chiA = ((10.556403 + (-2.3814292 + (-0.00121197 + (0.000170663 - 0.0000000560*t) * t) * t) * t) * t) * Arcsec2Radians; //5.40


//console.log(dpsi+"\t"+deps);

		const epsA=e0 - ((46.83676900 - (0.0001831 + (0.0020034 - (0.000000576 - 0.000000043400*t) *t) *t) *t) *t) * Arcsec2Radians; //5.40
		//const dpsi1=(dpsi*Math.sin(eA)*Math.cos(chiA)-deps*Math.sin(chiA))/Math.sin(omegaA); //5.24
		//const deps1=dpsi*Math.sin(eA)*Math.sin(chiA)+deps*Math.cos(chiA);


		//Rotation matrix from 5.4.5
		//(R1(−e0) · R3(psiA) · R1(omegaA) · R3(−chiA))
		//Above eq rotates from "of date" to J2000, so we reverse the signs to go from J2000 to "of date"
		const m1=astrolib.getXRotationMatrix(e0);
		const m2=astrolib.getZRotationMatrix(-psiA);
		const m3=astrolib.getXRotationMatrix(-omegaA);
		const m4=astrolib.getZRotationMatrix(chiA);

		const m5=astrolib.dot(m4,m3);
		const m6=astrolib.dot(m5,m2);
		const precessionMatrix=astrolib.dot(m6,m1);

		/*
		//Compute nutation
		const nut=eraNut00a(0,jd);
		const dpsi=nut[0];
		const deps=nut[1];

		const m7=astrolib.getXRotationMatrix(-epsA);
		const m8=astrolib.getZRotationMatrix(dpsi);
		const m9=astrolib.getXRotationMatrix((epsA+deps));

		const m10=astrolib.dot(m7,m8);
		const m11=astrolib.dot(m10,m9);
		const nutationMatrix=astrolib.dot(precessionMatrix,m11);

		return nutationMatrix;
		*/
		return precessionMatrix;
	}

}

astrolib.SUN=0;
astrolib.MERCURY=1;
astrolib.VENUS=2;
astrolib.EARTH=3;
astrolib.MARS=4;
astrolib.JUPITER=5;
astrolib.SATURN=6;
astrolib.URANUS=7;
astrolib.NEPTUNE=8;
astrolib.EMB=9;
astrolib.MOON=10;

astrolib.bodies=["Sun","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune","Earth-Moon Barrycenter","Moon"];</script>
<script>
//Generated from https://github.com/eleanorlutz/western_constellations_atlas_of_space
// Lincense: https://github.com/eleanorlutz/western_constellations_atlas_of_space/blob/main/LICENSE (GPL)
// DSO data from https://github.com/mattiaverga/OpenNGC by CC-BY-SA-v4.0
// types: 'S' - star,'Ca' - canstelation,  'Oc' - open cluster, 'Gc' = globular cluster, 'Ga' - gallaxy, 'Ne' - nebula, 'P' - Planet
var allstars_index = {"Oc": 482, "Ga": 1809, "Ne": 2015, "Gc": 2194, "P": 2201, "Ca": 2289, "S": 7357};
var allstars = [{"DE":24.1167,"RA":56.7500,"name":"M45","t":"Oc","AM":1.6000},{"RA":130.1328,"DE":-53.0355,"AM":2.5000,"name":"IC2391","t":"Oc"},{"RA":253.5455,"DE":-41.8242,"AM":2.6000,"name":"NGC6231","t":"Oc"},{"RA":166.4492,"DE":-58.7705,"AM":3.0000,"name":"NGC3532","t":"Oc"},{"RA":130.0925,"DE":19.6721,"AM":3.1000,"name":"M44","t":"Oc"},{"RA":268.4632,"DE":-34.7928,"AM":3.3000,"name":"M7","t":"Oc"},{"RA":34.7440,"DE":57.1172,"AM":3.7000,"name":"NGC0869","t":"Oc"},{"RA":35.6337,"DE":57.1441,"AM":3.8000,"name":"NGC0884","t":"Oc"},{"RA":119.5294,"DE":-60.7535,"AM":3.8000,"name":"NGC2516","t":"Oc"},{"RA":97.0047,"DE":-4.8474,"AM":3.9000,"name":"NGC2232","t":"Oc"},{"RA":109.6728,"DE":-24.9542,"AM":4.1000,"name":"NGC2362","t":"Oc"},{"RA":266.6132,"DE":5.6487,"AM":4.2000,"name":"IC4665","t":"Oc"},{"RA":150.6232,"DE":-60.1305,"AM":4.2000,"name":"NGC3114","t":"Oc"},{"RA":265.0865,"DE":-32.2542,"AM":4.2000,"name":"M6","t":"Oc"},{"RA":156.8715,"DE":-57.6173,"AM":4.3000,"name":"IC2581","t":"Oc"},{"RA":114.1459,"DE":-14.4826,"AM":4.4000,"name":"M47","t":"Oc"},{"RA":274.2338,"DE":-18.5146,"AM":4.5000,"name":"M24","t":"Oc"},{"RA":101.4998,"DE":-20.7542,"AM":4.5000,"name":"M41","t":"Oc"},{"RA":130.6255,"DE":-48.1506,"AM":4.6000,"name":"IC2395","t":"Oc"},{"RA":277.9449,"DE":-19.1149,"AM":4.6000,"name":"M25","t":"Oc"},{"RA":279.7146,"DE":5.4622,"AM":4.6000,"name":"IC4756","t":"Oc"},{"RA":276.8135,"DE":6.5082,"AM":4.6000,"name":"NGC6633","t":"Oc"},{"RA":322.9513,"DE":48.4382,"AM":4.6000,"name":"M39","t":"Oc"},{"RA":122.5395,"DE":-49.2057,"AM":4.7000,"name":"NGC2547","t":"Oc"},{"RA":158.9532,"DE":-58.2245,"AM":4.7000,"name":"NGC3293","t":"Oc"},{"RA":92.2711,"DE":24.3386,"AM":5.1000,"name":"M35","t":"Oc"},{"RA":240.8241,"DE":-60.4314,"AM":5.1000,"name":"NGC6025","t":"Oc"},{"RA":40.5308,"DE":42.7461,"AM":5.2000,"name":"M34","t":"Oc"},{"RA":301.4977,"DE":35.7773,"AM":5.2000,"name":"NGC6871","t":"Oc"},{"RA":174.0600,"DE":-61.6052,"AM":5.3000,"name":"NGC3766","t":"Oc"},{"RA":201.8134,"DE":-59.0409,"AM":5.3300,"name":"NGC5138","t":"Oc"},{"RA":102.0743,"DE":41.0789,"AM":5.4000,"name":"NGC2281","t":"Oc"},{"RA":244.7108,"DE":-57.9346,"AM":5.4000,"name":"NGC6087","t":"Oc"},{"RA":256.1721,"DE":-37.9852,"AM":5.4000,"name":"NGC6281","t":"Oc"},{"RA":218.9066,"DE":-56.6181,"AM":5.5000,"name":"NGC5662","t":"Oc"},{"RA":263.6773,"DE":-32.5814,"AM":5.5000,"name":"NGC6374","t":"Oc"},{"RA":269.2699,"DE":-18.9853,"AM":5.5000,"name":"M23","t":"Oc"},{"RA":88.0765,"DE":32.5530,"AM":5.6000,"name":"M37","t":"Oc"},{"RA":211.8659,"DE":-48.3425,"AM":5.6000,"name":"NGC5460","t":"Oc"},{"RA":243.2960,"DE":-54.2189,"AM":5.6000,"name":"NGC6067","t":"Oc"},{"RA":352.5308,"DE":49.1341,"AM":5.6000,"name":"NGC7686","t":"Oc"},{"RA":29.3951,"DE":37.8334,"AM":5.7000,"name":"NGC0752","t":"Oc"},{"RA":118.0408,"DE":-38.5333,"AM":5.8000,"name":"NGC2477","t":"Oc"},{"RA":123.4299,"DE":-5.7504,"AM":5.8000,"name":"M48","t":"Oc"},{"RA":246.3336,"DE":-40.6537,"AM":5.8000,"name":"NGC6124","t":"Oc"},{"RA":282.7750,"DE":-6.2700,"AM":5.8000,"name":"M11","t":"Oc"},{"RA":92.1015,"DE":13.9649,"AM":5.9000,"name":"NGC2169","t":"Oc"},{"RA":105.6686,"DE":-8.3640,"AM":5.9000,"name":"M50","t":"Oc"},{"RA":206.6465,"DE":-62.9165,"AM":5.9000,"name":"NGC5281","t":"Oc"},{"RA":271.0560,"DE":-22.4901,"AM":5.9000,"name":"M21","t":"Oc"},{"RA":84.0739,"DE":34.1407,"AM":6.0000,"name":"M36","t":"Oc"},{"RA":102.9387,"DE":0.4592,"AM":6.0000,"name":"NGC2301","t":"Oc"},{"RA":155.3427,"DE":-51.7226,"AM":6.0000,"name":"NGC3228","t":"Oc"},{"RA":208.4884,"DE":-61.8691,"AM":6.0000,"name":"NGC5316","t":"Oc"},{"RA":259.6075,"DE":-42.9340,"AM":6.0000,"name":"NGC6322","t":"Oc"},{"RA":274.0903,"DE":-15.0152,"AM":6.0000,"name":"NGC6605","t":"Oc"},{"RA":75.9591,"DE":23.7676,"AM":6.1000,"name":"NGC1746","t":"Oc"},{"RA":115.4451,"DE":-14.8100,"AM":6.1000,"name":"M46","t":"Oc"},{"RA":131.5940,"DE":-52.9475,"AM":6.1000,"name":"NGC2669","t":"Oc"},{"RA":328.4178,"DE":62.6033,"AM":6.1000,"name":"NGC7160","t":"Oc"},{"RA":65.2344,"DE":50.2553,"AM":6.2000,"name":"NGC1545","t":"Oc"},{"RA":116.1218,"DE":-23.8531,"AM":6.2000,"name":"M93","t":"Oc"},{"RA":123.0651,"DE":-37.5943,"AM":6.3000,"name":"NGC2546","t":"Oc"},{"RA":217.4336,"DE":-60.7108,"AM":6.3000,"name":"NGC5617","t":"Oc"},{"RA":308.6112,"DE":28.2827,"AM":6.3000,"name":"NGC6940","t":"Oc"},{"RA":19.8860,"DE":58.2907,"AM":6.4000,"name":"NGC0457","t":"Oc"},{"RA":63.8286,"DE":51.2115,"AM":6.4000,"name":"NGC1528","t":"Oc"},{"RA":71.4815,"DE":19.0951,"AM":6.4000,"name":"NGC1647","t":"Oc"},{"RA":72.1206,"DE":10.9304,"AM":6.4000,"name":"NGC1662","t":"Oc"},{"RA":82.1770,"DE":35.8549,"AM":6.4000,"name":"M38","t":"Oc"},{"RA":253.8893,"DE":-39.4609,"AM":6.4000,"name":"NGC6242","t":"Oc"},{"RA":333.7858,"DE":49.8975,"AM":6.4000,"name":"NGC7243","t":"Oc"},{"RA":7.4925,"DE":60.2112,"AM":6.5000,"name":"NGC0129","t":"Oc"},{"RA":25.9976,"DE":61.8827,"AM":6.5000,"name":"NGC0654","t":"Oc"},{"RA":108.5220,"DE":-25.6889,"AM":6.5000,"name":"NGC2354","t":"Oc"},{"RA":121.2424,"DE":-28.1467,"AM":6.5000,"name":"NGC2520","t":"Oc"},{"RA":122.6541,"DE":-12.8207,"AM":6.5000,"name":"NGC2539","t":"Oc"},{"RA":226.0885,"DE":-54.3964,"AM":6.5000,"name":"NGC5822","t":"Oc"},{"RA":274.5123,"DE":-12.2431,"AM":6.5000,"name":"NGC6604","t":"Oc"},{"RA":57.3703,"DE":52.6553,"AM":6.6000,"name":"NGC1444","t":"Oc"},{"RA":167.5800,"DE":-60.2484,"AM":6.6000,"name":"NGC3572","t":"Oc"},{"RA":248.5193,"DE":-44.0456,"AM":6.6000,"name":"NGC6169","t":"Oc"},{"RA":305.9907,"DE":38.5077,"AM":6.6000,"name":"M29","t":"Oc"},{"RA":40.6461,"DE":61.5944,"AM":6.7000,"name":"NGC1027","t":"Oc"},{"RA":52.9172,"DE":37.3794,"AM":6.7000,"name":"NGC1342","t":"Oc"},{"RA":90.2772,"DE":23.3222,"AM":6.7000,"name":"NGC2129","t":"Oc"},{"RA":107.0283,"DE":-10.6168,"AM":6.7000,"name":"NGC2343","t":"Oc"},{"RA":114.2780,"DE":-13.8715,"AM":6.7000,"name":"NGC2423","t":"Oc"},{"RA":248.6457,"DE":-49.7719,"AM":6.7000,"name":"NGC6167","t":"Oc"},{"RA":282.8289,"DE":10.3187,"AM":6.7000,"name":"NGC6709","t":"Oc"},{"RA":359.3503,"DE":56.7083,"AM":6.7000,"name":"NGC7789","t":"Oc"},{"RA":294.3246,"DE":46.3888,"AM":6.8000,"name":"NGC6811","t":"Oc"},{"RA":261.2047,"DE":-49.9382,"AM":6.9000,"name":"IC4651","t":"Oc"},{"RA":61.9554,"DE":62.3315,"AM":6.9000,"name":"NGC1502","t":"Oc"},{"RA":115.1892,"DE":-31.6924,"AM":6.9000,"name":"NGC2439","t":"Oc"},{"RA":132.8339,"DE":11.8119,"AM":6.9000,"name":"M67","t":"Oc"},{"RA":190.5701,"DE":-62.9958,"AM":6.9000,"name":"NGC4609","t":"Oc"},{"RA":274.9937,"DE":-17.1020,"AM":6.9000,"name":"M18","t":"Oc"},{"RA":351.2017,"DE":61.5932,"AM":6.9000,"name":"M52","t":"Oc"},{"RA":10.9016,"DE":61.7669,"AM":7.0000,"name":"NGC0225","t":"Oc"},{"RA":67.9450,"DE":43.7848,"AM":7.0000,"name":"NGC1582","t":"Oc"},{"RA":77.6876,"DE":16.5128,"AM":7.0000,"name":"NGC1807","t":"Oc"},{"RA":80.0232,"DE":39.3436,"AM":7.0000,"name":"NGC1857","t":"Oc"},{"RA":124.7348,"DE":-29.7493,"AM":7.0000,"name":"NGC2571","t":"Oc"},{"RA":321.0904,"DE":36.4875,"AM":7.0000,"name":"NGC7063","t":"Oc"},{"RA":26.5669,"DE":61.2182,"AM":7.1000,"name":"NGC0663","t":"Oc"},{"RA":108.6263,"DE":-10.2659,"AM":7.1000,"name":"NGC2353","t":"Oc"},{"RA":106.7060,"DE":-10.0286,"AM":7.2000,"name":"NGC2335","t":"Oc"},{"RA":109.4297,"DE":-15.6413,"AM":7.2000,"name":"NGC2360","t":"Oc"},{"RA":142.6209,"DE":-52.9140,"AM":7.2000,"name":"NGC2910","t":"Oc"},{"RA":187.4801,"DE":-64.7897,"AM":7.2000,"name":"NGC4463","t":"Oc"},{"RA":246.9437,"DE":-49.1512,"AM":7.2000,"name":"NGC6134","t":"Oc"},{"RA":248.9469,"DE":-45.6437,"AM":7.2000,"name":"NGC6178","t":"Oc"},{"RA":252.3675,"DE":-53.7283,"AM":7.2000,"name":"NGC6208","t":"Oc"},{"RA":266.7570,"DE":-31.5294,"AM":7.2000,"name":"NGC6425","t":"Oc"},{"RA":322.3239,"DE":47.1263,"AM":7.2000,"name":"NGC7082","t":"Oc"},{"RA":304.1386,"DE":37.5553,"AM":7.3000,"name":"IC4996","t":"Oc"},{"RA":98.6603,"DE":8.3664,"AM":7.3000,"name":"NGC2251","t":"Oc"},{"RA":112.9030,"DE":-17.1904,"AM":7.3000,"name":"NGC2409","t":"Oc"},{"RA":118.7932,"DE":-24.2546,"AM":7.3000,"name":"NGC2482","t":"Oc"},{"RA":295.3254,"DE":40.1868,"AM":7.3000,"name":"NGC6819","t":"Oc"},{"RA":129.7630,"DE":-46.2273,"AM":7.3200,"name":"NGC2645","t":"Oc"},{"RA":141.9093,"DE":-57.0069,"AM":7.4000,"name":"IC2488","t":"Oc"},{"RA":23.3409,"DE":60.6580,"AM":7.4000,"name":"M103","t":"Oc"},{"RA":111.2910,"DE":-21.0199,"AM":7.4000,"name":"NGC2384","t":"Oc"},{"RA":112.0122,"DE":-11.7197,"AM":7.4000,"name":"NGC2396","t":"Oc"},{"RA":124.6466,"DE":-30.6356,"AM":7.4000,"name":"NGC2567","t":"Oc"},{"RA":159.6893,"DE":-54.1307,"AM":7.4000,"name":"NGC3330","t":"Oc"},{"RA":181.6649,"DE":-61.2501,"AM":7.4000,"name":"NGC4103","t":"Oc"},{"RA":186.0252,"DE":-61.8704,"AM":7.4000,"name":"NGC4349","t":"Oc"},{"RA":251.0306,"DE":-47.4627,"AM":7.4000,"name":"NGC6200","t":"Oc"},{"RA":305.8002,"DE":40.7786,"AM":7.4000,"name":"NGC6910","t":"Oc"},{"RA":80.6839,"DE":33.4120,"AM":7.5000,"name":"NGC1893","t":"Oc"},{"RA":101.9174,"DE":-3.1477,"AM":7.5000,"name":"NGC2286","t":"Oc"},{"RA":283.6432,"DE":-19.9011,"AM":7.5000,"name":"NGC6716","t":"Oc"},{"RA":286.9544,"DE":4.2664,"AM":7.5000,"name":"NGC6755","t":"Oc"},{"RA":38.3293,"DE":57.5697,"AM":7.6000,"name":"NGC0957","t":"Oc"},{"RA":72.7726,"DE":43.6762,"AM":7.6000,"name":"NGC1664","t":"Oc"},{"RA":118.9116,"DE":-27.8868,"AM":7.6000,"name":"NGC2483","t":"Oc"},{"RA":120.0074,"DE":-10.7696,"AM":7.6000,"name":"NGC2506","t":"Oc"},{"RA":121.7671,"DE":-29.8839,"AM":7.6000,"name":"NGC2533","t":"Oc"},{"RA":171.4045,"DE":-43.2501,"AM":7.6000,"name":"NGC3680","t":"Oc"},{"RA":270.8506,"DE":-27.8861,"AM":7.6000,"name":"NGC6520","t":"Oc"},{"RA":300.9799,"DE":44.1591,"AM":7.6000,"name":"NGC6866","t":"Oc"},{"RA":317.6992,"DE":45.6218,"AM":7.6000,"name":"NGC7039","t":"Oc"},{"RA":77.0237,"DE":37.0228,"AM":7.7000,"name":"NGC1778","t":"Oc"},{"RA":78.1095,"DE":16.6841,"AM":7.7000,"name":"NGC1817","t":"Oc"},{"RA":98.6790,"DE":5.3662,"AM":7.7000,"name":"NGC2252","t":"Oc"},{"RA":107.0783,"DE":-13.1937,"AM":7.7000,"name":"NGC2345","t":"Oc"},{"RA":166.0115,"DE":-61.3683,"AM":7.7000,"name":"NGC3519","t":"Oc"},{"RA":216.9470,"DE":-59.6322,"AM":7.7000,"name":"NGC5606","t":"Oc"},{"RA":331.2827,"DE":46.4835,"AM":7.7000,"name":"NGC7209","t":"Oc"},{"RA":333.1042,"DE":57.2713,"AM":7.7000,"name":"NGC7234","t":"Oc"},{"RA":131.3728,"DE":-48.7916,"AM":7.8000,"name":"NGC2670","t":"Oc"},{"RA":279.1390,"DE":-8.2208,"AM":7.8000,"name":"NGC6664","t":"Oc"},{"RA":298.0523,"DE":29.4082,"AM":7.8000,"name":"NGC6834","t":"Oc"},{"RA":307.8755,"DE":60.6621,"AM":7.8000,"name":"NGC6939","t":"Oc"},{"RA":26.0958,"DE":60.6692,"AM":7.9000,"name":"NGC0659","t":"Oc"},{"RA":29.6247,"DE":55.4746,"AM":7.9000,"name":"NGC0744","t":"Oc"},{"RA":110.0189,"DE":-21.8841,"AM":7.9000,"name":"NGC2367","t":"Oc"},{"RA":113.3033,"DE":-15.4539,"AM":7.9000,"name":"NGC2414","t":"Oc"},{"RA":119.0623,"DE":-30.0608,"AM":7.9000,"name":"NGC2489","t":"Oc"},{"RA":226.3776,"DE":-55.6037,"AM":7.9000,"name":"NGC5823","t":"Oc"},{"RA":297.7483,"DE":23.1001,"AM":7.9000,"name":"NGC6830","t":"Oc"},{"RA":347.7657,"DE":60.5709,"AM":7.9000,"name":"NGC7510","t":"Oc"},{"RA":110.9836,"DE":-13.2634,"AM":8.0000,"name":"NGC2374","t":"Oc"},{"RA":111.8035,"DE":13.6082,"AM":8.0000,"name":"NGC2395","t":"Oc"},{"RA":255.1892,"DE":-44.6550,"AM":8.0000,"name":"NGC6259","t":"Oc"},{"RA":271.8440,"DE":-23.2962,"AM":8.0000,"name":"NGC6546","t":"Oc"},{"RA":278.2056,"DE":-17.2287,"AM":8.0000,"name":"NGC6647","t":"Oc"},{"RA":302.8323,"DE":35.8322,"AM":8.0000,"name":"NGC6883","t":"Oc"},{"RA":11.8647,"DE":85.2696,"AM":8.1000,"name":"NGC0188","t":"Oc"},{"RA":248.1901,"DE":-52.6440,"AM":8.1000,"name":"NGC6152","t":"Oc"},{"RA":169.3640,"DE":-62.7251,"AM":8.2000,"name":"IC2714","t":"Oc"},{"RA":25.7630,"DE":64.0366,"AM":8.2000,"name":"NGC0637","t":"Oc"},{"RA":82.0190,"DE":35.3257,"AM":8.2000,"name":"NGC1907","t":"Oc"},{"RA":164.8909,"DE":-60.3369,"AM":8.2000,"name":"NGC3496","t":"Oc"},{"RA":168.2457,"DE":-60.7890,"AM":8.2000,"name":"NGC3590","t":"Oc"},{"RA":251.5396,"DE":-47.0170,"AM":8.2000,"name":"NGC6204","t":"Oc"},{"RA":254.4229,"DE":-44.8119,"AM":8.2000,"name":"NGC6249","t":"Oc"},{"RA":267.6693,"DE":-30.2116,"AM":8.2000,"name":"NGC6451","t":"Oc"},{"RA":268.3005,"DE":-22.2751,"AM":8.2000,"name":"NGC6469","t":"Oc"},{"RA":81.8421,"DE":-67.4638,"AM":8.2200,"name":"NGC1968","t":"Oc"},{"RA":114.5996,"DE":21.5741,"AM":8.3000,"name":"NGC2420","t":"Oc"},{"RA":114.0492,"DE":-20.6122,"AM":8.3000,"name":"NGC2421","t":"Oc"},{"RA":116.8922,"DE":-27.1948,"AM":8.3000,"name":"NGC2453","t":"Oc"},{"RA":143.2955,"DE":-53.3960,"AM":8.3000,"name":"NGC2925","t":"Oc"},{"RA":177.6384,"DE":-55.6698,"AM":8.3000,"name":"NGC3960","t":"Oc"},{"RA":285.3398,"DE":11.6156,"AM":8.3000,"name":"NGC6738","t":"Oc"},{"RA":320.8645,"DE":46.3785,"AM":8.3000,"name":"NGC7062","t":"Oc"},{"RA":84.1864,"DE":-69.4986,"AM":8.3900,"name":"NGC2055","t":"Oc"},{"RA":91.1983,"DE":24.0710,"AM":8.4000,"name":"IC2157","t":"Oc"},{"RA":48.6728,"DE":47.2387,"AM":8.4000,"name":"NGC1245","t":"Oc"},{"RA":62.4779,"DE":49.5173,"AM":8.4000,"name":"NGC1513","t":"Oc"},{"RA":106.0332,"DE":1.0446,"AM":8.4000,"name":"NGC2324","t":"Oc"},{"RA":111.1662,"DE":-20.9476,"AM":8.4000,"name":"NGC2383","t":"Oc"},{"RA":129.3123,"DE":-29.9504,"AM":8.4000,"name":"NGC2627","t":"Oc"},{"RA":187.1098,"DE":-60.1032,"AM":8.4000,"name":"NGC4439","t":"Oc"},{"RA":231.8618,"DE":-54.5288,"AM":8.4000,"name":"NGC5925","t":"Oc"},{"RA":322.6148,"DE":51.6005,"AM":8.4000,"name":"NGC7086","t":"Oc"},{"RA":335.0266,"DE":58.0518,"AM":8.4000,"name":"NGC7261","t":"Oc"},{"RA":95.2052,"DE":-7.2838,"AM":8.4500,"name":"NGC2215","t":"Oc"},{"RA":93.4413,"DE":12.8067,"AM":8.5000,"name":"NGC2194","t":"Oc"},{"RA":97.4154,"DE":6.8307,"AM":8.5000,"name":"NGC2236","t":"Oc"},{"RA":106.7493,"DE":27.2616,"AM":8.5000,"name":"NGC2331","t":"Oc"},{"RA":241.8974,"DE":-54.0149,"AM":8.5000,"name":"NGC6031","t":"Oc"},{"RA":250.0995,"DE":-43.3668,"AM":8.5000,"name":"NGC6192","t":"Oc"},{"RA":264.4014,"DE":-35.0259,"AM":8.5000,"name":"NGC6396","t":"Oc"},{"RA":278.1579,"DE":-16.8839,"AM":8.5000,"name":"NGC6645","t":"Oc"},{"RA":359.6011,"DE":61.2083,"AM":8.5000,"name":"NGC7790","t":"Oc"},{"RA":91.8567,"DE":24.0962,"AM":8.6000,"name":"NGC2158","t":"Oc"},{"RA":93.8843,"DE":-18.6659,"AM":8.6000,"name":"NGC2204","t":"Oc"},{"RA":130.6376,"DE":-45.0005,"AM":8.6000,"name":"NGC2659","t":"Oc"},{"RA":194.4932,"DE":-64.9617,"AM":8.6000,"name":"NGC4815","t":"Oc"},{"RA":273.1844,"DE":-21.6280,"AM":8.6000,"name":"NGC6568","t":"Oc"},{"RA":93.0297,"DE":5.4586,"AM":8.7000,"name":"NGC2186","t":"Oc"},{"RA":9.8987,"DE":61.0945,"AM":8.8000,"name":"NGC0189","t":"Oc"},{"RA":18.9907,"DE":58.8171,"AM":8.8000,"name":"NGC0436","t":"Oc"},{"RA":130.6583,"DE":-47.2007,"AM":8.8000,"name":"NGC2660","t":"Oc"},{"RA":147.1460,"DE":-56.4301,"AM":8.8000,"name":"NGC3033","t":"Oc"},{"RA":180.5216,"DE":-63.2235,"AM":8.8000,"name":"NGC4052","t":"Oc"},{"RA":222.2248,"DE":-54.4977,"AM":8.8000,"name":"NGC5749","t":"Oc"},{"RA":265.0533,"DE":-36.9477,"AM":8.8000,"name":"NGC6400","t":"Oc"},{"RA":292.6460,"DE":20.2610,"AM":8.8000,"name":"NGC6802","t":"Oc"},{"RA":281.3278,"DE":-9.3836,"AM":8.8700,"name":"M26","t":"Oc"},{"RA":38.1288,"DE":44.5935,"AM":8.9000,"name":"NGC0956","t":"Oc"},{"RA":98.4578,"DE":-5.0844,"AM":8.9000,"name":"NGC2250","t":"Oc"},{"RA":102.9737,"DE":-7.0827,"AM":8.9000,"name":"NGC2299","t":"Oc"},{"RA":186.0138,"DE":-58.1238,"AM":8.9000,"name":"NGC4337","t":"Oc"},{"RA":195.0183,"DE":-59.6094,"AM":8.9000,"name":"NGC4852","t":"Oc"},{"RA":278.3665,"DE":-10.4028,"AM":8.9000,"name":"NGC6649","t":"Oc"},{"RA":238.0360,"DE":-56.4728,"AM":9.0000,"name":"NGC5999","t":"Oc"},{"RA":275.7582,"DE":-12.0237,"AM":9.0000,"name":"NGC6625","t":"Oc"},{"RA":334.0055,"DE":53.9913,"AM":9.1000,"name":"IC1442","t":"Oc"},{"RA":8.2664,"DE":63.3090,"AM":9.1000,"name":"NGC0146","t":"Oc"},{"RA":88.4384,"DE":0.4108,"AM":9.1000,"name":"NGC2112","t":"Oc"},{"RA":98.9569,"DE":7.6733,"AM":9.1000,"name":"NGC2254","t":"Oc"},{"RA":202.7719,"DE":-60.9392,"AM":9.1000,"name":"NGC5168","t":"Oc"},{"RA":316.8023,"DE":50.8756,"AM":9.1000,"name":"NGC7031","t":"Oc"},{"RA":125.8503,"DE":-29.5087,"AM":9.2000,"name":"NGC2587","t":"Oc"},{"RA":130.8639,"DE":-32.6562,"AM":9.2000,"name":"NGC2658","t":"Oc"},{"RA":282.6907,"DE":-5.2054,"AM":9.2000,"name":"NGC6704","t":"Oc"},{"RA":333.7980,"DE":54.3426,"AM":9.2000,"name":"NGC7245","t":"Oc"},{"RA":84.1617,"DE":-69.3835,"AM":9.2500,"name":"NGC2050","t":"Oc"},{"RA":17.0750,"DE":61.5833,"AM":9.3000,"name":"NGC0381","t":"Oc"},{"RA":120.1993,"DE":-19.0505,"AM":9.3000,"name":"NGC2509","t":"Oc"},{"RA":326.2896,"DE":65.7744,"AM":9.3000,"name":"NGC7142","t":"Oc"},{"RA":73.7957,"DE":-67.1689,"AM":9.3700,"name":"NGC1747","t":"Oc"},{"RA":7.8207,"DE":63.3526,"AM":9.4000,"name":"NGC0133","t":"Oc"},{"RA":90.7294,"DE":10.4465,"AM":9.4000,"name":"NGC2141","t":"Oc"},{"RA":97.3937,"DE":-31.2813,"AM":9.4000,"name":"NGC2243","t":"Oc"},{"RA":184.2890,"DE":-55.2861,"AM":9.4000,"name":"NGC4230","t":"Oc"},{"RA":280.5582,"DE":-6.2123,"AM":9.4000,"name":"NGC6683","t":"Oc"},{"RA":359.1899,"DE":61.3999,"AM":9.4000,"name":"NGC7788","t":"Oc"},{"RA":22.3882,"DE":63.3014,"AM":9.5000,"name":"NGC0559","t":"Oc"},{"RA":100.8300,"DE":26.9696,"AM":9.5000,"name":"NGC2266","t":"Oc"},{"RA":116.3125,"DE":-37.9674,"AM":9.5000,"name":"NGC2451","t":"Oc"},{"RA":255.5433,"DE":-39.7282,"AM":9.5000,"name":"NGC6268","t":"Oc"},{"RA":290.2217,"DE":37.7719,"AM":9.5000,"name":"NGC6791","t":"Oc"},{"RA":14.0735,"DE":-72.4629,"AM":9.5500,"name":"NGC0330","t":"Oc"},{"RA":84.0399,"DE":-68.9234,"AM":9.5800,"name":"NGC2042","t":"Oc"},{"RA":61.1329,"DE":52.6614,"AM":9.6000,"name":"NGC1496","t":"Oc"},{"RA":104.4481,"DE":-4.6113,"AM":9.6000,"name":"NGC2311","t":"Oc"},{"RA":118.7753,"DE":-17.7078,"AM":9.6000,"name":"NGC2479","t":"Oc"},{"RA":269.9616,"DE":-17.4503,"AM":9.6000,"name":"NGC6507","t":"Oc"},{"RA":332.6120,"DE":55.3986,"AM":9.6000,"name":"NGC7226","t":"Oc"},{"RA":204.2350,"DE":-62.0931,"AM":9.7000,"name":"IC4291","t":"Oc"},{"RA":109.2469,"DE":13.7499,"AM":9.7000,"name":"NGC2355","t":"Oc"},{"RA":125.3662,"DE":-30.2935,"AM":9.7000,"name":"NGC2580","t":"Oc"},{"RA":150.1647,"DE":-54.7877,"AM":9.7000,"name":"NGC3105","t":"Oc"},{"RA":321.0963,"DE":48.0093,"AM":9.7000,"name":"NGC7067","t":"Oc"},{"RA":325.9909,"DE":53.7151,"AM":9.7000,"name":"NGC7128","t":"Oc"},{"RA":337.0118,"DE":52.2891,"AM":9.7000,"name":"NGC7295","t":"Oc"},{"RA":76.8632,"DE":-71.1954,"AM":9.7300,"name":"NGC1848","t":"Oc"},{"RA":6.3183,"DE":61.3235,"AM":9.8000,"name":"NGC0103","t":"Oc"},{"RA":220.8737,"DE":-57.5770,"AM":9.8000,"name":"NGC5715","t":"Oc"},{"RA":246.1099,"DE":-51.9483,"AM":9.8000,"name":"NGC6115","t":"Oc"},{"RA":145.0480,"DE":-50.3209,"AM":9.9000,"name":"NGC2972","t":"Oc"},{"RA":74.1572,"DE":-66.4789,"AM":9.9400,"name":"NGC1761","t":"Oc"},{"RA":81.9205,"DE":-69.1343,"AM":9.9900,"name":"NGC1984","t":"Oc"},{"RA":100.8212,"DE":4.6243,"AM":10.0000,"name":"NGC2269","t":"Oc"},{"RA":103.7984,"DE":17.9928,"AM":10.0000,"name":"NGC2304","t":"Oc"},{"RA":273.9539,"DE":-22.1376,"AM":10.0000,"name":"NGC6583","t":"Oc"},{"RA":252.3484,"DE":-44.7315,"AM":10.1000,"name":"NGC6216","t":"Oc"},{"RA":76.4375,"DE":-70.5816,"AM":10.2000,"name":"NGC1845","t":"Oc"},{"RA":115.2245,"DE":-19.0691,"AM":10.2000,"name":"NGC2432","t":"Oc"},{"RA":117.2442,"DE":-21.2979,"AM":10.2000,"name":"NGC2455","t":"Oc"},{"RA":254.7714,"DE":-52.7088,"AM":10.2000,"name":"NGC6253","t":"Oc"},{"RA":81.7195,"DE":-68.8367,"AM":10.2800,"name":"NGC1970","t":"Oc"},{"RA":81.9959,"DE":-67.4241,"AM":10.3000,"name":"NGC1974","t":"Oc"},{"RA":83.7526,"DE":-69.7316,"AM":10.3100,"name":"NGC2037","t":"Oc"},{"RA":83.0270,"DE":-69.2430,"AM":10.4300,"name":"NGC2015","t":"Oc"},{"RA":74.4629,"DE":-69.3922,"AM":10.5000,"name":"NGC1782","t":"Oc"},{"RA":104.0150,"DE":-7.1743,"AM":10.5000,"name":"NGC2309","t":"Oc"},{"RA":81.5284,"DE":-66.5973,"AM":10.5800,"name":"NGC1951","t":"Oc"},{"RA":83.0842,"DE":-67.5231,"AM":10.5800,"name":"NGC2011","t":"Oc"},{"RA":84.0258,"DE":-69.1987,"AM":10.5900,"name":"NGC2044","t":"Oc"},{"RA":264.9057,"DE":-33.2467,"AM":10.6000,"name":"NGC6404","t":"Oc"},{"RA":287.1774,"DE":4.7058,"AM":10.6000,"name":"NGC6756","t":"Oc"},{"RA":74.1137,"DE":-69.4006,"AM":10.6100,"name":"NGC1767","t":"Oc"},{"RA":68.7178,"DE":45.2714,"AM":10.7000,"name":"NGC1605","t":"Oc"},{"RA":238.9529,"DE":-57.4374,"AM":10.7000,"name":"NGC6005","t":"Oc"},{"RA":85.6293,"DE":-68.2732,"AM":10.7300,"name":"NGC2098","t":"Oc"},{"RA":73.5819,"DE":-67.0996,"AM":10.7600,"name":"NGC1735","t":"Oc"},{"RA":74.5287,"DE":-67.2423,"AM":10.7600,"name":"NGC1774","t":"Oc"},{"RA":99.5893,"DE":10.8836,"AM":10.8000,"name":"NGC2259","t":"Oc"},{"RA":201.4142,"DE":-63.4583,"AM":10.8000,"name":"NGC5120","t":"Oc"},{"RA":81.6805,"DE":-69.1015,"AM":10.8100,"name":"NGC1967","t":"Oc"},{"RA":82.8375,"DE":-66.9653,"AM":10.8800,"name":"NGC2006","t":"Oc"},{"RA":15.9727,"DE":-72.8237,"AM":10.9000,"name":"NGC0376","t":"Oc"},{"RA":93.8226,"DE":39.8552,"AM":10.9000,"name":"NGC2192","t":"Oc"},{"RA":75.4350,"DE":-65.8233,"AM":10.9200,"name":"NGC1787","t":"Oc"},{"RA":93.2372,"DE":-68.2607,"AM":10.9300,"name":"NGC2214","t":"Oc"},{"RA":83.1402,"DE":-71.7155,"AM":10.9400,"name":"NGC2025","t":"Oc"},{"RA":74.2200,"DE":-69.5561,"AM":10.9700,"name":"NGC1772","t":"Oc"},{"RA":83.7488,"DE":-66.9163,"AM":10.9700,"name":"NGC2027","t":"Oc"},{"RA":24.0989,"DE":64.5366,"AM":11.0000,"name":"NGC0609","t":"Oc"},{"RA":156.6307,"DE":-60.6752,"AM":11.0000,"name":"NGC3255","t":"Oc"},{"RA":82.7465,"DE":-69.1817,"AM":11.0200,"name":"NGC2009","t":"Oc"},{"RA":77.6646,"DE":-68.7523,"AM":11.0400,"name":"NGC1860","t":"Oc"},{"RA":274.6124,"DE":-18.4061,"AM":11.1000,"name":"NGC6603","t":"Oc"},{"RA":79.5804,"DE":-69.5365,"AM":11.1400,"name":"NGC1913","t":"Oc"},{"RA":129.6083,"DE":-34.7716,"AM":11.2000,"name":"NGC2635","t":"Oc"},{"RA":84.4101,"DE":-70.2365,"AM":11.2400,"name":"NGC2065","t":"Oc"},{"RA":85.5742,"DE":-68.4586,"AM":11.3100,"name":"NGC2096","t":"Oc"},{"RA":85.5854,"DE":-69.4871,"AM":11.4400,"name":"NGC2102","t":"Oc"},{"RA":81.5739,"DE":-68.8376,"AM":11.4700,"name":"NGC1962","t":"Oc"},{"RA":72.4811,"DE":-69.7563,"AM":11.5000,"name":"NGC1704","t":"Oc"},{"RA":76.0070,"DE":-67.2659,"AM":11.5000,"name":"NGC1820","t":"Oc"},{"RA":79.9538,"DE":-69.4483,"AM":11.5100,"name":"NGC1922","t":"Oc"},{"RA":85.8037,"DE":-70.6399,"AM":11.5100,"name":"NGC2107","t":"Oc"},{"RA":85.4573,"DE":-68.9214,"AM":11.5700,"name":"NGC2093","t":"Oc"},{"RA":131.5495,"DE":-41.8772,"AM":11.6000,"name":"NGC2671","t":"Oc"},{"RA":83.6279,"DE":-69.7801,"AM":11.6300,"name":"NGC2033","t":"Oc"},{"RA":87.8387,"DE":-69.3591,"AM":11.6400,"name":"NGC2127","t":"Oc"},{"RA":86.9413,"DE":-67.4502,"AM":11.6500,"name":"NGC2117","t":"Oc"},{"RA":18.7228,"DE":-71.5527,"AM":11.6600,"name":"NGC0458","t":"Oc"},{"RA":84.0306,"DE":-71.0114,"AM":11.6900,"name":"NGC2051","t":"Oc"},{"RA":28.0993,"DE":61.8526,"AM":11.7000,"name":"IC0166","t":"Oc"},{"RA":64.7113,"DE":58.2495,"AM":11.7000,"name":"IC0361","t":"Oc"},{"RA":81.6303,"DE":-68.8055,"AM":11.7000,"name":"NGC1965","t":"Oc"},{"RA":276.7973,"DE":-12.0312,"AM":11.7000,"name":"NGC6631","t":"Oc"},{"RA":12.8091,"DE":-73.1615,"AM":11.7100,"name":"NGC0290","t":"Oc"},{"RA":82.6455,"DE":-70.8197,"AM":11.7200,"name":"NGC2010","t":"Oc"},{"RA":13.3503,"DE":-72.1971,"AM":11.7300,"name":"NGC0299","t":"Oc"},{"RA":90.0243,"DE":-68.6369,"AM":11.7500,"name":"NGC2172","t":"Oc"},{"RA":15.5423,"DE":-71.6047,"AM":11.7700,"name":"NGC0361","t":"Oc"},{"RA":79.5797,"DE":-66.6274,"AM":11.7700,"name":"NGC1902","t":"Oc"},{"RA":84.1415,"DE":-70.6719,"AM":11.7700,"name":"NGC2056","t":"Oc"},{"RA":47.9195,"DE":53.3482,"AM":11.8000,"name":"NGC1220","t":"Oc"},{"RA":76.5098,"DE":-68.6268,"AM":11.8000,"name":"NGC1839","t":"Oc"},{"RA":110.2763,"DE":-10.3718,"AM":11.8000,"name":"NGC2368","t":"Oc"},{"RA":125.7899,"DE":-32.9752,"AM":11.8000,"name":"NGC2588","t":"Oc"},{"RA":207.1873,"DE":-64.6854,"AM":11.8000,"name":"NGC5288","t":"Oc"},{"RA":259.0483,"DE":-39.4250,"AM":11.8000,"name":"NGC6318","t":"Oc"},{"RA":81.6910,"DE":-68.8199,"AM":11.8300,"name":"NGC1966","t":"Oc"},{"RA":84.2259,"DE":-70.1623,"AM":11.8500,"name":"NGC2058","t":"Oc"},{"RA":105.1342,"DE":3.0422,"AM":11.8500,"name":"NGC2319","t":"Oc"},{"RA":79.1766,"DE":-69.6562,"AM":11.8600,"name":"NGC1898","t":"Oc"},{"RA":75.2636,"DE":-69.0826,"AM":11.8700,"name":"NGC1804","t":"Oc"},{"RA":75.8470,"DE":-66.3818,"AM":11.9000,"name":"NGC1810","t":"Oc"},{"RA":81.6885,"DE":-69.8516,"AM":11.9000,"name":"NGC1971","t":"Oc"},{"RA":83.6761,"DE":-70.5629,"AM":11.9200,"name":"NGC2038","t":"Oc"},{"RA":14.9496,"DE":-72.3323,"AM":11.9600,"name":"IC1611","t":"Oc"},{"RA":78.7744,"DE":-68.9776,"AM":11.9700,"name":"NGC1885","t":"Oc"},{"RA":81.4758,"DE":46.4901,"AM":12.0000,"name":"NGC1883","t":"Oc"},{"RA":318.2892,"DE":42.4962,"AM":12.0000,"name":"NGC7044","t":"Oc"},{"RA":76.0793,"DE":-68.9264,"AM":12.0400,"name":"NGC1825","t":"Oc"},{"RA":83.3778,"DE":-67.4529,"AM":12.0600,"name":"NGC2021","t":"Oc"},{"RA":13.5591,"DE":-72.2423,"AM":12.0700,"name":"NGC0306","t":"Oc"},{"RA":85.2418,"DE":-69.4371,"AM":12.0700,"name":"NGC2091","t":"Oc"},{"RA":88.5961,"DE":-70.9010,"AM":12.0700,"name":"NGC2145","t":"Oc"},{"RA":76.8778,"DE":-67.3234,"AM":12.0800,"name":"NGC1844","t":"Oc"},{"RA":75.8540,"DE":-70.3355,"AM":12.0900,"name":"NGC1823","t":"Oc"},{"RA":16.9820,"DE":-71.7684,"AM":12.1000,"name":"NGC0411","t":"Oc"},{"RA":81.8718,"DE":-71.8794,"AM":12.1400,"name":"NGC2000","t":"Oc"},{"RA":78.9636,"DE":-69.4685,"AM":12.1600,"name":"NGC1894","t":"Oc"},{"RA":89.5535,"DE":-68.2896,"AM":12.1600,"name":"NGC2160","t":"Oc"},{"RA":11.7923,"DE":-73.4772,"AM":12.1700,"name":"NGC0265","t":"Oc"},{"RA":81.4026,"DE":-69.9269,"AM":12.1700,"name":"NGC1959","t":"Oc"},{"RA":84.2297,"DE":-70.2689,"AM":12.1700,"name":"NGC2057","t":"Oc"},{"RA":84.4154,"DE":-67.4129,"AM":12.1800,"name":"NGC2053","t":"Oc"},{"RA":86.0955,"DE":-68.5478,"AM":12.2100,"name":"NGC2109","t":"Oc"},{"RA":73.9900,"DE":-70.2251,"AM":12.2200,"name":"NGC1766","t":"Oc"},{"RA":76.3934,"DE":-68.6279,"AM":12.2200,"name":"NGC1836","t":"Oc"},{"RA":13.2696,"DE":-73.3804,"AM":12.2400,"name":"NGC0294","t":"Oc"},{"RA":73.1058,"DE":-67.0507,"AM":12.2500,"name":"NGC1718","t":"Oc"},{"RA":8.2186,"DE":-73.1204,"AM":12.2600,"name":"NGC0152","t":"Oc"},{"RA":77.8825,"DE":-65.2497,"AM":12.2600,"name":"NGC1859","t":"Oc"},{"RA":76.2325,"DE":-70.7140,"AM":12.2700,"name":"NGC1837","t":"Oc"},{"RA":83.9194,"DE":-66.0350,"AM":12.2900,"name":"NGC2029","t":"Oc"},{"RA":73.2941,"DE":-68.6500,"AM":12.3000,"name":"NGC1732","t":"Oc"},{"RA":14.9942,"DE":-72.3707,"AM":12.3100,"name":"IC1612","t":"Oc"},{"RA":78.8889,"DE":-66.1296,"AM":12.3300,"name":"NGC1882","t":"Oc"},{"RA":92.6748,"DE":-71.5284,"AM":12.3800,"name":"NGC2213","t":"Oc"},{"RA":74.9092,"DE":-69.5576,"AM":12.4100,"name":"NGC1793","t":"Oc"},{"RA":75.6135,"DE":-70.6211,"AM":12.4100,"name":"NGC1815","t":"Oc"},{"RA":16.3410,"DE":-72.0425,"AM":12.4200,"name":"IC1624","t":"Oc"},{"RA":74.9454,"DE":-69.8012,"AM":12.4200,"name":"NGC1795","t":"Oc"},{"RA":88.5674,"DE":-68.5998,"AM":12.4400,"name":"NGC2140","t":"Oc"},{"RA":86.1375,"DE":-70.9933,"AM":12.4500,"name":"NGC2111","t":"Oc"},{"RA":81.6348,"DE":-69.8414,"AM":12.4600,"name":"NGC1969","t":"Oc"},{"RA":76.7840,"DE":-68.9714,"AM":12.4700,"name":"NGC1847","t":"Oc"},{"RA":80.2354,"DE":-69.4779,"AM":12.4700,"name":"NGC1928","t":"Oc"},{"RA":85.2492,"DE":-68.4654,"AM":12.4700,"name":"NGC2088","t":"Oc"},{"RA":86.5505,"DE":-68.0483,"AM":12.4800,"name":"NGC2114","t":"Oc"},{"RA":11.4722,"DE":-73.5068,"AM":12.5000,"name":"NGC0256","t":"Oc"},{"RA":72.3653,"DE":-69.8508,"AM":12.5000,"name":"NGC1702","t":"Oc"},{"RA":139.8453,"DE":-40.5204,"AM":12.5000,"name":"NGC2849","t":"Oc"},{"RA":76.0870,"DE":-69.3882,"AM":12.5200,"name":"NGC1828","t":"Oc"},{"RA":74.2283,"DE":-70.4320,"AM":12.5500,"name":"NGC1775","t":"Oc"},{"RA":76.1595,"DE":-69.3402,"AM":12.5600,"name":"NGC1830","t":"Oc"},{"RA":74.1155,"DE":-67.6937,"AM":12.5800,"name":"NGC1764","t":"Oc"},{"RA":12.0918,"DE":-73.5315,"AM":12.5900,"name":"NGC0269","t":"Oc"},{"RA":46.4820,"DE":44.3831,"AM":12.6000,"name":"NGC1193","t":"Oc"},{"RA":112.3517,"DE":-13.9662,"AM":12.6000,"name":"NGC2401","t":"Oc"},{"RA":223.3843,"DE":-52.6705,"AM":12.6000,"name":"NGC5764","t":"Oc"},{"RA":81.3183,"DE":-66.3946,"AM":12.6200,"name":"NGC1946","t":"Oc"},{"RA":81.6973,"DE":-69.8383,"AM":12.6200,"name":"NGC1972","t":"Oc"},{"RA":10.1821,"DE":-73.3857,"AM":12.6400,"name":"NGC0222","t":"Oc"},{"RA":83.9064,"DE":-70.2407,"AM":12.6400,"name":"NGC2046","t":"Oc"},{"RA":88.3048,"DE":-69.4820,"AM":12.6600,"name":"NGC2137","t":"Oc"},{"RA":85.0113,"DE":-66.8757,"AM":12.6700,"name":"NGC2062","t":"Oc"},{"RA":79.0247,"DE":-66.3186,"AM":12.7200,"name":"NGC1887","t":"Oc"},{"RA":75.6678,"DE":-70.3179,"AM":12.7600,"name":"NGC1813","t":"Oc"},{"RA":77.3950,"DE":-66.3158,"AM":12.7700,"name":"NGC1849","t":"Oc"},{"RA":83.6308,"DE":-70.0644,"AM":12.7700,"name":"NGC2036","t":"Oc"},{"RA":74.2507,"DE":-68.2494,"AM":12.7900,"name":"NGC1768","t":"Oc"},{"RA":78.4410,"DE":-72.0780,"AM":12.8100,"name":"NGC1890","t":"Oc"},{"RA":90.3187,"DE":-67.7332,"AM":12.8300,"name":"NGC2177","t":"Oc"},{"RA":84.2523,"DE":-70.1290,"AM":12.8500,"name":"NGC2059","t":"Oc"},{"RA":78.1692,"DE":-67.6213,"AM":12.8600,"name":"NGC1864","t":"Oc"},{"RA":89.8922,"DE":-67.9423,"AM":12.8600,"name":"NGC2166","t":"Oc"},{"RA":10.2768,"DE":-73.3524,"AM":12.8700,"name":"NGC0231","t":"Oc"},{"RA":83.4524,"DE":-69.9518,"AM":12.8800,"name":"NGC2028","t":"Oc"},{"RA":78.1045,"DE":-68.7710,"AM":12.9100,"name":"NGC1865","t":"Oc"},{"RA":86.8132,"DE":-68.5079,"AM":12.9200,"name":"NGC2116","t":"Oc"},{"RA":76.5328,"DE":-68.4452,"AM":12.9300,"name":"NGC1838","t":"Oc"},{"RA":78.2121,"DE":-70.4717,"AM":12.9400,"name":"NGC1878","t":"Oc"},{"RA":88.9400,"DE":-68.2016,"AM":12.9400,"name":"NGC2147","t":"Oc"},{"RA":79.8448,"DE":-69.7878,"AM":12.9500,"name":"NGC1921","t":"Oc"},{"RA":343.5836,"DE":60.8155,"AM":13.0000,"name":"NGC7419","t":"Oc"},{"RA":8.9911,"DE":-73.1664,"AM":13.0100,"name":"NGC0176","t":"Oc"},{"RA":74.6655,"DE":-66.4296,"AM":13.0100,"name":"NGC1776","t":"Oc"},{"RA":22.3598,"DE":-73.5605,"AM":13.0200,"name":"NGC0602","t":"Oc"},{"RA":75.9615,"DE":-67.2608,"AM":13.0200,"name":"NGC1816","t":"Oc"},{"RA":85.6507,"DE":-67.3189,"AM":13.0900,"name":"NGC2095","t":"Oc"},{"RA":302.6993,"DE":41.1739,"AM":13.1000,"name":"IC1311","t":"Oc"},{"RA":73.3895,"DE":-68.7688,"AM":13.1000,"name":"NGC1734","t":"Oc"},{"RA":84.4297,"DE":-70.1666,"AM":13.1000,"name":"NGC2066","t":"Oc"},{"RA":74.7770,"DE":-70.1688,"AM":13.1200,"name":"NGC1791","t":"Oc"},{"RA":76.2883,"DE":-66.2106,"AM":13.1500,"name":"NGC1822","t":"Oc"},{"RA":83.9708,"DE":-70.1927,"AM":13.1500,"name":"NGC2047","t":"Oc"},{"RA":77.5923,"DE":-70.7771,"AM":13.1600,"name":"NGC1861","t":"Oc"},{"RA":81.1375,"DE":-69.9023,"AM":13.1700,"name":"NGC1950","t":"Oc"},{"RA":79.5988,"DE":-67.2782,"AM":13.2100,"name":"NGC1905","t":"Oc"},{"RA":84.6016,"DE":-70.2341,"AM":13.2100,"name":"NGC2072","t":"Oc"},{"RA":76.3887,"DE":-66.2297,"AM":13.2500,"name":"NGC1826","t":"Oc"},{"RA":95.7140,"DE":-68.9254,"AM":13.2500,"name":"NGC2241","t":"Oc"},{"RA":17.3558,"DE":-71.7672,"AM":13.2600,"name":"NGC0422","t":"Oc"},{"RA":73.5198,"DE":-66.6826,"AM":13.3100,"name":"NGC1733","t":"Oc"},{"RA":78.1439,"DE":-66.1544,"AM":13.3300,"name":"NGC1862","t":"Oc"},{"RA":78.4261,"DE":-66.2919,"AM":13.3500,"name":"NGC1867","t":"Oc"},{"RA":86.9149,"DE":-69.1318,"AM":13.3800,"name":"NGC2118","t":"Oc"},{"RA":82.6446,"DE":-63.1995,"AM":13.4300,"name":"NGC1997","t":"Oc"},{"RA":81.1856,"DE":-63.9421,"AM":13.4600,"name":"NGC1942","t":"Oc"},{"RA":79.3803,"DE":-67.4510,"AM":13.4900,"name":"NGC1897","t":"Oc"},{"RA":18.1570,"DE":-71.7618,"AM":13.5100,"name":"IC1660","t":"Oc"},{"RA":73.7336,"DE":-68.1887,"AM":13.5600,"name":"NGC1749","t":"Oc"},{"RA":79.7891,"DE":-63.0237,"AM":13.5900,"name":"NGC1900","t":"Oc"},{"RA":80.6138,"DE":-66.1522,"AM":13.8000,"name":"NGC1933","t":"Oc"},{"RA":16.5560,"DE":-73.2961,"AM":13.8200,"name":"IC1626","t":"Oc"},{"RA":72.1249,"DE":-68.2429,"AM":13.9500,"name":"NGC1696","t":"Oc"},{"RA":17.9754,"DE":-71.3306,"AM":14.0000,"name":"IC1655","t":"Oc"},{"RA":76.8254,"DE":-67.2732,"AM":14.0200,"name":"NGC1842","t":"Oc"},{"RA":18.1365,"DE":-73.4567,"AM":14.0300,"name":"IC1662","t":"Oc"},{"RA":70.6652,"DE":-69.8213,"AM":14.0700,"name":"NGC1673","t":"Oc"},{"RA":302.9828,"DE":26.4888,"AM":14.1000,"name":"NGC6882","t":"Oc"},{"RA":299.1172,"DE":32.3497,"AM":14.2000,"name":"NGC6846","t":"Oc"},{"RA":10.1245,"DE":-73.4040,"AM":14.3900,"name":"NGC0220","t":"Oc"},{"RA":72.3481,"DE":13.1511,"AM":14.5400,"name":"NGC1663","t":"Oc"},{"RA":17.4133,"DE":-71.7690,"AM":14.9900,"name":"IC1641","t":"Oc"},{"RA":13.1866,"DE":-72.8286,"AM":2.2000,"name":"NGC0292","t":"Ga"},{"RA":10.6848,"DE":41.2691,"AM":3.4400,"name":"M31","t":"Ga"},{"RA":23.4620,"DE":30.6602,"AM":5.7200,"name":"M33","t":"Ga"},{"RA":201.3651,"DE":-43.0191,"AM":6.8400,"name":"NGC5128","t":"Ga"},{"RA":148.8882,"DE":69.0653,"AM":6.9400,"name":"M81","t":"Ga"},{"RA":204.2540,"DE":-29.8654,"AM":7.5200,"name":"M83","t":"Ga"},{"RA":210.8023,"DE":54.3489,"AM":7.8600,"name":"M101","t":"Ga"},{"RA":3.7233,"DE":-39.1966,"AM":7.8700,"name":"NGC0055","t":"Ga"},{"RA":189.9976,"DE":-11.6231,"AM":8.0000,"name":"M104","t":"Ga"},{"RA":10.0920,"DE":41.6853,"AM":8.0700,"name":"M110","t":"Ga"},{"RA":10.6743,"DE":40.8653,"AM":8.0800,"name":"M32","t":"Ga"},{"RA":296.2406,"DE":-14.8034,"AM":8.1000,"name":"NGC6822","t":"Ga"},{"RA":13.7228,"DE":-37.6844,"AM":8.1300,"name":"NGC0300","t":"Ga"},{"RA":192.7211,"DE":41.1204,"AM":8.2400,"name":"M94","t":"Ga"},{"RA":287.4421,"DE":-63.8575,"AM":8.2500,"name":"NGC6744","t":"Ga"},{"RA":202.4696,"DE":47.1952,"AM":8.3600,"name":"M51","t":"Ga"},{"RA":114.2142,"DE":65.6026,"AM":8.3800,"name":"NGC2403","t":"Ga"},{"RA":148.9697,"DE":69.6794,"AM":8.4100,"name":"M82","t":"Ga"},{"RA":184.7396,"DE":47.3040,"AM":8.4100,"name":"M106","t":"Ga"},{"RA":194.1818,"DE":21.6830,"AM":8.5200,"name":"M64","t":"Ga"},{"RA":50.6738,"DE":-37.2082,"AM":8.5300,"name":"NGC1316","t":"Ga"},{"RA":198.9555,"DE":42.0293,"AM":8.5900,"name":"M63","t":"Ga"},{"RA":187.7059,"DE":12.3911,"AM":8.6300,"name":"M87","t":"Ga"},{"RA":190.9166,"DE":11.5527,"AM":8.7900,"name":"M60","t":"Ga"},{"RA":49.3275,"DE":-41.1081,"AM":8.8100,"name":"NGC1269","t":"Ga"},{"RA":40.6696,"DE":0.0133,"AM":8.8700,"name":"M77","t":"Ga"},{"RA":186.5489,"DE":12.9462,"AM":8.9000,"name":"M86","t":"Ga"},{"RA":170.0623,"DE":12.9915,"AM":8.9200,"name":"M66","t":"Ga"},{"RA":166.4524,"DE":0.0359,"AM":9.0200,"name":"NGC3521","t":"Ga"},{"RA":186.3505,"DE":18.1915,"AM":9.0500,"name":"M85","t":"Ga"},{"RA":143.0421,"DE":21.5008,"AM":9.0700,"name":"NGC2903","t":"Ga"},{"RA":11.7856,"DE":-20.7604,"AM":9.1000,"name":"NGC0247","t":"Ga"},{"RA":190.5334,"DE":32.5415,"AM":9.1900,"name":"NGC4631","t":"Ga"},{"RA":22.4484,"DE":-6.9801,"AM":9.2000,"name":"IC0127","t":"Ga"},{"RA":287.3063,"DE":-63.4655,"AM":9.2000,"name":"IC4820","t":"Ga"},{"RA":9.7415,"DE":48.3374,"AM":9.2000,"name":"NGC0185","t":"Ga"},{"RA":140.5110,"DE":50.9765,"AM":9.2200,"name":"NGC2841","t":"Ga"},{"RA":302.4753,"DE":-48.3796,"AM":9.2200,"name":"NGC6868","t":"Ga"},{"RA":161.6906,"DE":11.8199,"AM":9.2500,"name":"M96","t":"Ga"},{"RA":359.4576,"DE":-32.5910,"AM":9.2800,"name":"NGC7793","t":"Ga"},{"RA":169.7330,"DE":13.0924,"AM":9.3200,"name":"M65","t":"Ga"},{"RA":40.1000,"DE":39.0633,"AM":9.3500,"name":"NGC1023","t":"Ga"},{"RA":185.7285,"DE":15.8218,"AM":9.3500,"name":"M100","t":"Ga"},{"RA":64.0436,"DE":-55.7801,"AM":9.4000,"name":"NGC1553","t":"Ga"},{"RA":146.4116,"DE":-31.1911,"AM":9.4100,"name":"NGC2997","t":"Ga"},{"RA":24.1740,"DE":15.7837,"AM":9.4600,"name":"M74","t":"Ga"},{"RA":41.5794,"DE":-30.2749,"AM":9.4800,"name":"NGC1097","t":"Ga"},{"RA":170.0707,"DE":13.5897,"AM":9.4800,"name":"NGC3628","t":"Ga"},{"RA":339.2667,"DE":34.4155,"AM":9.4800,"name":"NGC7331","t":"Ga"},{"RA":5.0722,"DE":59.3038,"AM":9.5000,"name":"IC0010","t":"Ga"},{"RA":8.3005,"DE":48.5087,"AM":9.5000,"name":"NGC0147","t":"Ga"},{"RA":189.2075,"DE":13.1629,"AM":9.5400,"name":"M90","t":"Ga"},{"RA":202.4983,"DE":47.2661,"AM":9.5500,"name":"NGC5195","t":"Ga"},{"RA":169.5688,"DE":-32.8141,"AM":9.5600,"name":"NGC3621","t":"Ga"},{"RA":190.5093,"DE":11.6470,"AM":9.5600,"name":"M59","t":"Ga"},{"RA":54.6210,"DE":-35.4507,"AM":9.5900,"name":"NGC1399","t":"Ga"},{"RA":53.4015,"DE":-36.1404,"AM":9.6300,"name":"NGC1365","t":"Ga"},{"RA":187.0462,"DE":44.0936,"AM":9.6400,"name":"NGC4449","t":"Ga"},{"RA":185.4787,"DE":4.4736,"AM":9.6500,"name":"M61","t":"Ga"},{"RA":200.4900,"DE":-36.6302,"AM":9.6500,"name":"NGC5102","t":"Ga"},{"RA":189.4313,"DE":11.8182,"AM":9.6600,"name":"M58","t":"Ga"},{"RA":55.0494,"DE":-18.5801,"AM":9.6700,"name":"NGC1407","t":"Ga"},{"RA":71.4271,"DE":-59.2472,"AM":9.6800,"name":"NGC1672","t":"Ga"},{"RA":182.0251,"DE":65.1741,"AM":9.7200,"name":"NGC4125","t":"Ga"},{"RA":65.0018,"DE":-54.9378,"AM":9.7300,"name":"NGC1566","t":"Ga"},{"RA":160.9904,"DE":11.7038,"AM":9.7300,"name":"M95","t":"Ga"},{"RA":187.8504,"DE":25.7752,"AM":9.7400,"name":"NGC4494","t":"Ga"},{"RA":188.9159,"DE":12.5563,"AM":9.7500,"name":"M89","t":"Ga"},{"RA":161.9566,"DE":12.5816,"AM":9.7600,"name":"M105","t":"Ga"},{"RA":63.9380,"DE":-55.5922,"AM":9.7900,"name":"NGC1549","t":"Ga"},{"RA":133.1722,"DE":33.4218,"AM":9.7900,"name":"NGC2683","t":"Ga"},{"RA":187.6510,"DE":41.6439,"AM":9.7900,"name":"NGC4490","t":"Ga"},{"RA":177.7570,"DE":-28.8060,"AM":9.8000,"name":"NGC3923","t":"Ga"},{"RA":160.8798,"DE":24.9222,"AM":9.8600,"name":"NGC3344","t":"Ga"},{"RA":47.4396,"DE":-20.5793,"AM":9.8700,"name":"NGC1232","t":"Ga"},{"RA":137.9062,"DE":60.0372,"AM":9.8700,"name":"NGC2768","t":"Ga"},{"RA":184.7067,"DE":14.4165,"AM":9.8700,"name":"M99","t":"Ga"},{"RA":179.3999,"DE":53.3745,"AM":9.8800,"name":"M109","t":"Ga"},{"RA":226.6229,"DE":55.7632,"AM":9.8900,"name":"M102","t":"Ga"},{"RA":35.6392,"DE":42.3491,"AM":9.9300,"name":"NGC0891","t":"Ga"},{"RA":54.1150,"DE":-34.9762,"AM":9.9300,"name":"NGC1380","t":"Ga"},{"RA":183.9132,"DE":36.3269,"AM":9.9300,"name":"NGC4214","t":"Ga"},{"RA":76.9264,"DE":-37.5131,"AM":9.9400,"name":"NGC1808","t":"Ga"},{"RA":193.0921,"DE":-1.1997,"AM":9.9500,"name":"NGC4753","t":"Ga"},{"RA":55.5065,"DE":-47.2221,"AM":9.9900,"name":"NGC1433","t":"Ga"},{"RA":49.5669,"DE":-66.4982,"AM":10.0000,"name":"NGC1313","t":"Ga"},{"RA":54.7163,"DE":-35.5944,"AM":10.0000,"name":"NGC1404","t":"Ga"},{"RA":16.1991,"DE":2.1178,"AM":10.0100,"name":"IC1613","t":"Ga"},{"RA":183.9768,"DE":13.1494,"AM":10.0100,"name":"NGC4216","t":"Ga"},{"RA":188.9902,"DE":27.9600,"AM":10.0100,"name":"NGC4559","t":"Ga"},{"RA":199.7284,"DE":-21.0391,"AM":10.0100,"name":"NGC5068","t":"Ga"},{"RA":144.1869,"DE":-21.1281,"AM":10.0400,"name":"NGC2935","t":"Ga"},{"RA":150.7787,"DE":-26.1596,"AM":10.0400,"name":"NGC3109","t":"Ga"},{"RA":167.8790,"DE":55.6741,"AM":10.0600,"name":"M108","t":"Ga"},{"RA":184.1755,"DE":69.4626,"AM":10.0800,"name":"NGC4236","t":"Ga"},{"RA":187.1235,"DE":17.0849,"AM":10.0800,"name":"NGC4450","t":"Ga"},{"RA":186.4536,"DE":33.5469,"AM":10.1100,"name":"NGC4395","t":"Ga"},{"RA":7.5915,"DE":-33.2440,"AM":10.1200,"name":"NGC0134","t":"Ga"},{"RA":36.8203,"DE":33.5792,"AM":10.1200,"name":"NGC0925","t":"Ga"},{"RA":186.6129,"DE":31.2235,"AM":10.1200,"name":"NGC4414","t":"Ga"},{"RA":150.8295,"DE":68.7339,"AM":10.1400,"name":"NGC3077","t":"Ga"},{"RA":183.4512,"DE":14.9003,"AM":10.1400,"name":"M98","t":"Ga"},{"RA":138.0812,"DE":-24.1726,"AM":10.1600,"name":"NGC2784","t":"Ga"},{"RA":146.8144,"DE":67.9164,"AM":10.1600,"name":"NGC2976","t":"Ga"},{"RA":185.0284,"DE":29.2808,"AM":10.1600,"name":"NGC4278","t":"Ga"},{"RA":186.9400,"DE":13.0088,"AM":10.1700,"name":"NGC4438","t":"Ga"},{"RA":35.7690,"DE":-21.2339,"AM":10.1800,"name":"NGC0908","t":"Ga"},{"RA":76.3102,"DE":-37.9808,"AM":10.1800,"name":"NGC1792","t":"Ga"},{"RA":187.4536,"DE":13.4294,"AM":10.2000,"name":"NGC4473","t":"Ga"},{"RA":197.1564,"DE":-49.5064,"AM":10.2000,"name":"NGC4976","t":"Ga"},{"RA":67.9147,"DE":-54.6023,"AM":10.2600,"name":"NGC1617","t":"Ga"},{"RA":267.3601,"DE":70.1444,"AM":10.2800,"name":"NGC6503","t":"Ga"},{"RA":133.3864,"DE":51.3137,"AM":10.2900,"name":"NGC2681","t":"Ga"},{"RA":165.0774,"DE":13.9012,"AM":10.2900,"name":"NGC3489","t":"Ga"},{"RA":29.8316,"DE":19.0075,"AM":10.3100,"name":"NGC0772","t":"Ga"},{"RA":52.0820,"DE":-31.0682,"AM":10.3200,"name":"NGC1340","t":"Ga"},{"RA":188.8730,"DE":-3.7932,"AM":10.3200,"name":"NGC4546","t":"Ga"},{"RA":154.9790,"DE":45.5496,"AM":10.3300,"name":"NGC3198","t":"Ga"},{"RA":161.9264,"DE":13.9859,"AM":10.3800,"name":"NGC3377","t":"Ga"},{"RA":178.2060,"DE":44.1207,"AM":10.3800,"name":"NGC3938","t":"Ga"},{"RA":344.3265,"DE":-41.0706,"AM":10.3800,"name":"NGC7424","t":"Ga"},{"RA":167.4902,"DE":-37.5392,"AM":10.4000,"name":"NGC3557","t":"Ga"},{"RA":184.9608,"DE":29.6145,"AM":10.4100,"name":"NGC4274","t":"Ga"},{"RA":199.5211,"DE":-26.8372,"AM":10.4100,"name":"NGC5061","t":"Ga"},{"RA":49.9212,"DE":-19.4114,"AM":10.4200,"name":"NGC1300","t":"Ga"},{"RA":114.0993,"DE":-69.5308,"AM":10.4200,"name":"NGC2442","t":"Ga"},{"RA":128.3452,"DE":-22.9737,"AM":10.4200,"name":"NGC2613","t":"Ga"},{"RA":187.5092,"DE":13.6366,"AM":10.4200,"name":"NGC4477","t":"Ga"},{"RA":170.2785,"DE":3.2348,"AM":10.4400,"name":"NGC3640","t":"Ga"},{"RA":64.3990,"DE":-62.7837,"AM":10.4500,"name":"NGC1559","t":"Ga"},{"RA":282.2412,"DE":-65.1734,"AM":10.4500,"name":"NGC6684","t":"Ga"},{"RA":225.2968,"DE":1.7020,"AM":10.4600,"name":"NGC5813","t":"Ga"},{"RA":344.3065,"DE":-43.3961,"AM":10.4700,"name":"IC5267","t":"Ga"},{"RA":40.2700,"DE":-8.2558,"AM":10.4700,"name":"NGC1052","t":"Ga"},{"RA":200.4427,"DE":-27.4305,"AM":10.4700,"name":"NGC5101","t":"Ga"},{"RA":22.8365,"DE":-6.8681,"AM":10.4800,"name":"NGC0584","t":"Ga"},{"RA":65.4951,"DE":-56.9748,"AM":10.4800,"name":"NGC1574","t":"Ga"},{"RA":137.5838,"DE":7.0379,"AM":10.4800,"name":"NGC2775","t":"Ga"},{"RA":186.2656,"DE":12.8870,"AM":10.4900,"name":"M84","t":"Ga"},{"RA":204.9832,"DE":-31.6401,"AM":10.4900,"name":"NGC5253","t":"Ga"},{"RA":191.2750,"DE":3.0558,"AM":10.5000,"name":"NGC4664","t":"Ga"},{"RA":209.0300,"DE":5.2548,"AM":10.5100,"name":"NGC5363","t":"Ga"},{"RA":52.7838,"DE":-33.6286,"AM":10.5200,"name":"NGC1350","t":"Ga"},{"RA":190.9903,"DE":32.1703,"AM":10.5200,"name":"NGC4656 NED01","t":"Ga"},{"RA":165.0995,"DE":28.9751,"AM":10.5300,"name":"NGC3486","t":"Ga"},{"RA":50.9850,"DE":-36.4647,"AM":10.5400,"name":"NGC1326","t":"Ga"},{"RA":60.9762,"DE":-43.3489,"AM":10.5400,"name":"NGC1512","t":"Ga"},{"RA":162.7220,"DE":13.4121,"AM":10.5400,"name":"NGC3412","t":"Ga"},{"RA":188.6127,"DE":2.1881,"AM":10.5500,"name":"NGC4536","t":"Ga"},{"RA":215.0829,"DE":3.9337,"AM":10.5500,"name":"NGC5566","t":"Ga"},{"RA":161.6536,"DE":63.2242,"AM":10.5700,"name":"NGC3359","t":"Ga"},{"RA":349.0448,"DE":-42.5847,"AM":10.5700,"name":"NGC7552","t":"Ga"},{"RA":185.6326,"DE":29.8959,"AM":10.5800,"name":"NGC4314","t":"Ga"},{"RA":40.4385,"DE":0.4432,"AM":10.5900,"name":"NGC1055","t":"Ga"},{"RA":94.6571,"DE":78.3570,"AM":10.5900,"name":"NGC2146","t":"Ga"},{"RA":63.1802,"DE":-57.7380,"AM":10.6000,"name":"NGC1543","t":"Ga"},{"RA":147.5926,"DE":72.2786,"AM":10.6100,"name":"NGC2985","t":"Ga"},{"RA":150.0595,"DE":-19.6370,"AM":10.6100,"name":"NGC3091","t":"Ga"},{"RA":154.2235,"DE":73.4008,"AM":10.6100,"name":"NGC3147","t":"Ga"},{"RA":173.1452,"DE":53.0679,"AM":10.6100,"name":"NGC3718","t":"Ga"},{"RA":349.5979,"DE":-42.3706,"AM":10.6200,"name":"NGC7582","t":"Ga"},{"RA":46.0333,"DE":-26.0696,"AM":10.6400,"name":"NGC1201","t":"Ga"},{"RA":94.0918,"DE":-21.3727,"AM":10.6500,"name":"NGC2207","t":"Ga"},{"RA":309.3087,"DE":66.1056,"AM":10.6500,"name":"NGC6951","t":"Ga"},{"RA":177.1591,"DE":48.7108,"AM":10.6700,"name":"NGC3893","t":"Ga"},{"RA":54.2377,"DE":-35.5066,"AM":10.6900,"name":"NGC1387","t":"Ga"},{"RA":328.1768,"DE":-48.2537,"AM":10.7100,"name":"NGC7144","t":"Ga"},{"RA":353.6145,"DE":-36.1011,"AM":10.7200,"name":"IC5332","t":"Ga"},{"RA":3.5166,"DE":-23.1821,"AM":10.7300,"name":"NGC0045","t":"Ga"},{"RA":41.4996,"DE":-7.5785,"AM":10.7300,"name":"NGC1084","t":"Ga"},{"RA":181.7630,"DE":43.0657,"AM":10.7400,"name":"NGC4111","t":"Ga"},{"RA":319.7512,"DE":-48.5622,"AM":10.7400,"name":"NGC7049","t":"Ga"},{"RA":190.3869,"DE":41.1508,"AM":10.7800,"name":"NGC4618","t":"Ga"},{"RA":202.4533,"DE":-17.9664,"AM":10.7900,"name":"NGC5170","t":"Ga"},{"RA":211.2567,"DE":53.6622,"AM":10.7900,"name":"NGC5474","t":"Ga"},{"RA":81.6984,"DE":-63.7600,"AM":10.8000,"name":"NGC1947","t":"Ga"},{"RA":186.9187,"DE":13.0789,"AM":10.8000,"name":"NGC4435","t":"Ga"},{"RA":83.3407,"DE":-21.9458,"AM":10.8100,"name":"NGC1964","t":"Ga"},{"RA":186.2310,"DE":11.7042,"AM":10.8100,"name":"NGC4371","t":"Ga"},{"RA":155.3962,"DE":-34.2668,"AM":10.8200,"name":"NGC3223","t":"Ga"},{"RA":184.3757,"DE":45.6193,"AM":10.8300,"name":"NGC4242","t":"Ga"},{"RA":346.2360,"DE":12.3229,"AM":10.8500,"name":"NGC7479","t":"Ga"},{"RA":150.4908,"DE":55.6798,"AM":10.8600,"name":"NGC3079","t":"Ga"},{"RA":157.0978,"DE":68.4121,"AM":10.8700,"name":"IC2574","t":"Ga"},{"RA":154.6037,"DE":21.8940,"AM":10.8800,"name":"NGC3193","t":"Ga"},{"RA":219.7962,"DE":5.3635,"AM":10.8800,"name":"NGC5701","t":"Ga"},{"RA":330.6730,"DE":-51.2964,"AM":10.9000,"name":"IC5152","t":"Ga"},{"RA":38.3931,"DE":-39.0451,"AM":10.9100,"name":"NGC0986","t":"Ga"},{"RA":54.0165,"DE":-35.4412,"AM":10.9100,"name":"NGC1379","t":"Ga"},{"RA":62.4660,"DE":-56.1184,"AM":10.9200,"name":"NGC1533","t":"Ga"},{"RA":63.6523,"DE":-56.0608,"AM":10.9200,"name":"NGC1546","t":"Ga"},{"RA":190.9276,"DE":16.3934,"AM":10.9200,"name":"NGC4651","t":"Ga"},{"RA":22.6212,"DE":-22.6674,"AM":10.9300,"name":"NGC0578","t":"Ga"},{"RA":146.0668,"DE":-21.2780,"AM":10.9300,"name":"NGC2986","t":"Ga"},{"RA":159.1784,"DE":-27.5283,"AM":10.9300,"name":"NGC3311","t":"Ga"},{"RA":306.1172,"DE":-43.6535,"AM":10.9300,"name":"NGC6902","t":"Ga"},{"RA":54.3702,"DE":-24.5003,"AM":10.9400,"name":"NGC1385","t":"Ga"},{"RA":54.8785,"DE":-18.6881,"AM":10.9600,"name":"NGC1400","t":"Ga"},{"RA":177.3051,"DE":-29.2767,"AM":10.9600,"name":"NGC3904","t":"Ga"},{"RA":215.2653,"DE":3.2710,"AM":10.9600,"name":"NGC5576","t":"Ga"},{"RA":66.9088,"DE":-55.0278,"AM":10.9700,"name":"NGC1596","t":"Ga"},{"RA":85.5194,"DE":69.3784,"AM":10.9900,"name":"NGC1961","t":"Ga"},{"RA":151.4507,"DE":-67.3780,"AM":11.0000,"name":"NGC3136","t":"Ga"},{"RA":202.3080,"DE":-33.1738,"AM":11.0000,"name":"NGC5161","t":"Ga"},{"RA":214.6131,"DE":-43.3886,"AM":11.0000,"name":"NGC5530","t":"Ga"},{"RA":257.6035,"DE":72.3044,"AM":11.0100,"name":"NGC6340","t":"Ga"},{"RA":40.0999,"DE":-8.4336,"AM":11.0200,"name":"NGC1042","t":"Ga"},{"RA":50.6845,"DE":-37.1037,"AM":11.0200,"name":"NGC1317","t":"Ga"},{"RA":157.2561,"DE":-44.6568,"AM":11.0200,"name":"NGC3261","t":"Ga"},{"RA":186.4448,"DE":12.6621,"AM":11.0200,"name":"NGC4388","t":"Ga"},{"RA":353.3186,"DE":-45.0160,"AM":11.0300,"name":"IC5328","t":"Ga"},{"RA":61.0113,"DE":-54.1001,"AM":11.0300,"name":"NGC1515","t":"Ga"},{"RA":67.7044,"DE":64.8479,"AM":11.0300,"name":"NGC1569","t":"Ga"},{"RA":156.6345,"DE":-39.9439,"AM":11.0300,"name":"NGC3250","t":"Ga"},{"RA":193.3715,"DE":2.1684,"AM":11.0400,"name":"NGC4772","t":"Ga"},{"RA":287.8485,"DE":-57.0496,"AM":11.0400,"name":"NGC6753","t":"Ga"},{"RA":323.9362,"DE":-63.9028,"AM":11.0400,"name":"NGC7083","t":"Ga"},{"RA":186.3243,"DE":-39.7597,"AM":11.0500,"name":"NGC4373","t":"Ga"},{"RA":324.1202,"DE":-54.5573,"AM":11.0500,"name":"NGC7090","t":"Ga"},{"RA":149.6025,"DE":-26.9267,"AM":11.0700,"name":"NGC3078","t":"Ga"},{"RA":159.7894,"DE":41.6867,"AM":11.0700,"name":"NGC3319","t":"Ga"},{"RA":172.5311,"DE":9.2766,"AM":11.0700,"name":"NGC3705","t":"Ga"},{"RA":188.0260,"DE":11.1764,"AM":11.0700,"name":"NGC4503","t":"Ga"},{"RA":296.3131,"DE":-54.3441,"AM":11.0800,"name":"IC4889","t":"Ga"},{"RA":53.8191,"DE":-35.2263,"AM":11.0800,"name":"NGC1374","t":"Ga"},{"RA":133.9072,"DE":78.2231,"AM":11.0800,"name":"NGC2655","t":"Ga"},{"RA":172.4351,"DE":-36.3913,"AM":11.0800,"name":"NGC3706","t":"Ga"},{"RA":185.9911,"DE":16.6934,"AM":11.0800,"name":"NGC4350","t":"Ga"},{"RA":192.0568,"DE":-3.3327,"AM":11.0800,"name":"NGC4691","t":"Ga"},{"RA":26.9772,"DE":27.4328,"AM":11.0900,"name":"NGC0672","t":"Ga"},{"RA":266.7870,"DE":-64.6418,"AM":11.1000,"name":"IC4662","t":"Ga"},{"RA":179.8757,"DE":-19.2652,"AM":11.1000,"name":"NGC4027","t":"Ga"},{"RA":301.8312,"DE":-48.3702,"AM":11.1000,"name":"NGC6861","t":"Ga"},{"RA":341.8229,"DE":-65.0597,"AM":11.1100,"name":"IC5250A","t":"Ga"},{"RA":319.1349,"DE":-48.3636,"AM":11.1100,"name":"NGC7041","t":"Ga"},{"RA":189.1124,"DE":11.4393,"AM":11.1200,"name":"NGC4564","t":"Ga"},{"RA":200.0740,"DE":-24.4401,"AM":11.1200,"name":"NGC5085","t":"Ga"},{"RA":8.5645,"DE":-27.8036,"AM":11.1300,"name":"NGC0150","t":"Ga"},{"RA":170.4295,"DE":20.1696,"AM":11.1300,"name":"NGC3646","t":"Ga"},{"RA":205.7588,"DE":-48.1694,"AM":11.1400,"name":"NGC5266","t":"Ga"},{"RA":209.4610,"DE":-43.9313,"AM":11.1400,"name":"NGC5365","t":"Ga"},{"RA":237.8551,"DE":62.3100,"AM":11.1400,"name":"NGC6015","t":"Ga"},{"RA":154.5235,"DE":21.8323,"AM":11.1500,"name":"NGC3189","t":"Ga"},{"RA":14.4537,"DE":30.3524,"AM":11.1600,"name":"NGC0315","t":"Ga"},{"RA":25.7600,"DE":13.6451,"AM":11.1600,"name":"NGC0660","t":"Ga"},{"RA":186.7352,"DE":15.0474,"AM":11.1600,"name":"NGC4419","t":"Ga"},{"RA":183.0720,"DE":13.2052,"AM":11.1800,"name":"NGC4168","t":"Ga"},{"RA":187.2625,"DE":13.1837,"AM":11.1900,"name":"NGC4461","t":"Ga"},{"RA":189.1427,"DE":11.2389,"AM":11.1900,"name":"NGC4568","t":"Ga"},{"RA":86.7579,"DE":-34.2506,"AM":11.2000,"name":"NGC2090","t":"Ga"},{"RA":180.3615,"DE":61.8958,"AM":11.2000,"name":"NGC4036","t":"Ga"},{"RA":217.4183,"DE":3.2333,"AM":11.2000,"name":"NGC5638","t":"Ga"},{"RA":220.0480,"DE":0.2890,"AM":11.2000,"name":"NGC5713","t":"Ga"},{"RA":226.5034,"DE":1.6338,"AM":11.2000,"name":"NGC5845","t":"Ga"},{"RA":302.0812,"DE":-48.2114,"AM":11.2000,"name":"NGC6861D","t":"Ga"},{"RA":330.6659,"DE":-20.8128,"AM":11.2000,"name":"NGC7184","t":"Ga"},{"RA":181.0160,"DE":31.8958,"AM":11.2100,"name":"NGC4062","t":"Ga"},{"RA":331.7090,"DE":-64.3162,"AM":11.2100,"name":"NGC7192","t":"Ga"},{"RA":214.9508,"DE":56.7291,"AM":11.2200,"name":"NGC5585","t":"Ga"},{"RA":295.8927,"DE":-58.6556,"AM":11.2200,"name":"NGC6810","t":"Ga"},{"RA":54.1924,"DE":-35.9994,"AM":11.2300,"name":"NGC1386","t":"Ga"},{"RA":190.6976,"DE":11.4425,"AM":11.2300,"name":"NGC4638","t":"Ga"},{"RA":328.3343,"DE":-47.8824,"AM":11.2300,"name":"NGC7145","t":"Ga"},{"RA":147.5340,"DE":-73.9222,"AM":11.2400,"name":"NGC3059","t":"Ga"},{"RA":23.7693,"DE":-41.4362,"AM":11.2500,"name":"NGC0625","t":"Ga"},{"RA":311.1406,"DE":-68.7477,"AM":11.2500,"name":"NGC6943","t":"Ga"},{"RA":113.7132,"DE":-69.2841,"AM":11.2600,"name":"NGC2434","t":"Ga"},{"RA":348.7021,"DE":-43.5999,"AM":11.2600,"name":"NGC7531","t":"Ga"},{"RA":284.1237,"DE":-54.3058,"AM":11.2700,"name":"IC4797","t":"Ga"},{"RA":352.1810,"DE":-41.3335,"AM":11.2700,"name":"IC5325","t":"Ga"},{"RA":252.7784,"DE":-58.9935,"AM":11.2800,"name":"NGC6215","t":"Ga"},{"RA":190.2300,"DE":-40.9764,"AM":11.3000,"name":"NGC4603","t":"Ga"},{"RA":195.0339,"DE":27.9770,"AM":11.3000,"name":"NGC4889","t":"Ga"},{"RA":306.2776,"DE":-24.8092,"AM":11.3000,"name":"NGC6907","t":"Ga"},{"RA":308.5857,"DE":-31.9809,"AM":11.3000,"name":"NGC6925","t":"Ga"},{"RA":359.7490,"DE":-55.4583,"AM":11.3000,"name":"NGC7796","t":"Ga"},{"RA":340.4683,"DE":-44.7672,"AM":11.3100,"name":"IC5240","t":"Ga"},{"RA":32.0881,"DE":10.9949,"AM":11.3100,"name":"NGC0821","t":"Ga"},{"RA":184.1138,"DE":-43.3242,"AM":11.3100,"name":"NGC4219","t":"Ga"},{"RA":189.1363,"DE":11.2580,"AM":11.3100,"name":"NGC4567","t":"Ga"},{"RA":340.1009,"DE":-66.4790,"AM":11.3100,"name":"NGC7329","t":"Ga"},{"RA":355.9765,"DE":26.0756,"AM":11.3100,"name":"NGC7741","t":"Ga"},{"RA":182.3741,"DE":43.6853,"AM":11.3200,"name":"NGC4138","t":"Ga"},{"RA":192.5162,"DE":-41.3820,"AM":11.3200,"name":"NGC4709","t":"Ga"},{"RA":56.3212,"DE":76.6383,"AM":11.3300,"name":"IC0334","t":"Ga"},{"RA":156.9636,"DE":-43.9038,"AM":11.3300,"name":"NGC3256","t":"Ga"},{"RA":198.2161,"DE":-43.0962,"AM":11.3300,"name":"NGC5011","t":"Ga"},{"RA":210.9114,"DE":-33.9783,"AM":11.3300,"name":"NGC5419","t":"Ga"},{"RA":39.6363,"DE":-6.6774,"AM":11.3400,"name":"NGC1022","t":"Ga"},{"RA":185.3865,"DE":14.6062,"AM":11.3400,"name":"NGC4298","t":"Ga"},{"RA":223.4900,"DE":3.5444,"AM":11.3400,"name":"NGC5775","t":"Ga"},{"RA":234.1320,"DE":16.6078,"AM":11.3400,"name":"NGC5962","t":"Ga"},{"RA":281.8285,"DE":45.5506,"AM":11.3400,"name":"NGC6703","t":"Ga"},{"RA":53.0126,"DE":-20.8192,"AM":11.3500,"name":"NGC1353","t":"Ga"},{"RA":160.6940,"DE":-36.3527,"AM":11.3500,"name":"NGC3347","t":"Ga"},{"RA":181.6867,"DE":-29.7683,"AM":11.3500,"name":"NGC4106","t":"Ga"},{"RA":182.7682,"DE":50.4847,"AM":11.3500,"name":"NGC4157","t":"Ga"},{"RA":356.2468,"DE":-42.9109,"AM":11.3500,"name":"NGC7744","t":"Ga"},{"RA":281.8247,"DE":-63.3313,"AM":11.3600,"name":"IC4765","t":"Ga"},{"RA":356.9657,"DE":-30.5220,"AM":11.3600,"name":"NGC7755","t":"Ga"},{"RA":40.9348,"DE":-29.0034,"AM":11.3700,"name":"NGC1079","t":"Ga"},{"RA":326.0672,"DE":-75.1113,"AM":11.3700,"name":"NGC7098","t":"Ga"},{"RA":212.6043,"DE":-43.3246,"AM":11.3800,"name":"NGC5483","t":"Ga"},{"RA":343.9406,"DE":-42.6420,"AM":11.3800,"name":"NGC7412","t":"Ga"},{"RA":112.2278,"DE":69.2158,"AM":11.3900,"name":"NGC2366","t":"Ga"},{"RA":344.1507,"DE":-37.0301,"AM":11.3900,"name":"NGC7418","t":"Ga"},{"RA":194.8988,"DE":27.9593,"AM":11.4000,"name":"NGC4874","t":"Ga"},{"RA":74.9908,"DE":-26.0222,"AM":11.4100,"name":"NGC1744","t":"Ga"},{"RA":201.1900,"DE":-37.6822,"AM":11.4100,"name":"NGC5121","t":"Ga"},{"RA":349.8381,"DE":-42.2568,"AM":11.4100,"name":"NGC7599","t":"Ga"},{"RA":21.1437,"DE":3.7949,"AM":11.4200,"name":"NGC0520 NED01","t":"Ga"},{"RA":32.4289,"DE":-10.1841,"AM":11.4200,"name":"NGC0839","t":"Ga"},{"RA":312.1775,"DE":-37.9974,"AM":11.4200,"name":"NGC6958","t":"Ga"},{"RA":140.8759,"DE":-23.1614,"AM":11.4300,"name":"NGC2865","t":"Ga"},{"RA":55.7046,"DE":-22.1084,"AM":11.4400,"name":"NGC1426","t":"Ga"},{"RA":344.8612,"DE":-37.7029,"AM":11.4500,"name":"IC5273","t":"Ga"},{"RA":30.0621,"DE":31.4296,"AM":11.4500,"name":"NGC0777","t":"Ga"},{"RA":187.5726,"DE":12.3286,"AM":11.4500,"name":"NGC4478","t":"Ga"},{"RA":267.9534,"DE":23.0719,"AM":11.4500,"name":"NGC6482","t":"Ga"},{"RA":305.2068,"DE":-48.2391,"AM":11.4500,"name":"NGC6893","t":"Ga"},{"RA":209.0695,"DE":47.2357,"AM":11.4600,"name":"NGC5377","t":"Ga"},{"RA":17.7454,"DE":33.1519,"AM":11.4800,"name":"NGC0410","t":"Ga"},{"RA":182.6358,"DE":39.4057,"AM":11.4800,"name":"NGC4151","t":"Ga"},{"RA":229.6522,"DE":-24.0686,"AM":11.4800,"name":"NGC5903","t":"Ga"},{"RA":317.8337,"DE":-64.0253,"AM":11.4800,"name":"NGC7020","t":"Ga"},{"RA":168.7759,"DE":14.7870,"AM":11.4900,"name":"NGC3596","t":"Ga"},{"RA":54.1320,"DE":-35.2952,"AM":11.5000,"name":"NGC1381","t":"Ga"},{"RA":54.2991,"DE":-35.7456,"AM":11.5000,"name":"NGC1389","t":"Ga"},{"RA":161.6456,"DE":13.7509,"AM":11.5000,"name":"NGC3367","t":"Ga"},{"RA":20.0279,"DE":3.4154,"AM":11.5100,"name":"NGC0474","t":"Ga"},{"RA":200.3034,"DE":-43.7046,"AM":11.5100,"name":"NGC5090","t":"Ga"},{"RA":229.5565,"DE":-24.0979,"AM":11.5200,"name":"NGC5898","t":"Ga"},{"RA":160.8876,"DE":-36.4107,"AM":11.5300,"name":"NGC3358","t":"Ga"},{"RA":193.4706,"DE":-39.7143,"AM":11.5300,"name":"NGC4767","t":"Ga"},{"RA":207.2721,"DE":-30.2959,"AM":11.5400,"name":"IC4329","t":"Ga"},{"RA":321.0917,"DE":-40.5377,"AM":11.5400,"name":"IC5105","t":"Ga"},{"RA":187.3384,"DE":-23.1664,"AM":11.5400,"name":"NGC4462","t":"Ga"},{"RA":304.5798,"DE":-70.8588,"AM":11.5400,"name":"NGC6876","t":"Ga"},{"RA":331.4784,"DE":-50.1193,"AM":11.5400,"name":"NGC7196","t":"Ga"},{"RA":217.9109,"DE":-43.4184,"AM":11.5500,"name":"IC4441","t":"Ga"},{"RA":51.1065,"DE":-21.5440,"AM":11.5500,"name":"NGC1325","t":"Ga"},{"RA":149.7861,"DE":-34.2252,"AM":11.5500,"name":"NGC3087","t":"Ga"},{"RA":184.8774,"DE":14.8777,"AM":11.5500,"name":"NGC4262","t":"Ga"},{"RA":288.4681,"DE":-56.3099,"AM":11.5600,"name":"NGC6758","t":"Ga"},{"RA":290.0937,"DE":-60.3892,"AM":11.5700,"name":"IC4845","t":"Ga"},{"RA":186.6947,"DE":7.9190,"AM":11.5700,"name":"NGC4416","t":"Ga"},{"RA":2.4856,"DE":-24.9631,"AM":11.5800,"name":"NGC0024","t":"Ga"},{"RA":114.1174,"DE":-47.6356,"AM":11.5800,"name":"NGC2427","t":"Ga"},{"RA":150.0243,"DE":-31.5529,"AM":11.5800,"name":"NGC3095","t":"Ga"},{"RA":325.3303,"DE":-63.9087,"AM":11.5800,"name":"NGC7096","t":"Ga"},{"RA":8.5116,"DE":-9.7053,"AM":11.5900,"name":"NGC0151","t":"Ga"},{"RA":304.2357,"DE":-70.7679,"AM":11.5900,"name":"NGC6872","t":"Ga"},{"RA":194.1801,"DE":-50.3469,"AM":11.6000,"name":"IC3896","t":"Ga"},{"RA":147.8144,"DE":-32.7526,"AM":11.6000,"name":"NGC3038","t":"Ga"},{"RA":157.3331,"DE":29.4918,"AM":11.6000,"name":"NGC3254","t":"Ga"},{"RA":186.7606,"DE":15.4615,"AM":11.6000,"name":"NGC4421","t":"Ga"},{"RA":14.9587,"DE":-7.5780,"AM":11.6100,"name":"NGC0337","t":"Ga"},{"RA":185.4270,"DE":14.5983,"AM":11.6100,"name":"NGC4302","t":"Ga"},{"RA":199.7497,"DE":-47.9087,"AM":11.6100,"name":"NGC5064","t":"Ga"},{"RA":275.5728,"DE":-85.4021,"AM":11.6100,"name":"NGC6438","t":"Ga"},{"RA":323.1469,"DE":-44.0676,"AM":11.6100,"name":"NGC7079","t":"Ga"},{"RA":185.9384,"DE":-34.6222,"AM":11.6200,"name":"IC3253","t":"Ga"},{"RA":35.5042,"DE":33.2661,"AM":11.6200,"name":"NGC0890","t":"Ga"},{"RA":120.4717,"DE":50.7371,"AM":11.6200,"name":"NGC2500","t":"Ga"},{"RA":171.1820,"DE":38.7629,"AM":11.6200,"name":"NGC3665","t":"Ga"},{"RA":178.2307,"DE":36.9863,"AM":11.6200,"name":"NGC3941","t":"Ga"},{"RA":278.6032,"DE":-58.4966,"AM":11.6300,"name":"IC4721","t":"Ga"},{"RA":12.4492,"DE":32.2777,"AM":11.6300,"name":"NGC0266","t":"Ga"},{"RA":138.5213,"DE":40.1137,"AM":11.6300,"name":"NGC2782","t":"Ga"},{"RA":182.6402,"DE":30.4015,"AM":11.6400,"name":"NGC4150","t":"Ga"},{"RA":199.4279,"DE":-32.1017,"AM":11.6500,"name":"IC4214","t":"Ga"},{"RA":21.0162,"DE":12.9174,"AM":11.6500,"name":"NGC0514","t":"Ga"},{"RA":130.9087,"DE":50.2056,"AM":11.6500,"name":"NGC2639","t":"Ga"},{"RA":250.7656,"DE":36.8324,"AM":11.6500,"name":"NGC6207","t":"Ga"},{"RA":313.0232,"DE":-69.2016,"AM":11.6600,"name":"IC5052","t":"Ga"},{"RA":28.3054,"DE":4.1958,"AM":11.6700,"name":"NGC0718","t":"Ga"},{"RA":163.1297,"DE":36.6188,"AM":11.6700,"name":"NGC3432","t":"Ga"},{"RA":300.8932,"DE":-48.2845,"AM":11.6700,"name":"NGC6851","t":"Ga"},{"RA":58.9465,"DE":-42.3686,"AM":11.6800,"name":"NGC1487 NED02","t":"Ga"},{"RA":145.9213,"DE":-20.4772,"AM":11.6800,"name":"NGC2983","t":"Ga"},{"RA":158.2310,"DE":28.5117,"AM":11.6800,"name":"NGC3277","t":"Ga"},{"RA":188.8774,"DE":12.2208,"AM":11.6800,"name":"NGC4550","t":"Ga"},{"RA":191.0416,"DE":-41.7499,"AM":11.6800,"name":"NGC4645","t":"Ga"},{"RA":333.3404,"DE":-46.0176,"AM":11.6900,"name":"IC5181","t":"Ga"},{"RA":123.3110,"DE":45.9898,"AM":11.6900,"name":"NGC2537","t":"Ga"},{"RA":138.0605,"DE":44.9548,"AM":11.6900,"name":"NGC2776","t":"Ga"},{"RA":179.1172,"DE":55.1253,"AM":11.7000,"name":"NGC3982","t":"Ga"},{"RA":225.0017,"DE":1.8913,"AM":11.7000,"name":"NGC5806","t":"Ga"},{"RA":90.2825,"DE":-23.6726,"AM":11.7100,"name":"NGC2139","t":"Ga"},{"RA":325.0538,"DE":-42.5394,"AM":11.7100,"name":"NGC7097","t":"Ga"},{"RA":70.5605,"DE":-20.4348,"AM":11.7200,"name":"NGC1640","t":"Ga"},{"RA":157.2232,"DE":-35.6055,"AM":11.7200,"name":"NGC3258","t":"Ga"},{"RA":185.6307,"DE":15.5379,"AM":11.7200,"name":"NGC4312","t":"Ga"},{"RA":186.3114,"DE":15.6075,"AM":11.7200,"name":"NGC4379","t":"Ga"},{"RA":186.9732,"DE":12.2933,"AM":11.7200,"name":"NGC4440","t":"Ga"},{"RA":17.3626,"DE":35.7181,"AM":11.7300,"name":"NGC0404","t":"Ga"},{"RA":35.4020,"DE":-5.5214,"AM":11.7300,"name":"NGC0895","t":"Ga"},{"RA":157.6104,"DE":-35.3595,"AM":11.7300,"name":"NGC3271","t":"Ga"},{"RA":44.9263,"DE":25.2378,"AM":11.7400,"name":"NGC1156","t":"Ga"},{"RA":183.4470,"DE":13.4248,"AM":11.7400,"name":"NGC4189","t":"Ga"},{"RA":194.5327,"DE":-46.2642,"AM":11.7400,"name":"NGC4835","t":"Ga"},{"RA":40.8750,"DE":37.3413,"AM":11.7500,"name":"NGC1058","t":"Ga"},{"RA":289.5945,"DE":-60.5011,"AM":11.7500,"name":"NGC6769","t":"Ga"},{"RA":103.4748,"DE":-40.8626,"AM":11.7600,"name":"NGC2310","t":"Ga"},{"RA":302.5452,"DE":-48.2871,"AM":11.7600,"name":"NGC6870","t":"Ga"},{"RA":304.3220,"DE":-52.7968,"AM":11.7600,"name":"NGC6887","t":"Ga"},{"RA":157.5028,"DE":-35.3255,"AM":11.7700,"name":"NGC3268","t":"Ga"},{"RA":19.9369,"DE":3.4099,"AM":11.7800,"name":"NGC0470","t":"Ga"},{"RA":159.1488,"DE":-27.5184,"AM":11.7800,"name":"NGC3309","t":"Ga"},{"RA":247.1603,"DE":39.5516,"AM":11.7800,"name":"NGC6166","t":"Ga"},{"RA":303.3020,"DE":-46.1616,"AM":11.7800,"name":"NGC6875","t":"Ga"},{"RA":305.9920,"DE":-43.9953,"AM":11.7900,"name":"IC4946","t":"Ga"},{"RA":139.8275,"DE":69.2032,"AM":11.7900,"name":"NGC2787","t":"Ga"},{"RA":155.8774,"DE":19.8651,"AM":11.7900,"name":"NGC3227","t":"Ga"},{"RA":333.9083,"DE":-45.8501,"AM":11.7900,"name":"NGC7232","t":"Ga"},{"RA":334.6938,"DE":-36.8016,"AM":11.8000,"name":"IC5186","t":"Ga"},{"RA":123.6672,"DE":49.0617,"AM":11.8000,"name":"NGC2541","t":"Ga"},{"RA":343.7540,"DE":-39.6613,"AM":11.8000,"name":"NGC7410","t":"Ga"},{"RA":207.1825,"DE":-30.2175,"AM":11.8100,"name":"IC4327","t":"Ga"},{"RA":40.8127,"DE":32.4250,"AM":11.8100,"name":"NGC1060","t":"Ga"},{"RA":317.9669,"DE":-49.2837,"AM":11.8100,"name":"NGC7029","t":"Ga"},{"RA":11.8650,"DE":-31.4217,"AM":11.8200,"name":"NGC0254","t":"Ga"},{"RA":92.5397,"DE":-34.1062,"AM":11.8200,"name":"NGC2188","t":"Ga"},{"RA":130.6658,"DE":14.2856,"AM":11.8200,"name":"NGC2648","t":"Ga"},{"RA":176.0090,"DE":19.9498,"AM":11.8200,"name":"NGC3842","t":"Ga"},{"RA":234.4009,"DE":5.9740,"AM":11.8200,"name":"NGC5964","t":"Ga"},{"RA":146.5778,"DE":-30.4375,"AM":11.8300,"name":"NGC3001","t":"Ga"},{"RA":186.8055,"DE":12.7347,"AM":11.8300,"name":"NGC4425","t":"Ga"},{"RA":329.0405,"DE":-49.5219,"AM":11.8300,"name":"NGC7155","t":"Ga"},{"RA":61.7072,"DE":-21.1726,"AM":11.8400,"name":"NGC1518","t":"Ga"},{"RA":139.0823,"DE":-23.6333,"AM":11.8400,"name":"NGC2815","t":"Ga"},{"RA":190.7076,"DE":2.6878,"AM":11.8400,"name":"NGC4636","t":"Ga"},{"RA":290.9913,"DE":-59.9225,"AM":11.8400,"name":"NGC6782","t":"Ga"},{"RA":330.1372,"DE":-43.3897,"AM":11.8400,"name":"NGC7166","t":"Ga"},{"RA":344.2942,"DE":-36.4622,"AM":11.8500,"name":"IC1459","t":"Ga"},{"RA":19.7922,"DE":3.3008,"AM":11.8500,"name":"NGC0467","t":"Ga"},{"RA":202.8678,"DE":-34.7944,"AM":11.8500,"name":"NGC5188","t":"Ga"},{"RA":342.9531,"DE":-20.6081,"AM":11.8500,"name":"NGC7392","t":"Ga"},{"RA":330.5308,"DE":-51.7431,"AM":11.8600,"name":"NGC7168","t":"Ga"},{"RA":187.2115,"DE":-1.9392,"AM":11.8700,"name":"NGC4454","t":"Ga"},{"RA":345.2497,"DE":30.1449,"AM":11.8700,"name":"NGC7457","t":"Ga"},{"RA":100.6721,"DE":-27.4595,"AM":11.8800,"name":"NGC2272","t":"Ga"},{"RA":134.2470,"DE":51.3474,"AM":11.8800,"name":"NGC2693","t":"Ga"},{"RA":306.9120,"DE":-47.0270,"AM":11.8800,"name":"NGC6909","t":"Ga"},{"RA":334.0379,"DE":-36.8437,"AM":11.8900,"name":"IC5179","t":"Ga"},{"RA":176.6937,"DE":-27.9222,"AM":11.8900,"name":"NGC3885","t":"Ga"},{"RA":196.3342,"DE":-35.3374,"AM":11.8900,"name":"NGC4947","t":"Ga"},{"RA":170.7276,"DE":16.5900,"AM":11.9000,"name":"NGC3655","t":"Ga"},{"RA":178.4881,"DE":-23.1642,"AM":11.9000,"name":"NGC3955","t":"Ga"},{"RA":191.8760,"DE":-39.5709,"AM":11.9000,"name":"NGC4679","t":"Ga"},{"RA":191.0816,"DE":-40.7318,"AM":11.9100,"name":"NGC4650","t":"Ga"},{"RA":351.2057,"DE":15.2756,"AM":11.9100,"name":"NGC7653","t":"Ga"},{"RA":202.9730,"DE":-33.2342,"AM":11.9200,"name":"NGC5193","t":"Ga"},{"RA":331.9683,"DE":31.3593,"AM":11.9200,"name":"NGC7217","t":"Ga"},{"RA":95.4157,"DE":-27.2338,"AM":11.9300,"name":"NGC2217","t":"Ga"},{"RA":187.6297,"DE":41.7012,"AM":11.9300,"name":"NGC4485","t":"Ga"},{"RA":193.6693,"DE":28.9387,"AM":11.9300,"name":"NGC4793","t":"Ga"},{"RA":208.9164,"DE":40.4618,"AM":11.9300,"name":"NGC5371","t":"Ga"},{"RA":344.2264,"DE":-37.3473,"AM":11.9300,"name":"NGC7421","t":"Ga"},{"RA":289.6555,"DE":-60.4965,"AM":11.9400,"name":"NGC6770","t":"Ga"},{"RA":0.9955,"DE":20.7523,"AM":11.9400,"name":"NGC7817","t":"Ga"},{"RA":163.1490,"DE":22.9341,"AM":11.9600,"name":"NGC3437","t":"Ga"},{"RA":37.6381,"DE":-1.1084,"AM":11.9700,"name":"NGC0955","t":"Ga"},{"RA":159.3146,"DE":-41.6276,"AM":11.9700,"name":"NGC3318","t":"Ga"},{"RA":158.8837,"DE":-41.7409,"AM":11.9700,"name":"NGC3318A","t":"Ga"},{"RA":181.9048,"DE":2.6905,"AM":11.9700,"name":"NGC4116","t":"Ga"},{"RA":26.8745,"DE":27.3334,"AM":11.9800,"name":"IC1727","t":"Ga"},{"RA":37.7027,"DE":37.1368,"AM":11.9800,"name":"NGC0949","t":"Ga"},{"RA":187.1805,"DE":11.7550,"AM":11.9800,"name":"NGC4452","t":"Ga"},{"RA":350.1255,"DE":17.2256,"AM":11.9800,"name":"NGC7625","t":"Ga"},{"RA":47.8110,"DE":-8.9221,"AM":11.9900,"name":"NGC1241","t":"Ga"},{"RA":183.7711,"DE":33.1973,"AM":11.9900,"name":"NGC4203","t":"Ga"},{"RA":202.1837,"DE":-48.9168,"AM":11.9900,"name":"NGC5156","t":"Ga"},{"RA":291.3298,"DE":-63.8602,"AM":11.9900,"name":"NGC6776","t":"Ga"},{"RA":27.2388,"DE":5.9075,"AM":12.0000,"name":"NGC0676","t":"Ga"},{"RA":196.0220,"DE":-41.4116,"AM":12.0000,"name":"NGC4930","t":"Ga"},{"RA":283.0085,"DE":-57.3207,"AM":12.0000,"name":"NGC6699","t":"Ga"},{"RA":96.7318,"DE":59.0801,"AM":12.0100,"name":"IC2166","t":"Ga"},{"RA":138.4572,"DE":-69.6448,"AM":12.0100,"name":"NGC2822","t":"Ga"},{"RA":353.2607,"DE":-51.6984,"AM":12.0100,"name":"NGC7690","t":"Ga"},{"RA":54.6608,"DE":-18.4280,"AM":12.0200,"name":"NGC1393","t":"Ga"},{"RA":185.5530,"DE":-33.4845,"AM":12.0200,"name":"NGC4304","t":"Ga"},{"RA":188.9081,"DE":12.2640,"AM":12.0200,"name":"NGC4551","t":"Ga"},{"RA":213.1008,"DE":-30.6441,"AM":12.0200,"name":"NGC5494","t":"Ga"},{"RA":198.3645,"DE":36.5939,"AM":12.0300,"name":"NGC5033","t":"Ga"},{"RA":173.9533,"DE":54.5239,"AM":12.0400,"name":"NGC3738","t":"Ga"},{"RA":285.2117,"DE":-57.7594,"AM":12.0400,"name":"NGC6721","t":"Ga"},{"RA":316.3663,"DE":-52.5520,"AM":12.0400,"name":"NGC7007","t":"Ga"},{"RA":143.7400,"DE":21.7053,"AM":12.0500,"name":"NGC2916","t":"Ga"},{"RA":2.2679,"DE":27.7294,"AM":12.0600,"name":"NGC0016","t":"Ga"},{"RA":142.9030,"DE":-16.7347,"AM":12.0600,"name":"NGC2907","t":"Ga"},{"RA":188.5253,"DE":11.3212,"AM":12.0600,"name":"NGC4528","t":"Ga"},{"RA":194.3515,"DE":27.4978,"AM":12.0600,"name":"NGC4839","t":"Ga"},{"RA":335.1865,"DE":-24.6783,"AM":12.0600,"name":"NGC7252","t":"Ga"},{"RA":349.4964,"DE":9.6802,"AM":12.0600,"name":"NGC7587","t":"Ga"},{"RA":30.3205,"DE":28.8373,"AM":12.0700,"name":"NGC0784","t":"Ga"},{"RA":185.0869,"DE":29.3109,"AM":12.0700,"name":"NGC4283","t":"Ga"},{"RA":187.2399,"DE":13.2419,"AM":12.0700,"name":"NGC4458","t":"Ga"},{"RA":21.4346,"DE":-1.3796,"AM":12.0800,"name":"NGC0541","t":"Ga"},{"RA":45.3089,"DE":44.8973,"AM":12.0800,"name":"NGC1161","t":"Ga"},{"RA":50.2643,"DE":-37.1017,"AM":12.0800,"name":"NGC1310","t":"Ga"},{"RA":158.3993,"DE":-27.4544,"AM":12.0800,"name":"NGC3285","t":"Ga"},{"RA":182.4002,"DE":42.5342,"AM":12.0800,"name":"NGC4143","t":"Ga"},{"RA":200.1040,"DE":-20.6110,"AM":12.0800,"name":"NGC5087","t":"Ga"},{"RA":209.2333,"DE":29.1644,"AM":12.0800,"name":"NGC5375","t":"Ga"},{"RA":332.3180,"DE":-47.1666,"AM":12.0800,"name":"NGC7213","t":"Ga"},{"RA":150.9662,"DE":-27.5709,"AM":12.0900,"name":"IC2537","t":"Ga"},{"RA":193.3639,"DE":-48.7492,"AM":12.0900,"name":"NGC4785","t":"Ga"},{"RA":307.9128,"DE":-30.8319,"AM":12.0900,"name":"NGC6923","t":"Ga"},{"RA":10.3912,"DE":-10.0214,"AM":12.1000,"name":"NGC0217","t":"Ga"},{"RA":162.4588,"DE":32.9829,"AM":12.1000,"name":"NGC3395","t":"Ga"},{"RA":179.4839,"DE":55.4536,"AM":12.1000,"name":"NGC3998","t":"Ga"},{"RA":193.5793,"DE":27.0680,"AM":12.1000,"name":"NGC4789","t":"Ga"},{"RA":309.5842,"DE":-52.1104,"AM":12.1000,"name":"NGC6935","t":"Ga"},{"RA":310.1577,"DE":-54.3031,"AM":12.1000,"name":"NGC6942","t":"Ga"},{"RA":49.3050,"DE":-32.5759,"AM":12.1100,"name":"NGC1288","t":"Ga"},{"RA":126.2095,"DE":73.4120,"AM":12.1100,"name":"NGC2551","t":"Ga"},{"RA":186.9055,"DE":-39.3378,"AM":12.1200,"name":"IC3370","t":"Ga"},{"RA":8.5646,"DE":-31.7860,"AM":12.1200,"name":"NGC0148","t":"Ga"},{"RA":186.3563,"DE":16.4701,"AM":12.1200,"name":"NGC4383","t":"Ga"},{"RA":186.4237,"DE":12.8105,"AM":12.1200,"name":"NGC4387","t":"Ga"},{"RA":332.8135,"DE":-30.5632,"AM":12.1300,"name":"NGC7221","t":"Ga"},{"RA":16.8540,"DE":32.4126,"AM":12.1400,"name":"NGC0383","t":"Ga"},{"RA":108.1194,"DE":47.1667,"AM":12.1400,"name":"NGC2344","t":"Ga"},{"RA":218.5052,"DE":-78.3875,"AM":12.1400,"name":"NGC5612","t":"Ga"},{"RA":311.8294,"DE":0.3208,"AM":12.1400,"name":"NGC6962","t":"Ga"},{"RA":354.0922,"DE":2.1565,"AM":12.1400,"name":"NGC7715","t":"Ga"},{"RA":58.6623,"DE":-20.5027,"AM":12.1500,"name":"NGC1482","t":"Ga"},{"RA":107.3253,"DE":20.6360,"AM":12.1500,"name":"NGC2342","t":"Ga"},{"RA":159.6911,"DE":53.5034,"AM":12.1500,"name":"NGC3310","t":"Ga"},{"RA":183.8200,"DE":13.0240,"AM":12.1500,"name":"NGC4206","t":"Ga"},{"RA":330.5269,"DE":-31.9930,"AM":12.1500,"name":"NGC7174","t":"Ga"},{"RA":178.6671,"DE":-13.9750,"AM":12.1600,"name":"NGC3962","t":"Ga"},{"RA":300.2434,"DE":-47.0703,"AM":12.1600,"name":"NGC6845A","t":"Ga"},{"RA":179.7175,"DE":42.7225,"AM":12.1700,"name":"IC0750","t":"Ga"},{"RA":330.8120,"DE":-33.8384,"AM":12.1700,"name":"IC5156","t":"Ga"},{"RA":15.3912,"DE":-7.5883,"AM":12.1700,"name":"NGC0337A","t":"Ga"},{"RA":154.4107,"DE":21.6883,"AM":12.1700,"name":"NGC3185","t":"Ga"},{"RA":187.4448,"DE":8.0005,"AM":12.1700,"name":"M49","t":"Ga"},{"RA":146.4252,"DE":-14.3264,"AM":12.1800,"name":"NGC2992","t":"Ga"},{"RA":49.1876,"DE":80.7933,"AM":12.1900,"name":"NGC1184","t":"Ga"},{"RA":160.0709,"DE":-27.7771,"AM":12.1900,"name":"NGC3336","t":"Ga"},{"RA":187.4962,"DE":12.3487,"AM":12.1900,"name":"NGC4476","t":"Ga"},{"RA":226.3645,"DE":1.6348,"AM":12.1900,"name":"NGC5839","t":"Ga"},{"RA":207.2070,"DE":-30.5111,"AM":12.2000,"name":"NGC5302","t":"Ga"},{"RA":36.2684,"DE":-24.7882,"AM":12.2100,"name":"NGC0922","t":"Ga"},{"RA":167.3839,"DE":-37.3496,"AM":12.2100,"name":"NGC3557B","t":"Ga"},{"RA":167.6516,"DE":-37.5476,"AM":12.2100,"name":"NGC3564","t":"Ga"},{"RA":185.3186,"DE":4.5957,"AM":12.2100,"name":"NGC4292","t":"Ga"},{"RA":200.0705,"DE":-21.8276,"AM":12.2100,"name":"NGC5084","t":"Ga"},{"RA":8.9461,"DE":-25.3744,"AM":12.2200,"name":"IC1558","t":"Ga"},{"RA":211.7973,"DE":55.0017,"AM":12.2200,"name":"NGC5485","t":"Ga"},{"RA":327.0225,"DE":-50.5652,"AM":12.2200,"name":"NGC7124","t":"Ga"},{"RA":353.8703,"DE":-56.0123,"AM":12.2200,"name":"NGC7702","t":"Ga"},{"RA":288.8110,"DE":-54.6614,"AM":12.2300,"name":"IC4837","t":"Ga"},{"RA":119.5853,"DE":25.1492,"AM":12.2300,"name":"NGC2487","t":"Ga"},{"RA":140.3645,"DE":-11.9095,"AM":12.2300,"name":"NGC2855","t":"Ga"},{"RA":196.0704,"DE":-30.5263,"AM":12.2300,"name":"NGC4936","t":"Ga"},{"RA":196.0548,"DE":-5.5516,"AM":12.2300,"name":"NGC4941","t":"Ga"},{"RA":300.8710,"DE":-54.9799,"AM":12.2400,"name":"IC4933","t":"Ga"},{"RA":186.6344,"DE":12.6110,"AM":12.2500,"name":"NGC4407","t":"Ga"},{"RA":316.9674,"DE":-47.1790,"AM":12.2500,"name":"NGC7014","t":"Ga"},{"RA":357.8534,"DE":20.1118,"AM":12.2500,"name":"NGC7771","t":"Ga"},{"RA":223.3126,"DE":3.9597,"AM":12.2600,"name":"NGC5770","t":"Ga"},{"RA":224.4405,"DE":71.6823,"AM":12.2600,"name":"NGC5832","t":"Ga"},{"RA":141.1572,"DE":49.3571,"AM":12.2700,"name":"NGC2857","t":"Ga"},{"RA":192.0955,"DE":8.4874,"AM":12.2700,"name":"NGC4698","t":"Ga"},{"RA":156.3702,"DE":-39.8276,"AM":12.2800,"name":"NGC3244","t":"Ga"},{"RA":289.8520,"DE":-60.6442,"AM":12.2900,"name":"IC4842","t":"Ga"},{"RA":322.6056,"DE":-43.0871,"AM":12.2900,"name":"NGC7070","t":"Ga"},{"RA":20.7979,"DE":33.4606,"AM":12.3000,"name":"NGC0499","t":"Ga"},{"RA":301.4117,"DE":-54.3756,"AM":12.3000,"name":"NGC6854","t":"Ga"},{"RA":321.8395,"DE":-60.0146,"AM":12.3000,"name":"NGC7059","t":"Ga"},{"RA":357.7249,"DE":-40.7282,"AM":12.3000,"name":"NGC7764","t":"Ga"},{"RA":183.4733,"DE":13.1729,"AM":12.3100,"name":"NGC4193","t":"Ga"},{"RA":139.3450,"DE":41.9997,"AM":12.3200,"name":"NGC2798","t":"Ga"},{"RA":194.7597,"DE":34.8594,"AM":12.3200,"name":"NGC4861","t":"Ga"},{"RA":131.2844,"DE":-33.7948,"AM":12.3300,"name":"NGC2663","t":"Ga"},{"RA":322.5081,"DE":26.7178,"AM":12.3300,"name":"NGC7080","t":"Ga"},{"RA":183.0782,"DE":29.1794,"AM":12.3400,"name":"NGC4169","t":"Ga"},{"RA":193.0817,"DE":-41.0600,"AM":12.3400,"name":"NGC4744","t":"Ga"},{"RA":345.8151,"DE":8.8740,"AM":12.3400,"name":"NGC7469","t":"Ga"},{"RA":190.4697,"DE":41.2740,"AM":12.3500,"name":"NGC4625","t":"Ga"},{"RA":328.8377,"DE":-34.8141,"AM":12.3500,"name":"NGC7154","t":"Ga"},{"RA":326.8555,"DE":-34.8837,"AM":12.3600,"name":"IC5131","t":"Ga"},{"RA":159.0933,"DE":-27.4381,"AM":12.3600,"name":"NGC3308","t":"Ga"},{"RA":327.3255,"DE":-60.6092,"AM":12.3600,"name":"NGC7126","t":"Ga"},{"RA":33.9582,"DE":-31.2010,"AM":12.3700,"name":"IC1788","t":"Ga"},{"RA":215.0187,"DE":3.9925,"AM":12.3700,"name":"NGC5560","t":"Ga"},{"RA":327.3166,"DE":-60.7132,"AM":12.3700,"name":"NGC7125","t":"Ga"},{"RA":359.8563,"DE":20.7499,"AM":12.3700,"name":"NGC7798","t":"Ga"},{"RA":38.0998,"DE":35.4946,"AM":12.3800,"name":"NGC0959","t":"Ga"},{"RA":125.1487,"DE":21.0678,"AM":12.3900,"name":"NGC2563","t":"Ga"},{"RA":205.4028,"DE":-29.9131,"AM":12.3900,"name":"NGC5264","t":"Ga"},{"RA":210.3398,"DE":-33.0638,"AM":12.3900,"name":"NGC5398","t":"Ga"},{"RA":215.2332,"DE":3.2380,"AM":12.3900,"name":"NGC5574","t":"Ga"},{"RA":263.1657,"DE":16.4018,"AM":12.3900,"name":"NGC6389","t":"Ga"},{"RA":322.9470,"DE":-42.8477,"AM":12.3900,"name":"NGC7070A","t":"Ga"},{"RA":334.2247,"DE":40.5023,"AM":12.3900,"name":"NGC7248","t":"Ga"},{"RA":53.8201,"DE":-35.2657,"AM":12.4000,"name":"NGC1375","t":"Ga"},{"RA":166.6979,"DE":72.5686,"AM":12.4000,"name":"NGC3516","t":"Ga"},{"RA":38.5342,"DE":32.9469,"AM":12.4100,"name":"NGC0969","t":"Ga"},{"RA":54.1979,"DE":-34.7397,"AM":12.4100,"name":"NGC1380A","t":"Ga"},{"RA":153.5627,"DE":3.4661,"AM":12.4100,"name":"NGC3169","t":"Ga"},{"RA":238.5581,"DE":14.6013,"AM":12.4200,"name":"NGC6012","t":"Ga"},{"RA":303.4718,"DE":-44.5267,"AM":12.4200,"name":"NGC6878","t":"Ga"},{"RA":291.6056,"DE":-60.3361,"AM":12.4300,"name":"IC4852","t":"Ga"},{"RA":189.0866,"DE":25.9877,"AM":12.4300,"name":"NGC4565","t":"Ga"},{"RA":190.4987,"DE":32.5736,"AM":12.4300,"name":"NGC4627","t":"Ga"},{"RA":208.0420,"DE":2.3251,"AM":12.4300,"name":"NGC5329","t":"Ga"},{"RA":217.6063,"DE":35.3210,"AM":12.4300,"name":"NGC5656","t":"Ga"},{"RA":54.1313,"DE":-43.9568,"AM":12.4400,"name":"IC1970","t":"Ga"},{"RA":27.6285,"DE":6.1452,"AM":12.4400,"name":"NGC0693","t":"Ga"},{"RA":34.6886,"DE":-6.6391,"AM":12.4400,"name":"NGC0881","t":"Ga"},{"RA":187.5765,"DE":13.5776,"AM":12.4400,"name":"NGC4479","t":"Ga"},{"RA":190.6567,"DE":-40.7442,"AM":12.4400,"name":"NGC4622","t":"Ga"},{"RA":192.6107,"DE":25.5008,"AM":12.4400,"name":"NGC4725","t":"Ga"},{"RA":32.3525,"DE":-10.1359,"AM":12.4500,"name":"NGC0835","t":"Ga"},{"RA":92.0093,"DE":-21.7467,"AM":12.4500,"name":"NGC2179","t":"Ga"},{"RA":233.6349,"DE":15.1938,"AM":12.4500,"name":"NGC5953","t":"Ga"},{"RA":252.5207,"DE":42.7397,"AM":12.4500,"name":"NGC6239","t":"Ga"},{"RA":213.3328,"DE":-3.1489,"AM":12.4600,"name":"NGC5507","t":"Ga"},{"RA":54.4135,"DE":-18.3395,"AM":12.4700,"name":"NGC1383","t":"Ga"},{"RA":150.1702,"DE":-31.6645,"AM":12.4700,"name":"NGC3100","t":"Ga"},{"RA":187.8855,"DE":11.6247,"AM":12.4700,"name":"NGC4497","t":"Ga"},{"RA":226.8947,"DE":19.5823,"AM":12.4700,"name":"NGC5859","t":"Ga"},{"RA":49.9507,"DE":41.5117,"AM":12.4800,"name":"NGC1275","t":"Ga"},{"RA":75.6773,"DE":-61.1401,"AM":12.4800,"name":"NGC1796","t":"Ga"},{"RA":209.6583,"DE":37.4245,"AM":12.4800,"name":"NGC5395","t":"Ga"},{"RA":12.0062,"DE":27.6236,"AM":12.4900,"name":"NGC0252","t":"Ga"},{"RA":43.6399,"DE":-10.0277,"AM":12.4900,"name":"NGC1140","t":"Ga"},{"RA":27.9605,"DE":6.2969,"AM":12.5000,"name":"NGC0706","t":"Ga"},{"RA":162.4795,"DE":32.9908,"AM":12.5000,"name":"NGC3396","t":"Ga"},{"RA":174.9360,"DE":31.9312,"AM":12.5000,"name":"NGC3788","t":"Ga"},{"RA":175.4502,"DE":20.1036,"AM":12.5000,"name":"NGC3816","t":"Ga"},{"RA":190.8846,"DE":11.5819,"AM":12.5000,"name":"NGC4647","t":"Ga"},{"RA":340.5746,"DE":-30.0577,"AM":12.5000,"name":"NGC7361","t":"Ga"},{"RA":111.7669,"DE":80.1781,"AM":12.5100,"name":"NGC2336","t":"Ga"},{"RA":179.6419,"DE":42.7340,"AM":12.5200,"name":"IC0749","t":"Ga"},{"RA":181.6699,"DE":-29.7602,"AM":12.5200,"name":"NGC4105","t":"Ga"},{"RA":289.6646,"DE":-60.5460,"AM":12.5200,"name":"NGC6771","t":"Ga"},{"RA":184.4577,"DE":47.4092,"AM":12.5300,"name":"NGC4248","t":"Ga"},{"RA":216.7862,"DE":33.2526,"AM":12.5300,"name":"NGC5623","t":"Ga"},{"RA":20.3351,"DE":-34.0633,"AM":12.5400,"name":"NGC0491","t":"Ga"},{"RA":157.1963,"DE":-35.6581,"AM":12.5400,"name":"NGC3257","t":"Ga"},{"RA":201.9023,"DE":-29.5622,"AM":12.5400,"name":"NGC5150","t":"Ga"},{"RA":268.9991,"DE":18.3382,"AM":12.5400,"name":"NGC6500","t":"Ga"},{"RA":163.6479,"DE":56.9907,"AM":12.5500,"name":"NGC3445","t":"Ga"},{"RA":187.7380,"DE":11.4835,"AM":12.5500,"name":"NGC4491","t":"Ga"},{"RA":216.6387,"DE":56.5826,"AM":12.5500,"name":"NGC5631","t":"Ga"},{"RA":73.5563,"DE":-53.3611,"AM":12.5600,"name":"NGC1705","t":"Ga"},{"RA":124.8355,"DE":50.0096,"AM":12.5600,"name":"NGC2552","t":"Ga"},{"RA":198.0278,"DE":24.0950,"AM":12.5600,"name":"NGC5016","t":"Ga"},{"RA":286.4238,"DE":-66.5221,"AM":12.5700,"name":"IC4813","t":"Ga"},{"RA":167.7024,"DE":-37.4479,"AM":12.5800,"name":"NGC3568","t":"Ga"},{"RA":172.0025,"DE":29.5111,"AM":12.5800,"name":"NGC3687","t":"Ga"},{"RA":186.4951,"DE":15.6715,"AM":12.5800,"name":"NGC4396","t":"Ga"},{"RA":334.5742,"DE":40.5624,"AM":12.5800,"name":"NGC7250","t":"Ga"},{"RA":3.8547,"DE":-21.4444,"AM":12.5900,"name":"NGC0059","t":"Ga"},{"RA":21.9875,"DE":-35.7177,"AM":12.5900,"name":"NGC0568","t":"Ga"},{"RA":295.9750,"DE":-70.6334,"AM":12.5900,"name":"NGC6808","t":"Ga"},{"RA":310.8098,"DE":-29.8534,"AM":12.6000,"name":"IC5003","t":"Ga"},{"RA":122.8062,"DE":25.2068,"AM":12.6000,"name":"NGC2535","t":"Ga"},{"RA":95.6445,"DE":51.9095,"AM":12.6100,"name":"NGC2208","t":"Ga"},{"RA":259.5038,"DE":-59.1721,"AM":12.6100,"name":"NGC6305","t":"Ga"},{"RA":304.6508,"DE":-70.8531,"AM":12.6100,"name":"NGC6877","t":"Ga"},{"RA":227.3170,"DE":-11.3217,"AM":12.6200,"name":"NGC5861","t":"Ga"},{"RA":123.4955,"DE":45.7421,"AM":12.6300,"name":"IC2233","t":"Ga"},{"RA":19.9795,"DE":16.5447,"AM":12.6300,"name":"NGC0473","t":"Ga"},{"RA":339.0141,"DE":33.9481,"AM":12.6300,"name":"NGC7320","t":"Ga"},{"RA":146.4514,"DE":-14.3683,"AM":12.6400,"name":"NGC2993","t":"Ga"},{"RA":170.6313,"DE":39.8769,"AM":12.6400,"name":"NGC3648","t":"Ga"},{"RA":177.7786,"DE":55.0787,"AM":12.6400,"name":"NGC3921","t":"Ga"},{"RA":259.4708,"DE":61.7808,"AM":12.6400,"name":"NGC6359","t":"Ga"},{"RA":218.1136,"DE":49.9046,"AM":12.6500,"name":"IC1029","t":"Ga"},{"RA":289.0747,"DE":-60.2003,"AM":12.6500,"name":"IC4836","t":"Ga"},{"RA":314.4749,"DE":-51.8708,"AM":12.6500,"name":"NGC6984","t":"Ga"},{"RA":32.4616,"DE":-7.7625,"AM":12.6600,"name":"NGC0842","t":"Ga"},{"RA":204.1978,"DE":-34.0658,"AM":12.6700,"name":"IC4299","t":"Ga"},{"RA":14.0251,"DE":24.1269,"AM":12.6700,"name":"NGC0304","t":"Ga"},{"RA":176.2662,"DE":19.9737,"AM":12.6700,"name":"NGC3861","t":"Ga"},{"RA":191.7380,"DE":-41.5825,"AM":12.6700,"name":"NGC4677","t":"Ga"},{"RA":204.4127,"DE":-42.8470,"AM":12.6700,"name":"NGC5237","t":"Ga"},{"RA":141.5480,"DE":-76.6263,"AM":12.6800,"name":"NGC2915","t":"Ga"},{"RA":185.9951,"DE":48.7795,"AM":12.6800,"name":"NGC4357","t":"Ga"},{"RA":313.0394,"DE":-48.7778,"AM":12.6800,"name":"NGC6970","t":"Ga"},{"RA":146.2874,"DE":68.5946,"AM":12.6900,"name":"NGC2959","t":"Ga"},{"RA":322.2624,"DE":-52.7676,"AM":12.6900,"name":"NGC7064","t":"Ga"},{"RA":196.3958,"DE":21.1349,"AM":12.7000,"name":"IC4170 NED01","t":"Ga"},{"RA":8.9993,"DE":-10.1217,"AM":12.7000,"name":"NGC0163","t":"Ga"},{"RA":76.6072,"DE":-31.9542,"AM":12.7000,"name":"NGC1800","t":"Ga"},{"RA":133.8946,"DE":58.7344,"AM":12.7000,"name":"NGC2685","t":"Ga"},{"RA":147.4691,"DE":0.6182,"AM":12.7000,"name":"NGC3023","t":"Ga"},{"RA":208.3243,"DE":33.4908,"AM":12.7000,"name":"NGC5347","t":"Ga"},{"RA":17.0978,"DE":33.1336,"AM":12.7100,"name":"NGC0392","t":"Ga"},{"RA":23.5757,"DE":-29.4184,"AM":12.7100,"name":"NGC0613","t":"Ga"},{"RA":34.1348,"DE":-11.3486,"AM":12.7100,"name":"NGC0873","t":"Ga"},{"RA":215.9794,"DE":-28.6881,"AM":12.7100,"name":"NGC5592","t":"Ga"},{"RA":307.6604,"DE":-33.4856,"AM":12.7200,"name":"IC5020","t":"Ga"},{"RA":26.8535,"DE":27.8858,"AM":12.7200,"name":"NGC0670","t":"Ga"},{"RA":129.3863,"DE":28.7052,"AM":12.7200,"name":"NGC2619","t":"Ga"},{"RA":190.7183,"DE":13.2574,"AM":12.7200,"name":"NGC4639","t":"Ga"},{"RA":328.6401,"DE":2.9430,"AM":12.7200,"name":"NGC7156","t":"Ga"},{"RA":33.5145,"DE":27.8773,"AM":12.7500,"name":"NGC0855","t":"Ga"},{"RA":170.9110,"DE":53.8421,"AM":12.7500,"name":"NGC3656","t":"Ga"},{"RA":193.6488,"DE":-12.5686,"AM":12.7500,"name":"NGC4782","t":"Ga"},{"RA":30.2769,"DE":-6.8155,"AM":12.7600,"name":"NGC0788","t":"Ga"},{"RA":169.2277,"DE":18.0517,"AM":12.7600,"name":"NGC3607","t":"Ga"},{"RA":351.9209,"DE":23.5890,"AM":12.7600,"name":"NGC7673","t":"Ga"},{"RA":45.4265,"DE":35.2058,"AM":12.7700,"name":"NGC1167","t":"Ga"},{"RA":159.0490,"DE":-27.1622,"AM":12.7800,"name":"NGC3305","t":"Ga"},{"RA":341.9479,"DE":-22.3121,"AM":12.7800,"name":"NGC7377","t":"Ga"},{"RA":67.2842,"DE":-53.8279,"AM":12.7900,"name":"IC2082 NED01","t":"Ga"},{"RA":67.2793,"DE":-53.8267,"AM":12.7900,"name":"IC2082 NED02","t":"Ga"},{"RA":161.3434,"DE":55.9604,"AM":12.7900,"name":"NGC3353","t":"Ga"},{"RA":157.4645,"DE":-34.9116,"AM":12.8000,"name":"IC2584","t":"Ga"},{"RA":190.5337,"DE":-40.8209,"AM":12.8000,"name":"NGC4603D","t":"Ga"},{"RA":190.5685,"DE":-40.6421,"AM":12.8000,"name":"NGC4616","t":"Ga"},{"RA":193.6525,"DE":-12.5578,"AM":12.8000,"name":"NGC4783","t":"Ga"},{"RA":311.8921,"DE":0.4116,"AM":12.8000,"name":"NGC6967","t":"Ga"},{"RA":40.6483,"DE":34.7635,"AM":12.8100,"name":"NGC1050","t":"Ga"},{"RA":54.7788,"DE":-18.2923,"AM":12.8100,"name":"NGC1394","t":"Ga"},{"RA":322.6538,"DE":-43.1535,"AM":12.8100,"name":"NGC7072","t":"Ga"},{"RA":348.9830,"DE":13.1961,"AM":12.8100,"name":"NGC7563","t":"Ga"},{"RA":37.0465,"DE":19.5991,"AM":12.8200,"name":"NGC0935","t":"Ga"},{"RA":273.9291,"DE":24.9124,"AM":12.8200,"name":"NGC6599","t":"Ga"},{"RA":333.9541,"DE":-45.8464,"AM":12.8200,"name":"NGC7233","t":"Ga"},{"RA":322.6808,"DE":-60.0018,"AM":12.8300,"name":"IC5110","t":"Ga"},{"RA":51.2021,"DE":-21.3361,"AM":12.8300,"name":"NGC1325A","t":"Ga"},{"RA":181.3446,"DE":50.3529,"AM":12.8300,"name":"NGC4085","t":"Ga"},{"RA":204.9904,"DE":0.8309,"AM":12.8300,"name":"NGC5258","t":"Ga"},{"RA":199.6239,"DE":-31.6309,"AM":12.8400,"name":"IC4219","t":"Ga"},{"RA":194.0506,"DE":27.7455,"AM":12.8400,"name":"NGC4816","t":"Ga"},{"RA":199.8820,"DE":-12.6570,"AM":12.8500,"name":"NGC5077","t":"Ga"},{"RA":72.1548,"DE":-6.3200,"AM":12.8600,"name":"NGC1667","t":"Ga"},{"RA":95.9800,"DE":78.5301,"AM":12.8700,"name":"NGC2146A","t":"Ga"},{"RA":166.0122,"DE":28.0368,"AM":12.8700,"name":"NGC3512","t":"Ga"},{"RA":167.8274,"DE":-36.8755,"AM":12.8700,"name":"NGC3573","t":"Ga"},{"RA":179.4036,"DE":32.2776,"AM":12.8700,"name":"NGC3994","t":"Ga"},{"RA":184.8468,"DE":5.8252,"AM":12.8700,"name":"NGC4261","t":"Ga"},{"RA":36.3178,"DE":42.0899,"AM":12.8800,"name":"NGC0906","t":"Ga"},{"RA":107.3002,"DE":20.6029,"AM":12.8800,"name":"NGC2341","t":"Ga"},{"RA":175.5380,"DE":20.3157,"AM":12.8800,"name":"NGC3821","t":"Ga"},{"RA":176.5507,"DE":20.3916,"AM":12.8800,"name":"NGC3884","t":"Ga"},{"RA":16.2341,"DE":-27.4294,"AM":12.8900,"name":"IC1616","t":"Ga"},{"RA":186.8641,"DE":12.2903,"AM":12.8900,"name":"NGC4431","t":"Ga"},{"RA":248.1332,"DE":82.5379,"AM":12.8900,"name":"NGC6251","t":"Ga"},{"RA":211.7683,"DE":-30.0171,"AM":12.9000,"name":"NGC5464","t":"Ga"},{"RA":194.1814,"DE":27.1786,"AM":12.9100,"name":"NGC4827","t":"Ga"},{"RA":54.2873,"DE":-35.1950,"AM":12.9200,"name":"NGC1382","t":"Ga"},{"RA":149.8716,"DE":-19.4923,"AM":12.9200,"name":"NGC3085","t":"Ga"},{"RA":180.7900,"DE":44.5313,"AM":12.9200,"name":"NGC4051","t":"Ga"},{"RA":50.0290,"DE":-52.1855,"AM":12.9300,"name":"NGC1311","t":"Ga"},{"RA":157.6215,"DE":-35.6106,"AM":12.9300,"name":"NGC3273","t":"Ga"},{"RA":165.7967,"DE":27.9725,"AM":12.9300,"name":"NGC3504","t":"Ga"},{"RA":216.8682,"DE":46.1465,"AM":12.9300,"name":"NGC5633","t":"Ga"},{"RA":283.8985,"DE":-53.7234,"AM":12.9300,"name":"NGC6708","t":"Ga"},{"RA":186.4072,"DE":-39.3197,"AM":12.9400,"name":"NGC4373A","t":"Ga"},{"RA":223.4269,"DE":3.5825,"AM":12.9400,"name":"NGC5774","t":"Ga"},{"RA":157.7483,"DE":-34.5629,"AM":12.9500,"name":"IC2587","t":"Ga"},{"RA":348.6227,"DE":23.6848,"AM":12.9500,"name":"NGC7539","t":"Ga"},{"RA":53.3025,"DE":-50.4143,"AM":12.9600,"name":"IC1959","t":"Ga"},{"RA":281.9239,"DE":-63.4057,"AM":12.9600,"name":"IC4767","t":"Ga"},{"RA":45.9100,"DE":-15.6132,"AM":12.9700,"name":"NGC1199","t":"Ga"},{"RA":201.5905,"DE":-33.8685,"AM":12.9700,"name":"NGC5140","t":"Ga"},{"RA":186.9218,"DE":12.3159,"AM":12.9800,"name":"NGC4436","t":"Ga"},{"RA":227.9204,"DE":75.3848,"AM":12.9800,"name":"NGC5912","t":"Ga"},{"RA":204.1626,"DE":-33.9658,"AM":12.9900,"name":"IC4296","t":"Ga"},{"RA":185.6134,"DE":4.5663,"AM":12.9900,"name":"NGC4301","t":"Ga"},{"RA":190.8799,"DE":-41.3625,"AM":12.9900,"name":"NGC4645B","t":"Ga"},{"RA":204.9705,"DE":0.8400,"AM":12.9900,"name":"NGC5257","t":"Ga"},{"RA":311.8512,"DE":0.3008,"AM":12.9900,"name":"NGC6964","t":"Ga"},{"RA":48.2136,"DE":4.7070,"AM":13.0000,"name":"IC0302","t":"Ga"},{"RA":14.3864,"DE":30.2808,"AM":13.0000,"name":"NGC0311","t":"Ga"},{"RA":14.5943,"DE":26.8663,"AM":13.0000,"name":"NGC0326 NED01","t":"Ga"},{"RA":32.3368,"DE":-10.1331,"AM":13.0000,"name":"NGC0833","t":"Ga"},{"RA":151.6390,"DE":-29.9349,"AM":13.0000,"name":"NGC3125","t":"Ga"},{"RA":159.8352,"DE":0.2002,"AM":13.0000,"name":"NGC3325","t":"Ga"},{"RA":190.6635,"DE":19.9453,"AM":13.0000,"name":"NGC4635","t":"Ga"},{"RA":193.7938,"DE":-12.6085,"AM":13.0000,"name":"NGC4794","t":"Ga"},{"RA":194.6466,"DE":27.5963,"AM":13.0000,"name":"NGC4853","t":"Ga"},{"RA":241.3036,"DE":20.5424,"AM":13.0000,"name":"NGC6052 NED01","t":"Ga"},{"RA":196.2432,"DE":29.1223,"AM":13.0100,"name":"NGC4952","t":"Ga"},{"RA":238.8583,"DE":78.9968,"AM":13.0100,"name":"NGC6068","t":"Ga"},{"RA":22.6943,"DE":21.4404,"AM":13.0200,"name":"NGC0575","t":"Ga"},{"RA":159.4055,"DE":-27.5943,"AM":13.0300,"name":"NGC3316","t":"Ga"},{"RA":330.7365,"DE":-20.4713,"AM":13.0300,"name":"NGC7185","t":"Ga"},{"RA":125.3511,"DE":-13.3179,"AM":13.0400,"name":"NGC2578","t":"Ga"},{"RA":53.4153,"DE":-5.0894,"AM":13.0500,"name":"NGC1358","t":"Ga"},{"RA":107.3683,"DE":50.1525,"AM":13.0500,"name":"NGC2330","t":"Ga"},{"RA":281.7399,"DE":45.7057,"AM":13.0500,"name":"NGC6702","t":"Ga"},{"RA":10.8660,"DE":0.1249,"AM":13.0600,"name":"NGC0237","t":"Ga"},{"RA":12.1964,"DE":31.9570,"AM":13.0600,"name":"NGC0262","t":"Ga"},{"RA":138.7486,"DE":29.7303,"AM":13.0600,"name":"NGC2789","t":"Ga"},{"RA":140.9021,"DE":2.1365,"AM":13.0600,"name":"NGC2861","t":"Ga"},{"RA":144.4340,"DE":2.7608,"AM":13.0600,"name":"NGC2936","t":"Ga"},{"RA":189.4630,"DE":-40.5374,"AM":13.0600,"name":"NGC4575","t":"Ga"},{"RA":300.8754,"DE":-54.8448,"AM":13.0700,"name":"NGC6850","t":"Ga"},{"RA":9.1205,"DE":-10.1062,"AM":13.0800,"name":"NGC0165","t":"Ga"},{"RA":259.2478,"DE":-62.8206,"AM":13.0800,"name":"NGC6300","t":"Ga"},{"RA":125.4181,"DE":73.9884,"AM":13.0900,"name":"NGC2544","t":"Ga"},{"RA":150.1380,"DE":-19.6620,"AM":13.0900,"name":"NGC3096","t":"Ga"},{"RA":195.0747,"DE":28.2023,"AM":13.0900,"name":"NGC4895","t":"Ga"},{"RA":206.2863,"DE":41.5034,"AM":13.0900,"name":"NGC5289","t":"Ga"},{"RA":207.1520,"DE":-30.4285,"AM":13.0900,"name":"NGC5298","t":"Ga"},{"RA":319.6377,"DE":26.4470,"AM":13.0900,"name":"NGC7052","t":"Ga"},{"RA":320.5315,"DE":18.6657,"AM":13.0900,"name":"NGC7056","t":"Ga"},{"RA":9.2150,"DE":23.9909,"AM":13.1000,"name":"NGC0169","t":"Ga"},{"RA":182.2917,"DE":29.1769,"AM":13.1000,"name":"NGC4134","t":"Ga"},{"RA":203.2723,"DE":-1.0358,"AM":13.1000,"name":"NGC5211","t":"Ga"},{"RA":339.3720,"DE":10.5316,"AM":13.1000,"name":"NGC7328","t":"Ga"},{"RA":39.9022,"DE":10.7933,"AM":13.1100,"name":"NGC1029","t":"Ga"},{"RA":142.5707,"DE":29.5400,"AM":13.1100,"name":"NGC2893","t":"Ga"},{"RA":159.3035,"DE":-27.6839,"AM":13.1100,"name":"NGC3314A","t":"Ga"},{"RA":226.8638,"DE":19.5976,"AM":13.1100,"name":"NGC5857","t":"Ga"},{"RA":338.9425,"DE":-26.0505,"AM":13.1100,"name":"NGC7314","t":"Ga"},{"RA":10.3631,"DE":-21.0454,"AM":13.1200,"name":"NGC0216","t":"Ga"},{"RA":205.5348,"DE":35.6542,"AM":13.1200,"name":"NGC5273","t":"Ga"},{"RA":209.6402,"DE":37.4535,"AM":13.1200,"name":"NGC5394","t":"Ga"},{"RA":288.5161,"DE":-56.6107,"AM":13.1300,"name":"IC4832","t":"Ga"},{"RA":42.9178,"DE":-16.6510,"AM":13.1300,"name":"NGC1125","t":"Ga"},{"RA":55.1224,"DE":-26.8622,"AM":13.1300,"name":"NGC1412","t":"Ga"},{"RA":178.9016,"DE":29.9959,"AM":13.1300,"name":"NGC3971","t":"Ga"},{"RA":333.2876,"DE":-64.8490,"AM":13.1300,"name":"NGC7219","t":"Ga"},{"RA":278.4590,"DE":-60.1291,"AM":13.1400,"name":"IC4718","t":"Ga"},{"RA":36.8872,"DE":0.2446,"AM":13.1400,"name":"NGC0934","t":"Ga"},{"RA":282.0430,"DE":-63.3834,"AM":13.1500,"name":"IC4770","t":"Ga"},{"RA":356.8691,"DE":-28.1095,"AM":13.1500,"name":"IC5353","t":"Ga"},{"RA":23.4906,"DE":-36.4933,"AM":13.1500,"name":"NGC0612","t":"Ga"},{"RA":62.7494,"DE":-56.4804,"AM":13.1500,"name":"NGC1536","t":"Ga"},{"RA":189.9143,"DE":-5.3442,"AM":13.1500,"name":"NGC4593","t":"Ga"},{"RA":197.7565,"DE":29.6367,"AM":13.1500,"name":"NGC5004","t":"Ga"},{"RA":348.1078,"DE":34.8815,"AM":13.1500,"name":"NGC7514","t":"Ga"},{"RA":22.9035,"DE":-6.8937,"AM":13.1600,"name":"NGC0586","t":"Ga"},{"RA":139.9453,"DE":33.7497,"AM":13.1700,"name":"NGC2832","t":"Ga"},{"RA":178.6403,"DE":58.3670,"AM":13.1700,"name":"NGC3958","t":"Ga"},{"RA":193.7299,"DE":27.4127,"AM":13.1700,"name":"NGC4797","t":"Ga"},{"RA":194.1161,"DE":26.9873,"AM":13.1700,"name":"NGC4819","t":"Ga"},{"RA":160.7622,"DE":-36.3624,"AM":13.1800,"name":"NGC3354","t":"Ga"},{"RA":187.9965,"DE":14.4204,"AM":13.1800,"name":"M88","t":"Ga"},{"RA":349.1861,"DE":13.4830,"AM":13.1800,"name":"NGC7570","t":"Ga"},{"RA":55.0297,"DE":-18.4435,"AM":13.1900,"name":"IC0343","t":"Ga"},{"RA":301.6178,"DE":-48.3756,"AM":13.1900,"name":"IC4943","t":"Ga"},{"RA":150.4801,"DE":72.1703,"AM":13.1900,"name":"NGC3065","t":"Ga"},{"RA":352.0255,"DE":23.5314,"AM":13.1900,"name":"NGC7677","t":"Ga"},{"RA":358.3438,"DE":-40.8103,"AM":13.1900,"name":"NGC7764A","t":"Ga"},{"RA":251.7459,"DE":58.4232,"AM":13.2000,"name":"IC1231","t":"Ga"},{"RA":152.2107,"DE":-67.0309,"AM":13.2000,"name":"IC2554","t":"Ga"},{"RA":170.2867,"DE":3.1946,"AM":13.2000,"name":"NGC3641","t":"Ga"},{"RA":183.0382,"DE":36.1692,"AM":13.2000,"name":"NGC4163","t":"Ga"},{"RA":189.0317,"DE":-39.4387,"AM":13.2000,"name":"NGC4553","t":"Ga"},{"RA":260.9210,"DE":-65.0102,"AM":13.2000,"name":"NGC6328","t":"Ga"},{"RA":343.8352,"DE":-33.8879,"AM":13.2100,"name":"IC5262","t":"Ga"},{"RA":181.1128,"DE":1.8960,"AM":13.2100,"name":"NGC4073","t":"Ga"},{"RA":228.7634,"DE":42.0498,"AM":13.2100,"name":"NGC5899","t":"Ga"},{"RA":268.0250,"DE":21.5696,"AM":13.2200,"name":"IC1269","t":"Ga"},{"RA":7.4105,"DE":-33.2597,"AM":13.2200,"name":"NGC0131","t":"Ga"},{"RA":167.6600,"DE":28.7676,"AM":13.2200,"name":"NGC3550 NED02","t":"Ga"},{"RA":332.1243,"DE":-64.7061,"AM":13.2200,"name":"NGC7199","t":"Ga"},{"RA":351.9863,"DE":8.7790,"AM":13.2300,"name":"NGC7674","t":"Ga"},{"RA":60.8860,"DE":-43.4001,"AM":13.2400,"name":"NGC1510","t":"Ga"},{"RA":160.5750,"DE":0.3769,"AM":13.2400,"name":"NGC3340","t":"Ga"},{"RA":194.7662,"DE":28.1237,"AM":13.2400,"name":"NGC4860","t":"Ga"},{"RA":183.4365,"DE":36.6340,"AM":13.2500,"name":"NGC4190","t":"Ga"},{"RA":53.7467,"DE":-35.1711,"AM":13.2600,"name":"NGC1373","t":"Ga"},{"RA":119.4854,"DE":25.1609,"AM":13.2600,"name":"NGC2486","t":"Ga"},{"RA":133.0206,"DE":53.6173,"AM":13.2600,"name":"NGC2675","t":"Ga"},{"RA":182.1970,"DE":29.3048,"AM":13.2700,"name":"NGC4131","t":"Ga"},{"RA":282.2537,"DE":47.6581,"AM":13.2700,"name":"NGC6711","t":"Ga"},{"RA":148.0340,"DE":29.2362,"AM":13.2800,"name":"NGC3032","t":"Ga"},{"RA":356.0881,"DE":9.9341,"AM":13.2800,"name":"NGC7743","t":"Ga"},{"RA":188.1711,"DE":12.7710,"AM":13.2900,"name":"IC3475","t":"Ga"},{"RA":28.1937,"DE":36.1518,"AM":13.2900,"name":"NGC0708","t":"Ga"},{"RA":24.0007,"DE":0.6635,"AM":13.3000,"name":"NGC0622","t":"Ga"},{"RA":183.5395,"DE":54.5268,"AM":13.3000,"name":"NGC4194","t":"Ga"},{"RA":207.2337,"DE":39.9851,"AM":13.3000,"name":"NGC5311","t":"Ga"},{"RA":327.4417,"DE":-34.8763,"AM":13.3000,"name":"NGC7135","t":"Ga"},{"RA":354.6225,"DE":27.0315,"AM":13.3000,"name":"NGC7720 NED01","t":"Ga"},{"RA":154.0780,"DE":-33.5638,"AM":13.3100,"name":"IC2560","t":"Ga"},{"RA":189.0005,"DE":54.2210,"AM":13.3100,"name":"NGC4566","t":"Ga"},{"RA":193.0666,"DE":-41.3907,"AM":13.3100,"name":"NGC4743","t":"Ga"},{"RA":224.8532,"DE":-16.6934,"AM":13.3200,"name":"NGC5793","t":"Ga"},{"RA":27.6385,"DE":36.3708,"AM":13.3300,"name":"NGC0687","t":"Ga"},{"RA":66.9790,"DE":-55.0577,"AM":13.3300,"name":"NGC1602","t":"Ga"},{"RA":155.8625,"DE":19.8985,"AM":13.3300,"name":"NGC3226","t":"Ga"},{"RA":156.9365,"DE":-40.4350,"AM":13.3300,"name":"NGC3250B","t":"Ga"},{"RA":195.2337,"DE":27.7908,"AM":13.3300,"name":"NGC4911","t":"Ga"},{"RA":21.4963,"DE":-1.3402,"AM":13.3400,"name":"NGC0545","t":"Ga"},{"RA":21.5026,"DE":-1.3452,"AM":13.3400,"name":"NGC0547","t":"Ga"},{"RA":54.7207,"DE":-18.3541,"AM":13.3400,"name":"NGC1391","t":"Ga"},{"RA":183.0894,"DE":29.2071,"AM":13.3400,"name":"NGC4173","t":"Ga"},{"RA":157.4525,"DE":-35.3224,"AM":13.3500,"name":"NGC3267","t":"Ga"},{"RA":182.6562,"DE":16.0329,"AM":13.3500,"name":"NGC4152","t":"Ga"},{"RA":200.3238,"DE":-43.7197,"AM":13.3500,"name":"NGC5091","t":"Ga"},{"RA":201.4336,"DE":-29.8337,"AM":13.3500,"name":"NGC5135","t":"Ga"},{"RA":304.8735,"DE":-70.8599,"AM":13.3500,"name":"NGC6880","t":"Ga"},{"RA":339.3308,"DE":34.4477,"AM":13.3500,"name":"NGC7335","t":"Ga"},{"RA":129.6003,"DE":25.7546,"AM":13.3600,"name":"NGC2623","t":"Ga"},{"RA":192.0628,"DE":10.9836,"AM":13.3600,"name":"NGC4694","t":"Ga"},{"RA":220.6385,"DE":28.7264,"AM":13.3600,"name":"NGC5735","t":"Ga"},{"RA":332.1018,"DE":-29.0512,"AM":13.3600,"name":"NGC7208","t":"Ga"},{"RA":186.7276,"DE":0.8776,"AM":13.3700,"name":"NGC4355","t":"Ga"},{"RA":226.6217,"DE":1.5949,"AM":13.3700,"name":"NGC5846A","t":"Ga"},{"RA":253.2453,"DE":2.4009,"AM":13.3700,"name":"NGC6240","t":"Ga"},{"RA":228.7715,"DE":42.2094,"AM":13.3900,"name":"NGC5900","t":"Ga"},{"RA":21.1119,"DE":33.7994,"AM":13.4000,"name":"NGC0513","t":"Ga"},{"RA":72.9586,"DE":-5.8032,"AM":13.4000,"name":"NGC1681","t":"Ga"},{"RA":150.2170,"DE":55.6188,"AM":13.4000,"name":"NGC3073","t":"Ga"},{"RA":220.5996,"DE":-17.2531,"AM":13.4000,"name":"NGC5728","t":"Ga"},{"RA":162.0182,"DE":-31.5334,"AM":13.4100,"name":"NGC3390","t":"Ga"},{"RA":197.4479,"DE":28.9069,"AM":13.4100,"name":"NGC5000","t":"Ga"},{"RA":281.8990,"DE":-63.2922,"AM":13.4200,"name":"IC4766","t":"Ga"},{"RA":198.5568,"DE":-42.9613,"AM":13.4200,"name":"NGC5026","t":"Ga"},{"RA":204.5729,"DE":48.2769,"AM":13.4200,"name":"NGC5256","t":"Ga"},{"RA":204.5721,"DE":48.2756,"AM":13.4200,"name":"NGC5256 NED01","t":"Ga"},{"RA":278.3219,"DE":-57.9757,"AM":13.4300,"name":"IC4717","t":"Ga"},{"RA":174.7573,"DE":-37.7387,"AM":13.4300,"name":"NGC3783","t":"Ga"},{"RA":331.2055,"DE":-64.0468,"AM":13.4300,"name":"NGC7179","t":"Ga"},{"RA":348.5549,"DE":13.4264,"AM":13.4300,"name":"NGC7536","t":"Ga"},{"RA":187.0359,"DE":12.0933,"AM":13.4400,"name":"IC0794","t":"Ga"},{"RA":304.4280,"DE":-70.9151,"AM":13.4400,"name":"IC4972","t":"Ga"},{"RA":13.1765,"DE":-31.2058,"AM":13.4400,"name":"NGC0289","t":"Ga"},{"RA":36.5280,"DE":0.3319,"AM":13.4400,"name":"NGC0926","t":"Ga"},{"RA":154.4494,"DE":21.8733,"AM":13.4400,"name":"NGC3187","t":"Ga"},{"RA":216.5508,"DE":48.5640,"AM":13.4400,"name":"NGC5622","t":"Ga"},{"RA":248.7883,"DE":46.2139,"AM":13.4500,"name":"IC1222","t":"Ga"},{"RA":9.8991,"DE":-9.1945,"AM":13.4500,"name":"NGC0195","t":"Ga"},{"RA":183.1294,"DE":29.1684,"AM":13.4500,"name":"NGC4175","t":"Ga"},{"RA":253.1920,"DE":-59.2186,"AM":13.4500,"name":"NGC6221","t":"Ga"},{"RA":259.9778,"DE":16.6607,"AM":13.4500,"name":"NGC6347","t":"Ga"},{"RA":187.8453,"DE":29.1365,"AM":13.4600,"name":"NGC4495","t":"Ga"},{"RA":30.9368,"DE":38.2587,"AM":13.4700,"name":"NGC0801","t":"Ga"},{"RA":196.5721,"DE":29.0629,"AM":13.4800,"name":"NGC4966","t":"Ga"},{"RA":0.8839,"DE":-10.7447,"AM":13.4800,"name":"NGC7808","t":"Ga"},{"RA":29.8068,"DE":18.9547,"AM":13.4900,"name":"NGC0770","t":"Ga"},{"RA":186.3254,"DE":4.9251,"AM":13.4900,"name":"NGC4378","t":"Ga"},{"RA":280.6781,"DE":40.3669,"AM":13.4900,"name":"NGC6695","t":"Ga"},{"RA":328.0638,"DE":-55.5697,"AM":13.4900,"name":"NGC7140","t":"Ga"},{"RA":190.2202,"DE":-36.7559,"AM":13.5000,"name":"IC3639","t":"Ga"},{"RA":204.0094,"DE":-25.8823,"AM":13.5000,"name":"IC4293","t":"Ga"},{"RA":147.9793,"DE":-6.8229,"AM":13.5000,"name":"NGC3035","t":"Ga"},{"RA":192.4756,"DE":-41.2796,"AM":13.5000,"name":"NGC4706","t":"Ga"},{"RA":193.8713,"DE":27.5214,"AM":13.5000,"name":"NGC4807","t":"Ga"},{"RA":195.2269,"DE":28.0076,"AM":13.5000,"name":"NGC4908","t":"Ga"},{"RA":213.0973,"DE":-27.1080,"AM":13.5000,"name":"NGC5495","t":"Ga"},{"RA":266.2359,"DE":55.7048,"AM":13.5000,"name":"NGC6454","t":"Ga"},{"RA":88.0474,"DE":-7.4562,"AM":13.5100,"name":"NGC2110","t":"Ga"},{"RA":157.4878,"DE":-35.2244,"AM":13.5100,"name":"NGC3269","t":"Ga"},{"RA":208.9981,"DE":-30.3414,"AM":13.5100,"name":"NGC5357","t":"Ga"},{"RA":186.7264,"DE":11.6640,"AM":13.5200,"name":"IC3358","t":"Ga"},{"RA":2.7773,"DE":-12.1073,"AM":13.5200,"name":"NGC0017","t":"Ga"},{"RA":194.8473,"DE":27.9116,"AM":13.5200,"name":"NGC4869","t":"Ga"},{"RA":209.1647,"DE":-44.0093,"AM":13.5200,"name":"NGC5365A","t":"Ga"},{"RA":312.1151,"DE":7.7400,"AM":13.5200,"name":"NGC6969","t":"Ga"},{"RA":302.1954,"DE":-61.1002,"AM":13.5300,"name":"NGC6860","t":"Ga"},{"RA":339.0148,"DE":33.9757,"AM":13.5300,"name":"NGC7319","t":"Ga"},{"RA":102.5361,"DE":60.8458,"AM":13.5400,"name":"NGC2273","t":"Ga"},{"RA":157.7782,"DE":28.7967,"AM":13.5400,"name":"NGC3265","t":"Ga"},{"RA":160.3583,"DE":-23.3843,"AM":13.5400,"name":"NGC3355","t":"Ga"},{"RA":183.0492,"DE":13.2465,"AM":13.5400,"name":"NGC4165","t":"Ga"},{"RA":188.9026,"DE":-39.9093,"AM":13.5400,"name":"NGC4507","t":"Ga"},{"RA":329.8587,"DE":-16.5123,"AM":13.5400,"name":"NGC7165","t":"Ga"},{"RA":339.6578,"DE":34.0714,"AM":13.5400,"name":"NGC7343","t":"Ga"},{"RA":260.9471,"DE":26.4865,"AM":13.5500,"name":"IC1256","t":"Ga"},{"RA":175.8523,"DE":19.7498,"AM":13.5500,"name":"IC2951","t":"Ga"},{"RA":149.8731,"DE":-22.8263,"AM":13.5500,"name":"NGC3081","t":"Ga"},{"RA":14.4127,"DE":43.8008,"AM":13.5600,"name":"NGC0317A","t":"Ga"},{"RA":194.9900,"DE":28.2474,"AM":13.5600,"name":"NGC4881","t":"Ga"},{"RA":207.5062,"DE":-30.5785,"AM":13.5600,"name":"NGC5304","t":"Ga"},{"RA":349.5941,"DE":-4.4161,"AM":13.5600,"name":"NGC7592B","t":"Ga"},{"RA":19.7598,"DE":-17.0604,"AM":13.5700,"name":"IC0093","t":"Ga"},{"RA":177.2350,"DE":48.6747,"AM":13.5700,"name":"NGC3896","t":"Ga"},{"RA":184.6105,"DE":29.8129,"AM":13.5700,"name":"NGC4253","t":"Ga"},{"RA":188.8602,"DE":14.4963,"AM":13.5700,"name":"M91","t":"Ga"},{"RA":198.8954,"DE":29.6761,"AM":13.5700,"name":"NGC5052","t":"Ga"},{"RA":195.2148,"DE":28.0428,"AM":13.5800,"name":"IC4051","t":"Ga"},{"RA":18.6039,"DE":-55.3971,"AM":13.5800,"name":"NGC0454 NED02","t":"Ga"},{"RA":181.6624,"DE":28.1742,"AM":13.5800,"name":"NGC4104","t":"Ga"},{"RA":191.2044,"DE":-40.7143,"AM":13.5800,"name":"NGC4650A","t":"Ga"},{"RA":227.8668,"DE":75.3838,"AM":13.5800,"name":"NGC5909","t":"Ga"},{"RA":123.2256,"DE":55.6721,"AM":13.5900,"name":"NGC2534","t":"Ga"},{"RA":311.8493,"DE":-38.4183,"AM":13.6000,"name":"IC5049B","t":"Ga"},{"RA":313.0097,"DE":-57.0688,"AM":13.6000,"name":"IC5063","t":"Ga"},{"RA":43.6141,"DE":41.5796,"AM":13.6000,"name":"NGC1129","t":"Ga"},{"RA":184.2912,"DE":7.1916,"AM":13.6000,"name":"NGC4235","t":"Ga"},{"RA":218.1698,"DE":-44.1744,"AM":13.6000,"name":"NGC5643","t":"Ga"},{"RA":219.3422,"DE":36.5678,"AM":13.6000,"name":"NGC5695","t":"Ga"},{"RA":338.9662,"DE":33.9449,"AM":13.6000,"name":"NGC7317","t":"Ga"},{"RA":34.2947,"DE":14.5478,"AM":13.6100,"name":"NGC0871","t":"Ga"},{"RA":161.8429,"DE":14.0694,"AM":13.6100,"name":"NGC3377A","t":"Ga"},{"RA":330.5079,"DE":-31.8697,"AM":13.6100,"name":"NGC7172","t":"Ga"},{"RA":204.6086,"DE":0.2276,"AM":13.6200,"name":"IC0903","t":"Ga"},{"RA":238.2202,"DE":40.6467,"AM":13.6300,"name":"NGC6013","t":"Ga"},{"RA":305.7794,"DE":-43.8686,"AM":13.6300,"name":"NGC6902B","t":"Ga"},{"RA":138.3808,"DE":28.9518,"AM":13.6400,"name":"IC2446","t":"Ga"},{"RA":157.0798,"DE":-35.4545,"AM":13.6400,"name":"NGC3258A","t":"Ga"},{"RA":183.1120,"DE":29.1492,"AM":13.6400,"name":"NGC4174","t":"Ga"},{"RA":283.8419,"DE":-53.8184,"AM":13.6400,"name":"NGC6707","t":"Ga"},{"RA":5.9975,"DE":15.7704,"AM":13.6500,"name":"NGC0099","t":"Ga"},{"RA":203.9107,"DE":75.0394,"AM":13.6500,"name":"NGC5262","t":"Ga"},{"RA":233.3661,"DE":56.5597,"AM":13.6500,"name":"NGC5963","t":"Ga"},{"RA":288.8922,"DE":-54.6267,"AM":13.6600,"name":"IC4839","t":"Ga"},{"RA":49.8387,"DE":41.4906,"AM":13.6600,"name":"NGC1272","t":"Ga"},{"RA":144.4376,"DE":2.7474,"AM":13.6600,"name":"NGC2937","t":"Ga"},{"RA":348.5532,"DE":13.5819,"AM":13.6600,"name":"NGC7535","t":"Ga"},{"RA":285.3779,"DE":-57.5321,"AM":13.6700,"name":"IC4806","t":"Ga"},{"RA":159.0885,"DE":58.6202,"AM":13.6700,"name":"NGC3284","t":"Ga"},{"RA":197.7343,"DE":37.0592,"AM":13.6700,"name":"NGC5005","t":"Ga"},{"RA":203.2029,"DE":41.8718,"AM":13.6700,"name":"NGC5214","t":"Ga"},{"RA":288.7700,"DE":-50.6568,"AM":13.6700,"name":"NGC6761","t":"Ga"},{"RA":322.4984,"DE":2.4142,"AM":13.6700,"name":"NGC7077","t":"Ga"},{"RA":40.9605,"DE":32.5119,"AM":13.6900,"name":"NGC1067","t":"Ga"},{"RA":194.8328,"DE":28.0843,"AM":13.6900,"name":"NGC4865","t":"Ga"},{"RA":237.1040,"DE":-13.7578,"AM":13.6900,"name":"NGC5995","t":"Ga"},{"RA":218.4677,"DE":5.4582,"AM":13.7000,"name":"NGC5674","t":"Ga"},{"RA":47.8305,"DE":-8.9024,"AM":13.7100,"name":"NGC1242","t":"Ga"},{"RA":139.3793,"DE":41.9941,"AM":13.7100,"name":"NGC2799","t":"Ga"},{"RA":214.4980,"DE":25.1368,"AM":13.7300,"name":"NGC5548","t":"Ga"},{"RA":221.9432,"DE":-19.0786,"AM":13.7300,"name":"NGC5757","t":"Ga"},{"RA":254.4920,"DE":27.8543,"AM":13.7300,"name":"NGC6269","t":"Ga"},{"RA":174.9273,"DE":31.9093,"AM":13.7400,"name":"NGC3786","t":"Ga"},{"RA":256.9041,"DE":60.7289,"AM":13.7400,"name":"NGC6306","t":"Ga"},{"RA":58.6265,"DE":10.7070,"AM":13.7600,"name":"NGC1474","t":"Ga"},{"RA":157.2760,"DE":-44.1597,"AM":13.7600,"name":"NGC3262","t":"Ga"},{"RA":349.7284,"DE":-42.2391,"AM":13.7600,"name":"NGC7590","t":"Ga"},{"RA":195.2027,"DE":28.0908,"AM":13.7700,"name":"IC4045","t":"Ga"},{"RA":61.5330,"DE":-52.6684,"AM":13.7800,"name":"NGC1522","t":"Ga"},{"RA":336.8028,"DE":-35.1404,"AM":13.7800,"name":"NGC7279","t":"Ga"},{"RA":191.9265,"DE":-41.5283,"AM":13.8000,"name":"NGC4683","t":"Ga"},{"RA":196.0600,"DE":-10.3396,"AM":13.8000,"name":"NGC4939","t":"Ga"},{"RA":33.6398,"DE":0.7667,"AM":13.8100,"name":"NGC0863","t":"Ga"},{"RA":192.7871,"DE":28.7881,"AM":13.8100,"name":"NGC4738","t":"Ga"},{"RA":195.2033,"DE":28.1583,"AM":13.8100,"name":"NGC4907","t":"Ga"},{"RA":309.6910,"DE":-52.1433,"AM":13.8100,"name":"NGC6937","t":"Ga"},{"RA":195.4307,"DE":29.0447,"AM":13.8200,"name":"IC4088","t":"Ga"},{"RA":197.3948,"DE":-51.9686,"AM":13.8200,"name":"IC4200","t":"Ga"},{"RA":320.3719,"DE":21.2420,"AM":13.8200,"name":"IC5104","t":"Ga"},{"RA":58.0366,"DE":-44.5325,"AM":13.8200,"name":"NGC1476","t":"Ga"},{"RA":197.3220,"DE":-5.2728,"AM":13.8200,"name":"NGC4990","t":"Ga"},{"RA":205.1546,"DE":-48.3420,"AM":13.8200,"name":"NGC5266A","t":"Ga"},{"RA":17.1085,"DE":33.1480,"AM":13.8300,"name":"NGC0394","t":"Ga"},{"RA":143.4421,"DE":10.1524,"AM":13.8300,"name":"NGC2911","t":"Ga"},{"RA":195.3900,"DE":29.1306,"AM":13.8400,"name":"IC0843","t":"Ga"},{"RA":257.8892,"DE":72.4020,"AM":13.8400,"name":"IC1254","t":"Ga"},{"RA":302.3824,"DE":-61.8505,"AM":13.8400,"name":"IC4951","t":"Ga"},{"RA":26.1477,"DE":37.6958,"AM":13.8400,"name":"NGC0662","t":"Ga"},{"RA":175.9957,"DE":20.0770,"AM":13.8400,"name":"NGC3840","t":"Ga"},{"RA":186.2287,"DE":7.4449,"AM":13.8400,"name":"NGC4370","t":"Ga"},{"RA":194.7030,"DE":27.8104,"AM":13.8500,"name":"IC3946","t":"Ga"},{"RA":48.9801,"DE":37.1541,"AM":13.8600,"name":"IC1900","t":"Ga"},{"RA":195.0736,"DE":27.9554,"AM":13.8600,"name":"NGC4898A","t":"Ga"},{"RA":176.0033,"DE":20.0293,"AM":13.8700,"name":"NGC3844","t":"Ga"},{"RA":194.8046,"DE":27.9770,"AM":13.8700,"name":"NGC4864","t":"Ga"},{"RA":308.2755,"DE":-2.0275,"AM":13.8700,"name":"NGC6926","t":"Ga"},{"RA":327.0813,"DE":-34.9513,"AM":13.8700,"name":"NGC7130","t":"Ga"},{"RA":233.7385,"DE":23.5031,"AM":13.8800,"name":"IC4553","t":"Ga"},{"RA":304.2390,"DE":-70.7498,"AM":13.8800,"name":"IC4970","t":"Ga"},{"RA":248.1633,"DE":78.1982,"AM":13.8800,"name":"NGC6217","t":"Ga"},{"RA":64.3091,"DE":4.7816,"AM":13.8900,"name":"NGC1542","t":"Ga"},{"RA":146.2515,"DE":29.4523,"AM":13.9000,"name":"IC0558","t":"Ga"},{"RA":23.3803,"DE":35.6683,"AM":13.9000,"name":"NGC0591","t":"Ga"},{"RA":347.4470,"DE":-43.4279,"AM":13.9000,"name":"NGC7496","t":"Ga"},{"RA":314.3266,"DE":-51.8623,"AM":13.9200,"name":"NGC6982","t":"Ga"},{"RA":195.1648,"DE":29.0194,"AM":13.9300,"name":"IC0842","t":"Ga"},{"RA":44.4232,"DE":6.0269,"AM":13.9300,"name":"NGC1128 NED02","t":"Ga"},{"RA":122.8163,"DE":25.1794,"AM":13.9300,"name":"NGC2536","t":"Ga"},{"RA":289.1921,"DE":-61.6145,"AM":13.9400,"name":"IC4838","t":"Ga"},{"RA":14.4185,"DE":43.7923,"AM":13.9400,"name":"NGC0317B","t":"Ga"},{"RA":185.7572,"DE":15.9056,"AM":13.9400,"name":"NGC4323","t":"Ga"},{"RA":162.0978,"DE":-25.1621,"AM":13.9500,"name":"NGC3393","t":"Ga"},{"RA":193.5219,"DE":27.1496,"AM":13.9500,"name":"NGC4789A","t":"Ga"},{"RA":159.2605,"DE":-27.5651,"AM":13.9600,"name":"NGC3312","t":"Ga"},{"RA":210.8585,"DE":-6.0308,"AM":13.9600,"name":"NGC5427","t":"Ga"},{"RA":223.5945,"DE":28.9397,"AM":13.9600,"name":"NGC5780","t":"Ga"},{"RA":11.8880,"DE":-25.2882,"AM":13.9700,"name":"NGC0253","t":"Ga"},{"RA":38.1727,"DE":-39.2962,"AM":13.9700,"name":"NGC0986A","t":"Ga"},{"RA":176.2709,"DE":19.6063,"AM":13.9700,"name":"NGC3862","t":"Ga"},{"RA":204.4062,"DE":15.9722,"AM":13.9700,"name":"NGC5249","t":"Ga"},{"RA":278.1464,"DE":-63.2933,"AM":13.9700,"name":"NGC6630","t":"Ga"},{"RA":37.0531,"DE":19.5833,"AM":13.9800,"name":"IC1801","t":"Ga"},{"RA":186.6961,"DE":12.4540,"AM":13.9800,"name":"IC3349","t":"Ga"},{"RA":278.2981,"DE":-56.7322,"AM":13.9800,"name":"IC4719","t":"Ga"},{"RA":49.8092,"DE":-19.1000,"AM":13.9800,"name":"NGC1297","t":"Ga"},{"RA":188.1790,"DE":29.7124,"AM":13.9800,"name":"NGC4514","t":"Ga"},{"RA":220.1165,"DE":-78.8092,"AM":13.9900,"name":"IC4448","t":"Ga"},{"RA":68.4994,"DE":-8.5789,"AM":13.9900,"name":"NGC1614","t":"Ga"},{"RA":107.2834,"DE":48.6154,"AM":13.9900,"name":"NGC2329","t":"Ga"},{"RA":159.1070,"DE":58.5562,"AM":13.9900,"name":"NGC3288","t":"Ga"},{"RA":182.2558,"DE":29.2501,"AM":13.9900,"name":"NGC4132","t":"Ga"},{"RA":194.9130,"DE":28.8955,"AM":14.0000,"name":"IC3990","t":"Ga"},{"RA":288.9654,"DE":-56.2091,"AM":14.0000,"name":"IC4840","t":"Ga"},{"RA":51.2029,"DE":-3.0423,"AM":14.0000,"name":"NGC1320","t":"Ga"},{"RA":73.8489,"DE":-20.5712,"AM":14.0000,"name":"NGC1692","t":"Ga"},{"RA":206.8520,"DE":-30.4070,"AM":14.0000,"name":"NGC5291","t":"Ga"},{"RA":231.5257,"DE":41.6707,"AM":14.0000,"name":"NGC5929","t":"Ga"},{"RA":195.1782,"DE":27.9714,"AM":14.0100,"name":"IC4042","t":"Ga"},{"RA":211.3888,"DE":54.4611,"AM":14.0100,"name":"NGC5477","t":"Ga"},{"RA":349.7359,"DE":0.2439,"AM":14.0100,"name":"NGC7603","t":"Ga"},{"RA":157.9670,"DE":-34.8537,"AM":14.0200,"name":"NGC3281","t":"Ga"},{"RA":182.2867,"DE":44.0032,"AM":14.0200,"name":"NGC4135","t":"Ga"},{"RA":304.5754,"DE":-44.8067,"AM":14.0200,"name":"NGC6890","t":"Ga"},{"RA":194.7842,"DE":27.7841,"AM":14.0300,"name":"IC3959","t":"Ga"},{"RA":194.8784,"DE":27.8842,"AM":14.0300,"name":"IC3973","t":"Ga"},{"RA":193.0519,"DE":-13.4147,"AM":14.0300,"name":"NGC4748","t":"Ga"},{"RA":194.5910,"DE":27.9677,"AM":14.0300,"name":"NGC4850","t":"Ga"},{"RA":277.4973,"DE":-67.2244,"AM":14.0400,"name":"IC4713","t":"Ga"},{"RA":167.2319,"DE":26.6105,"AM":14.0400,"name":"NGC3534","t":"Ga"},{"RA":170.5745,"DE":59.0745,"AM":14.0400,"name":"NGC3642","t":"Ga"},{"RA":149.6671,"DE":28.8776,"AM":14.0500,"name":"NGC3068","t":"Ga"},{"RA":205.2740,"DE":67.6723,"AM":14.0500,"name":"NGC5283","t":"Ga"},{"RA":304.9957,"DE":-52.6220,"AM":14.0600,"name":"IC4995","t":"Ga"},{"RA":194.8748,"DE":27.9564,"AM":14.0700,"name":"NGC4871","t":"Ga"},{"RA":195.1657,"DE":27.9239,"AM":14.0800,"name":"NGC4906","t":"Ga"},{"RA":67.4172,"DE":-27.4085,"AM":14.0900,"name":"NGC1592","t":"Ga"},{"RA":29.9635,"DE":-6.8404,"AM":14.1000,"name":"IC0184","t":"Ga"},{"RA":133.6931,"DE":39.5387,"AM":14.1000,"name":"NGC2691","t":"Ga"},{"RA":194.8918,"DE":27.9469,"AM":14.1000,"name":"NGC4872","t":"Ga"},{"RA":238.6980,"DE":78.9851,"AM":14.1000,"name":"NGC6068A","t":"Ga"},{"RA":332.2820,"DE":-27.8095,"AM":14.1000,"name":"NGC7214","t":"Ga"},{"RA":21.3807,"DE":1.7591,"AM":14.1100,"name":"NGC0533","t":"Ga"},{"RA":17.8651,"DE":-38.0835,"AM":14.1200,"name":"NGC0424","t":"Ga"},{"RA":129.5456,"DE":24.8953,"AM":14.1200,"name":"NGC2622","t":"Ga"},{"RA":186.4283,"DE":0.5726,"AM":14.1200,"name":"NGC4385","t":"Ga"},{"RA":194.6515,"DE":28.1137,"AM":14.1300,"name":"IC3943","t":"Ga"},{"RA":158.5310,"DE":-35.3234,"AM":14.1300,"name":"NGC3289","t":"Ga"},{"RA":194.8866,"DE":27.9836,"AM":14.1300,"name":"NGC4873","t":"Ga"},{"RA":49.9756,"DE":41.5634,"AM":14.1400,"name":"NGC1278","t":"Ga"},{"RA":194.8135,"DE":27.9707,"AM":14.1400,"name":"NGC4867","t":"Ga"},{"RA":168.4573,"DE":9.5863,"AM":14.1700,"name":"IC2637","t":"Ga"},{"RA":159.7991,"DE":0.4095,"AM":14.1800,"name":"IC0632","t":"Ga"},{"RA":45.9546,"DE":-1.1038,"AM":14.1800,"name":"NGC1194","t":"Ga"},{"RA":194.9350,"DE":27.9125,"AM":14.1800,"name":"NGC4876","t":"Ga"},{"RA":216.1143,"DE":-16.7628,"AM":14.1800,"name":"NGC5597","t":"Ga"},{"RA":103.0510,"DE":74.4271,"AM":14.1900,"name":"IC0450","t":"Ga"},{"RA":178.5511,"DE":0.1366,"AM":14.1900,"name":"IC0745","t":"Ga"},{"RA":121.7799,"DE":36.2335,"AM":14.1900,"name":"IC2227","t":"Ga"},{"RA":183.7293,"DE":13.4605,"AM":14.1900,"name":"IC3059","t":"Ga"},{"RA":354.8843,"DE":-22.4133,"AM":14.1900,"name":"IC5345","t":"Ga"},{"RA":49.8614,"DE":41.5405,"AM":14.2000,"name":"NGC1273","t":"Ga"},{"RA":190.1947,"DE":-40.8931,"AM":14.2000,"name":"NGC4601","t":"Ga"},{"RA":197.7571,"DE":29.5783,"AM":14.2000,"name":"NGC5004A","t":"Ga"},{"RA":338.6538,"DE":-22.4851,"AM":14.2000,"name":"NGC7310","t":"Ga"},{"RA":204.6342,"DE":0.5402,"AM":14.2100,"name":"IC0904","t":"Ga"},{"RA":137.8787,"DE":28.8266,"AM":14.2100,"name":"IC2443","t":"Ga"},{"RA":194.6975,"DE":27.6747,"AM":14.2100,"name":"NGC4854","t":"Ga"},{"RA":204.5665,"DE":4.5426,"AM":14.2100,"name":"NGC5252","t":"Ga"},{"RA":295.6693,"DE":-10.3235,"AM":14.2100,"name":"NGC6814","t":"Ga"},{"RA":351.8810,"DE":12.3852,"AM":14.2100,"name":"NGC7672","t":"Ga"},{"RA":223.5977,"DE":16.3553,"AM":14.2200,"name":"IC4516","t":"Ga"},{"RA":189.5553,"DE":28.9370,"AM":14.2200,"name":"NGC4585","t":"Ga"},{"RA":234.9045,"DE":59.3319,"AM":14.2200,"name":"NGC5985","t":"Ga"},{"RA":156.9270,"DE":-40.0026,"AM":14.2300,"name":"NGC3250C","t":"Ga"},{"RA":174.0257,"DE":45.2836,"AM":14.2300,"name":"NGC3741","t":"Ga"},{"RA":357.7441,"DE":27.1474,"AM":14.2300,"name":"NGC7768","t":"Ga"},{"RA":186.3133,"DE":12.7146,"AM":14.2400,"name":"IC3303","t":"Ga"},{"RA":187.1738,"DE":12.9159,"AM":14.2400,"name":"IC3393","t":"Ga"},{"RA":134.7103,"DE":6.2930,"AM":14.2400,"name":"NGC2718","t":"Ga"},{"RA":150.5293,"DE":3.0577,"AM":14.2500,"name":"IC0588","t":"Ga"},{"RA":145.8000,"DE":31.9287,"AM":14.2500,"name":"NGC2968","t":"Ga"},{"RA":191.5656,"DE":-41.7060,"AM":14.2500,"name":"NGC4672","t":"Ga"},{"RA":122.5253,"DE":24.9221,"AM":14.2600,"name":"IC0497","t":"Ga"},{"RA":37.9625,"DE":-36.6721,"AM":14.2600,"name":"IC1816","t":"Ga"},{"RA":194.7334,"DE":27.8334,"AM":14.2600,"name":"IC3949","t":"Ga"},{"RA":332.5416,"DE":-36.0886,"AM":14.2700,"name":"IC5169","t":"Ga"},{"RA":194.9834,"DE":28.0347,"AM":14.2700,"name":"NGC4883","t":"Ga"},{"RA":234.7257,"DE":17.0262,"AM":14.2700,"name":"NGC5972","t":"Ga"},{"RA":201.6851,"DE":-30.3624,"AM":14.2800,"name":"IC4247","t":"Ga"},{"RA":38.6574,"DE":-8.7876,"AM":14.2800,"name":"NGC0985","t":"Ga"},{"RA":300.2721,"DE":-47.0591,"AM":14.2800,"name":"NGC6845B","t":"Ga"},{"RA":195.0185,"DE":27.9876,"AM":14.2900,"name":"NGC4886","t":"Ga"},{"RA":349.8752,"DE":9.5082,"AM":14.2900,"name":"NGC7609 NED01","t":"Ga"},{"RA":195.9441,"DE":19.2715,"AM":14.3000,"name":"IC4130","t":"Ga"},{"RA":273.4151,"DE":-57.7254,"AM":14.3000,"name":"IC4687","t":"Ga"},{"RA":210.4245,"DE":33.8238,"AM":14.3000,"name":"NGC5421","t":"Ga"},{"RA":333.6875,"DE":13.8465,"AM":14.3000,"name":"NGC7236","t":"Ga"},{"RA":194.7751,"DE":27.9967,"AM":14.3100,"name":"IC3955","t":"Ga"},{"RA":88.9431,"DE":-69.5608,"AM":14.3200,"name":"NGC2150","t":"Ga"},{"RA":182.7067,"DE":39.4727,"AM":14.3200,"name":"NGC4156","t":"Ga"},{"RA":192.2840,"DE":-11.4099,"AM":14.3200,"name":"NGC4700","t":"Ga"},{"RA":234.9882,"DE":-30.5528,"AM":14.3200,"name":"NGC5968","t":"Ga"},{"RA":287.0682,"DE":50.9332,"AM":14.3200,"name":"NGC6764","t":"Ga"},{"RA":195.0754,"DE":27.9566,"AM":14.3300,"name":"NGC4898B","t":"Ga"},{"RA":254.8354,"DE":29.9464,"AM":14.3300,"name":"NGC6274 NED01","t":"Ga"},{"RA":345.1993,"DE":-12.9185,"AM":14.3300,"name":"NGC7450","t":"Ga"},{"RA":182.3230,"DE":44.0902,"AM":14.3400,"name":"NGC4137","t":"Ga"},{"RA":10.7659,"DE":-22.2469,"AM":14.3500,"name":"IC1574","t":"Ga"},{"RA":194.9158,"DE":28.9266,"AM":14.3600,"name":"IC3991","t":"Ga"},{"RA":303.8589,"DE":-61.8577,"AM":14.3600,"name":"IC4974 NED01","t":"Ga"},{"RA":354.0587,"DE":2.1552,"AM":14.3600,"name":"NGC7714","t":"Ga"},{"RA":213.3120,"DE":-3.2076,"AM":14.3800,"name":"NGC5506","t":"Ga"},{"RA":179.7192,"DE":42.5703,"AM":14.3900,"name":"IC0751","t":"Ga"},{"RA":157.2766,"DE":-35.5952,"AM":14.3900,"name":"NGC3260","t":"Ga"},{"RA":80.4790,"DE":3.3420,"AM":14.4000,"name":"IC0414","t":"Ga"},{"RA":196.3645,"DE":-49.4682,"AM":14.4000,"name":"NGC4945","t":"Ga"},{"RA":43.8008,"DE":0.1836,"AM":14.4100,"name":"NGC1144","t":"Ga"},{"RA":194.8725,"DE":27.8501,"AM":14.4200,"name":"IC3976","t":"Ga"},{"RA":342.4409,"DE":-68.6907,"AM":14.4200,"name":"IC5256","t":"Ga"},{"RA":192.7572,"DE":28.9280,"AM":14.4200,"name":"NGC4735","t":"Ga"},{"RA":345.5143,"DE":27.0526,"AM":14.4200,"name":"NGC7466","t":"Ga"},{"RA":355.1915,"DE":-20.5088,"AM":14.4200,"name":"NGC7730","t":"Ga"},{"RA":285.7488,"DE":-56.1597,"AM":14.4400,"name":"IC4810","t":"Ga"},{"RA":181.1237,"DE":20.3162,"AM":14.4400,"name":"NGC4074","t":"Ga"},{"RA":47.0450,"DE":-22.9608,"AM":14.4500,"name":"NGC1229","t":"Ga"},{"RA":170.8845,"DE":-8.6586,"AM":14.4500,"name":"NGC3660","t":"Ga"},{"RA":350.9893,"DE":16.7773,"AM":14.4500,"name":"NGC7647","t":"Ga"},{"RA":194.7832,"DE":27.8550,"AM":14.4700,"name":"IC3960","t":"Ga"},{"RA":189.5189,"DE":33.4588,"AM":14.4700,"name":"NGC4583","t":"Ga"},{"RA":20.5120,"DE":5.3672,"AM":14.4800,"name":"NGC0490","t":"Ga"},{"RA":159.0715,"DE":-27.5297,"AM":14.4800,"name":"NGC3307","t":"Ga"},{"RA":20.9878,"DE":-35.0693,"AM":14.5000,"name":"NGC0526B","t":"Ga"},{"RA":146.3551,"DE":-18.3739,"AM":14.5000,"name":"NGC2989","t":"Ga"},{"RA":343.1636,"DE":-9.2678,"AM":14.5000,"name":"NGC7399","t":"Ga"},{"RA":340.3121,"DE":-21.7985,"AM":14.5100,"name":"NGC7349","t":"Ga"},{"RA":351.6035,"DE":-39.2266,"AM":14.5200,"name":"NGC7658B","t":"Ga"},{"RA":186.7628,"DE":12.5608,"AM":14.5400,"name":"IC3363","t":"Ga"},{"RA":66.6410,"DE":-53.1873,"AM":14.5500,"name":"IC2073","t":"Ga"},{"RA":194.5627,"DE":28.1259,"AM":14.5600,"name":"IC0839","t":"Ga"},{"RA":187.9639,"DE":12.6570,"AM":14.5600,"name":"IC3457","t":"Ga"},{"RA":201.7773,"DE":-27.9564,"AM":14.5700,"name":"IC4249","t":"Ga"},{"RA":194.9080,"DE":27.9073,"AM":14.5700,"name":"NGC4875","t":"Ga"},{"RA":17.1296,"DE":33.1092,"AM":14.5800,"name":"NGC0397","t":"Ga"},{"RA":20.9766,"DE":-35.0655,"AM":14.6000,"name":"NGC0526A","t":"Ga"},{"RA":135.9272,"DE":29.2960,"AM":14.6100,"name":"IC2429","t":"Ga"},{"RA":194.7171,"DE":27.7851,"AM":14.6100,"name":"IC3947","t":"Ga"},{"RA":194.9449,"DE":27.9739,"AM":14.6100,"name":"IC3998","t":"Ga"},{"RA":159.8516,"DE":0.3893,"AM":14.6200,"name":"IC0633","t":"Ga"},{"RA":258.1613,"DE":23.2701,"AM":14.6200,"name":"NGC6314","t":"Ga"},{"RA":195.0923,"DE":28.0470,"AM":14.6300,"name":"IC4026","t":"Ga"},{"RA":282.0471,"DE":-53.1476,"AM":14.6300,"name":"IC4777","t":"Ga"},{"RA":294.4067,"DE":-65.8118,"AM":14.6300,"name":"IC4870","t":"Ga"},{"RA":195.0333,"DE":28.0786,"AM":14.6400,"name":"IC4012","t":"Ga"},{"RA":142.0743,"DE":29.7061,"AM":14.6500,"name":"IC2477","t":"Ga"},{"RA":187.8503,"DE":28.8552,"AM":14.6500,"name":"IC3451","t":"Ga"},{"RA":195.3552,"DE":29.3138,"AM":14.6700,"name":"NGC4922 NED02","t":"Ga"},{"RA":197.6985,"DE":29.7099,"AM":14.6700,"name":"NGC5004B","t":"Ga"},{"RA":195.1069,"DE":28.8678,"AM":14.6800,"name":"IC4032","t":"Ga"},{"RA":0.6103,"DE":3.3519,"AM":14.6800,"name":"NGC7811","t":"Ga"},{"RA":23.5106,"DE":-9.7741,"AM":14.7000,"name":"NGC0617","t":"Ga"},{"RA":139.9395,"DE":33.7450,"AM":14.7000,"name":"NGC2831","t":"Ga"},{"RA":146.3436,"DE":68.6083,"AM":14.7000,"name":"NGC2961","t":"Ga"},{"RA":194.7812,"DE":27.7678,"AM":14.7200,"name":"IC3957","t":"Ga"},{"RA":194.8062,"DE":27.7746,"AM":14.7200,"name":"IC3963","t":"Ga"},{"RA":356.9377,"DE":-28.1408,"AM":14.7200,"name":"IC5358","t":"Ga"},{"RA":61.7627,"DE":-55.3238,"AM":14.7300,"name":"IC2032","t":"Ga"},{"RA":183.6539,"DE":12.8119,"AM":14.7300,"name":"IC3056","t":"Ga"},{"RA":187.1169,"DE":12.8237,"AM":14.7300,"name":"IC3388","t":"Ga"},{"RA":199.2642,"DE":-2.2613,"AM":14.7300,"name":"IC4218","t":"Ga"},{"RA":63.0178,"DE":-58.5570,"AM":14.7400,"name":"IC2049","t":"Ga"},{"RA":37.0603,"DE":31.3117,"AM":14.7400,"name":"NGC0931","t":"Ga"},{"RA":132.0435,"DE":29.4914,"AM":14.7500,"name":"IC2404","t":"Ga"},{"RA":195.0614,"DE":28.0413,"AM":14.7500,"name":"IC4021","t":"Ga"},{"RA":337.2029,"DE":-22.2025,"AM":14.7500,"name":"NGC7287","t":"Ga"},{"RA":195.1580,"DE":28.0574,"AM":14.7600,"name":"IC4040","t":"Ga"},{"RA":170.4271,"DE":34.3628,"AM":14.7700,"name":"IC2744","t":"Ga"},{"RA":195.1702,"DE":27.9966,"AM":14.7700,"name":"IC4041","t":"Ga"},{"RA":111.2368,"DE":-9.6593,"AM":14.7700,"name":"NGC2377","t":"Ga"},{"RA":39.9048,"DE":10.8437,"AM":14.7900,"name":"NGC1028","t":"Ga"},{"RA":196.7749,"DE":-23.6770,"AM":14.7900,"name":"NGC4968","t":"Ga"},{"RA":75.4334,"DE":-4.2888,"AM":14.8000,"name":"IC0399","t":"Ga"},{"RA":201.6968,"DE":-29.8814,"AM":14.8000,"name":"IC4248","t":"Ga"},{"RA":42.3363,"DE":19.3039,"AM":14.8100,"name":"IC1854","t":"Ga"},{"RA":301.4164,"DE":-47.9791,"AM":14.8100,"name":"NGC6851B","t":"Ga"},{"RA":344.5081,"DE":13.1345,"AM":14.8100,"name":"NGC7432","t":"Ga"},{"RA":10.8890,"DE":-4.1178,"AM":14.8500,"name":"IC1575","t":"Ga"},{"RA":186.7131,"DE":13.1757,"AM":14.8600,"name":"IC3355","t":"Ga"},{"RA":3.9927,"DE":0.3035,"AM":14.8600,"name":"NGC0060","t":"Ga"},{"RA":167.2382,"DE":26.5961,"AM":14.8600,"name":"NGC3534B","t":"Ga"},{"RA":54.0577,"DE":-45.1796,"AM":14.8800,"name":"IC1969","t":"Ga"},{"RA":188.0114,"DE":11.8901,"AM":14.8800,"name":"IC3461","t":"Ga"},{"RA":242.0881,"DE":28.4787,"AM":14.9000,"name":"IC4590","t":"Ga"},{"RA":119.6171,"DE":37.7866,"AM":14.9000,"name":"NGC2484","t":"Ga"},{"RA":232.8253,"DE":7.4577,"AM":14.9000,"name":"NGC5940","t":"Ga"},{"RA":128.3464,"DE":29.5388,"AM":14.9200,"name":"NGC2604","t":"Ga"},{"RA":242.1515,"DE":12.3309,"AM":14.9400,"name":"IC1198","t":"Ga"},{"RA":194.5905,"DE":28.1487,"AM":14.9400,"name":"NGC4851","t":"Ga"},{"RA":195.0380,"DE":28.1704,"AM":14.9400,"name":"NGC4895A","t":"Ga"},{"RA":187.8155,"DE":12.3318,"AM":14.9500,"name":"IC3443","t":"Ga"},{"RA":39.6142,"DE":1.9077,"AM":14.9500,"name":"NGC1019","t":"Ga"},{"RA":19.0302,"DE":33.0896,"AM":14.9600,"name":"NGC0449","t":"Ga"},{"RA":196.0747,"DE":29.0295,"AM":14.9700,"name":"NGC4949","t":"Ga"},{"RA":297.3817,"DE":-70.2274,"AM":14.9800,"name":"IC4892","t":"Ga"},{"RA":214.3760,"DE":28.8000,"AM":14.9900,"name":"IC4396","t":"Ga"},{"RA":195.3522,"DE":29.3084,"AM":14.9900,"name":"NGC4922 NED01","t":"Ga"},{"RA":131.9711,"DE":53.8762,"AM":15.0000,"name":"NGC2656","t":"Ga"},{"RA":148.4943,"DE":-27.2863,"AM":15.0000,"name":"NGC3051","t":"Ga"},{"RA":193.7653,"DE":-12.4972,"AM":15.0000,"name":"NGC4792","t":"Ga"},{"RA":241.5668,"DE":18.2499,"AM":15.0000,"name":"NGC6061","t":"Ga"},{"RA":344.4840,"DE":26.1500,"AM":15.0000,"name":"NGC7436A","t":"Ga"},{"RA":349.5908,"DE":-4.4158,"AM":15.0000,"name":"NGC7592A","t":"Ga"},{"RA":36.4618,"DE":18.4962,"AM":15.0100,"name":"NGC0918","t":"Ga"},{"RA":194.7585,"DE":28.1157,"AM":15.0200,"name":"NGC4858","t":"Ga"},{"RA":195.0688,"DE":27.9675,"AM":15.0400,"name":"NGC4894","t":"Ga"},{"RA":195.0266,"DE":28.0041,"AM":15.0500,"name":"IC4011","t":"Ga"},{"RA":185.5811,"DE":28.8316,"AM":15.1000,"name":"IC3222","t":"Ga"},{"RA":187.7684,"DE":28.8527,"AM":15.1100,"name":"IC3441","t":"Ga"},{"RA":34.6133,"DE":-4.2058,"AM":15.1100,"name":"NGC0880","t":"Ga"},{"RA":187.2472,"DE":28.8619,"AM":15.1600,"name":"IC3402","t":"Ga"},{"RA":187.0513,"DE":10.2977,"AM":15.1800,"name":"IC3383","t":"Ga"},{"RA":73.1426,"DE":-2.9493,"AM":15.1800,"name":"NGC1685","t":"Ga"},{"RA":241.4033,"DE":17.8021,"AM":15.1900,"name":"IC1182","t":"Ga"},{"RA":22.2144,"DE":2.4464,"AM":15.2100,"name":"IC0123","t":"Ga"},{"RA":55.2948,"DE":-1.2988,"AM":15.2200,"name":"NGC1410","t":"Ga"},{"RA":195.1183,"DE":27.9724,"AM":15.2300,"name":"IC4033","t":"Ga"},{"RA":195.1165,"DE":27.9560,"AM":15.2700,"name":"IC4030","t":"Ga"},{"RA":188.3324,"DE":12.8534,"AM":15.3000,"name":"IC3492","t":"Ga"},{"RA":194.8562,"DE":27.9732,"AM":15.3200,"name":"IC3968","t":"Ga"},{"RA":58.4428,"DE":19.9739,"AM":15.4000,"name":"IC0355","t":"Ga"},{"RA":188.1024,"DE":11.7876,"AM":15.4000,"name":"IC3467","t":"Ga"},{"RA":189.1570,"DE":6.6209,"AM":15.4000,"name":"IC3576","t":"Ga"},{"RA":347.8221,"DE":-32.4519,"AM":15.4000,"name":"IC5289 NED02","t":"Ga"},{"RA":343.9869,"DE":-63.6947,"AM":15.4100,"name":"NGC7408","t":"Ga"},{"RA":187.0987,"DE":13.1958,"AM":15.4700,"name":"IC3386","t":"Ga"},{"RA":195.1975,"DE":27.9222,"AM":15.4700,"name":"IC4044","t":"Ga"},{"RA":44.9608,"DE":2.7714,"AM":15.5000,"name":"IC0277","t":"Ga"},{"RA":2.4970,"DE":-57.0208,"AM":15.5000,"name":"NGC0025","t":"Ga"},{"RA":34.2133,"DE":-8.9640,"AM":15.5000,"name":"NGC0879","t":"Ga"},{"RA":212.4887,"DE":17.5456,"AM":15.5000,"name":"NGC5490","t":"Ga"},{"RA":231.7434,"DE":28.8526,"AM":15.5400,"name":"IC4546","t":"Ga"},{"RA":255.3071,"DE":33.5132,"AM":15.5400,"name":"IC4638","t":"Ga"},{"RA":18.2025,"DE":0.2902,"AM":15.5800,"name":"NGC0426","t":"Ga"},{"RA":221.5463,"DE":0.2229,"AM":15.5800,"name":"NGC5750","t":"Ga"},{"RA":315.4070,"DE":-28.0319,"AM":15.6000,"name":"NGC6998","t":"Ga"},{"RA":187.8310,"DE":12.7380,"AM":15.8700,"name":"IC3445","t":"Ga"},{"RA":187.4044,"DE":7.9328,"AM":15.9200,"name":"NGC4471","t":"Ga"},{"RA":188.5281,"DE":12.7416,"AM":15.9300,"name":"IC3506","t":"Ga"},{"RA":205.0767,"DE":-28.8922,"AM":15.9300,"name":"IC4316","t":"Ga"},{"RA":224.2783,"DE":49.6690,"AM":15.9400,"name":"NGC5804","t":"Ga"},{"RA":83.8583,"DE":-5.9099,"AM":2.5000,"name":"NGC1980","t":"Ne"},{"RA":100.2427,"DE":9.8955,"AM":3.9000,"name":"NGC2264","t":"Ne"},{"RA":83.8187,"DE":-5.3897,"AM":4.0000,"name":"M42","t":"Ne"},{"RA":83.7900,"DE":-4.4251,"AM":4.2000,"name":"NGC1981","t":"Ne"},{"RA":271.1293,"DE":-24.3581,"AM":4.6000,"name":"NGC6530","t":"Ne"},{"RA":97.9815,"DE":4.9429,"AM":4.8000,"name":"NGC2239","t":"Ne"},{"RA":270.9220,"DE":-24.3802,"AM":5.8000,"name":"M8","t":"Ne"},{"RA":254.4836,"DE":-45.9366,"AM":5.9000,"name":"NGC6250","t":"Ne"},{"RA":274.7343,"DE":-13.8454,"AM":6.0000,"name":"IC4703","t":"Ne"},{"RA":274.7007,"DE":-13.8072,"AM":6.0000,"name":"M16","t":"Ne"},{"RA":38.1730,"DE":61.4569,"AM":6.5000,"name":"IC1805","t":"Ne"},{"RA":42.7941,"DE":60.4025,"AM":6.5000,"name":"IC1848","t":"Ne"},{"RA":159.3175,"DE":-58.6196,"AM":6.7000,"name":"NGC3324","t":"Ne"},{"RA":248.4243,"DE":-48.0801,"AM":6.7100,"name":"NGC6164","t":"Ne"},{"RA":248.5144,"DE":-48.1505,"AM":6.7100,"name":"NGC6165","t":"Ne"},{"RA":92.4148,"DE":20.4876,"AM":6.8000,"name":"NGC2175","t":"Ne"},{"RA":275.1963,"DE":-16.1715,"AM":7.0000,"name":"M17","t":"Ne"},{"RA":295.7912,"DE":23.2999,"AM":7.1000,"name":"NGC6823","t":"Ne"},{"RA":328.3698,"DE":47.2669,"AM":7.2000,"name":"IC5146","t":"Ne"},{"RA":341.8375,"DE":58.1324,"AM":7.2000,"name":"NGC7380","t":"Ne"},{"RA":84.6765,"DE":-69.1009,"AM":7.2500,"name":"NGC2070","t":"Ne"},{"RA":337.4107,"DE":-20.8373,"AM":7.3000,"name":"NGC7293","t":"Ne"},{"RA":299.9016,"DE":22.7210,"AM":7.4000,"name":"M27","t":"Ne"},{"RA":156.0583,"DE":-57.7633,"AM":7.6000,"name":"NGC3247","t":"Ne"},{"RA":156.1920,"DE":-18.6422,"AM":7.7000,"name":"NGC3242","t":"Ne"},{"RA":86.6909,"DE":0.0793,"AM":8.0000,"name":"M78","t":"Ne"},{"RA":316.0450,"DE":-11.3633,"AM":8.0000,"name":"NGC7009","t":"Ne"},{"RA":177.5748,"DE":-57.1823,"AM":8.1000,"name":"NGC3918","t":"Ne"},{"RA":273.0259,"DE":6.8537,"AM":8.1000,"name":"NGC6572","t":"Ne"},{"RA":351.4746,"DE":42.5349,"AM":8.3000,"name":"NGC7662","t":"Ne"},{"RA":83.6332,"DE":22.0145,"AM":8.4000,"name":"M1","t":"Ne"},{"RA":270.6755,"DE":-22.9719,"AM":8.5000,"name":"M20","t":"Ne"},{"RA":316.7564,"DE":42.2365,"AM":8.5000,"name":"NGC7027","t":"Ne"},{"RA":283.3959,"DE":33.0286,"AM":8.8000,"name":"M57","t":"Ne"},{"RA":81.5415,"DE":-67.4974,"AM":8.8700,"name":"NGC1955","t":"Ne"},{"RA":83.0828,"DE":-67.6898,"AM":8.9700,"name":"NGC2014","t":"Ne"},{"RA":83.8808,"DE":-5.2675,"AM":9.0000,"name":"M43","t":"Ne"},{"RA":269.6391,"DE":66.6332,"AM":9.0100,"name":"NGC6543","t":"Ne"},{"RA":151.7572,"DE":-40.4366,"AM":9.2000,"name":"NGC3132","t":"Ne"},{"RA":295.9905,"DE":-14.1532,"AM":9.3000,"name":"NGC6818","t":"Ne"},{"RA":53.3110,"DE":-25.8717,"AM":9.4000,"name":"NGC1360","t":"Ne"},{"RA":74.2050,"DE":-66.4091,"AM":9.4000,"name":"NGC1763","t":"Ne"},{"RA":115.4807,"DE":-18.2085,"AM":9.4000,"name":"NGC2440","t":"Ne"},{"RA":81.8675,"DE":-12.6973,"AM":9.4400,"name":"IC0418","t":"Ne"},{"RA":296.2005,"DE":50.5250,"AM":9.4400,"name":"NGC6826","t":"Ne"},{"RA":84.4454,"DE":-69.1717,"AM":9.5900,"name":"NGC2060","t":"Ne"},{"RA":63.5657,"DE":-12.7394,"AM":9.6000,"name":"NGC1535","t":"Ne"},{"RA":258.4360,"DE":-37.1031,"AM":9.6000,"name":"NGC6302","t":"Ne"},{"RA":112.2948,"DE":20.9118,"AM":9.6100,"name":"NGC2392","t":"Ne"},{"RA":79.6795,"DE":-69.2319,"AM":9.6500,"name":"NGC1910","t":"Ne"},{"RA":251.1230,"DE":23.7998,"AM":9.6500,"name":"NGC6210","t":"Ne"},{"RA":140.3540,"DE":-58.3117,"AM":9.7000,"name":"NGC2867","t":"Ne"},{"RA":208.4870,"DE":-66.5142,"AM":9.8000,"name":"NGC5315","t":"Ne"},{"RA":77.4664,"DE":-68.8912,"AM":9.8800,"name":"NGC1858","t":"Ne"},{"RA":168.6988,"DE":55.0190,"AM":9.9000,"name":"M97","t":"Ne"},{"RA":314.1644,"DE":44.6315,"AM":10.0000,"name":"NGC6997","t":"Ne"},{"RA":78.4657,"DE":-67.4526,"AM":10.0900,"name":"NGC1871","t":"Ne"},{"RA":25.5820,"DE":51.5755,"AM":10.1000,"name":"M76","t":"Ne"},{"RA":82.8556,"DE":34.2466,"AM":10.1000,"name":"NGC1931","t":"Ne"},{"RA":84.6935,"DE":-68.9744,"AM":10.1000,"name":"NGC2069","t":"Ne"},{"RA":229.2083,"DE":-45.6493,"AM":10.1800,"name":"NGC5882","t":"Ne"},{"RA":62.3206,"DE":30.7759,"AM":10.1900,"name":"NGC1514","t":"Ne"},{"RA":215.6103,"DE":-44.1502,"AM":10.2000,"name":"IC4406","t":"Ne"},{"RA":152.3370,"DE":-62.6137,"AM":10.3000,"name":"IC2553","t":"Ne"},{"RA":136.7761,"DE":-69.9418,"AM":10.4000,"name":"IC2448","t":"Ne"},{"RA":144.6966,"DE":-60.0919,"AM":10.4000,"name":"IC2501","t":"Ne"},{"RA":84.9409,"DE":-69.6441,"AM":10.4200,"name":"NGC2080","t":"Ne"},{"RA":87.2188,"DE":-70.0701,"AM":10.4300,"name":"NGC2122","t":"Ne"},{"RA":78.4820,"DE":-67.3344,"AM":10.4400,"name":"NGC1873","t":"Ne"},{"RA":95.4279,"DE":-12.9872,"AM":10.5000,"name":"IC2165","t":"Ne"},{"RA":305.0367,"DE":16.7317,"AM":10.5000,"name":"IC4997","t":"Ne"},{"RA":80.4495,"DE":-67.9372,"AM":10.5000,"name":"NGC1934","t":"Ne"},{"RA":290.7371,"DE":1.5133,"AM":10.5000,"name":"NGC6790","t":"Ne"},{"RA":303.7868,"DE":12.7044,"AM":10.5000,"name":"NGC6891","t":"Ne"},{"RA":188.2782,"DE":82.5639,"AM":10.6000,"name":"IC3568","t":"Ne"},{"RA":197.1968,"DE":-67.6437,"AM":10.6000,"name":"IC4191","t":"Ne"},{"RA":81.4427,"DE":-66.2668,"AM":10.6100,"name":"NGC1948","t":"Ne"},{"RA":289.3475,"DE":-39.6131,"AM":10.7000,"name":"IC1297","t":"Ne"},{"RA":242.9354,"DE":12.0714,"AM":10.7000,"name":"IC4593","t":"Ne"},{"RA":154.4605,"DE":-62.6701,"AM":10.7000,"name":"NGC3211","t":"Ne"},{"RA":278.1447,"DE":-25.1294,"AM":10.7000,"name":"NGC6644","t":"Ne"},{"RA":315.1367,"DE":54.5432,"AM":10.7000,"name":"NGC7008","t":"Ne"},{"RA":89.0995,"DE":46.1048,"AM":10.7800,"name":"IC2149","t":"Ne"},{"RA":281.4612,"DE":-33.3431,"AM":10.8000,"name":"IC4776","t":"Ne"},{"RA":115.4600,"DE":-14.7358,"AM":10.8000,"name":"NGC2438","t":"Ne"},{"RA":85.4181,"DE":-71.3331,"AM":10.8200,"name":"NGC2103","t":"Ne"},{"RA":84.9968,"DE":-69.7376,"AM":10.8300,"name":"NGC2083","t":"Ne"},{"RA":82.8537,"DE":-71.0691,"AM":10.8900,"name":"NGC2018","t":"Ne"},{"RA":84.9144,"DE":-69.7432,"AM":10.8900,"name":"NGC2078","t":"Ne"},{"RA":255.3900,"DE":-21.8260,"AM":10.9000,"name":"IC4634","t":"Ne"},{"RA":11.7640,"DE":-11.8719,"AM":10.9000,"name":"NGC0246","t":"Ne"},{"RA":186.1282,"DE":-18.7848,"AM":10.9000,"name":"NGC4361","t":"Ne"},{"RA":247.8777,"DE":-40.2534,"AM":10.9000,"name":"NGC6153","t":"Ne"},{"RA":302.5987,"DE":46.4608,"AM":10.9000,"name":"NGC6884","t":"Ne"},{"RA":316.5770,"DE":47.8522,"AM":10.9000,"name":"NGC7026","t":"Ne"},{"RA":83.8800,"DE":-67.5842,"AM":10.9900,"name":"NGC2035","t":"Ne"},{"RA":329.8967,"DE":-39.3858,"AM":11.0000,"name":"IC5148","t":"Ne"},{"RA":228.2117,"DE":-38.1256,"AM":11.0000,"name":"NGC5873","t":"Ne"},{"RA":273.0104,"DE":-33.8683,"AM":11.0000,"name":"NGC6563","t":"Ne"},{"RA":273.4383,"DE":-19.0758,"AM":11.0000,"name":"NGC6567","t":"Ne"},{"RA":80.6840,"DE":-68.0611,"AM":11.1000,"name":"IC2128","t":"Ne"},{"RA":305.5958,"DE":20.1045,"AM":11.1000,"name":"NGC6905","t":"Ne"},{"RA":266.3971,"DE":-46.0899,"AM":11.2000,"name":"IC1266","t":"Ne"},{"RA":165.0833,"DE":-65.2494,"AM":11.2000,"name":"IC2621","t":"Ne"},{"RA":111.3944,"DE":29.4906,"AM":11.2000,"name":"NGC2371","t":"Ne"},{"RA":207.7637,"DE":-51.2058,"AM":11.2000,"name":"NGC5307","t":"Ne"},{"RA":267.3127,"DE":-20.0095,"AM":11.2000,"name":"NGC6445","t":"Ne"},{"RA":80.3919,"DE":-65.4867,"AM":11.2400,"name":"NGC1923","t":"Ne"},{"RA":73.5111,"DE":-69.1986,"AM":11.2600,"name":"NGC1743","t":"Ne"},{"RA":72.3611,"DE":-69.2009,"AM":11.3000,"name":"IC2105","t":"Ne"},{"RA":335.9821,"DE":50.9667,"AM":11.3000,"name":"IC5217","t":"Ne"},{"RA":171.9881,"DE":-59.9581,"AM":11.3000,"name":"NGC3699","t":"Ne"},{"RA":276.4269,"DE":-23.2029,"AM":11.3000,"name":"NGC6629","t":"Ne"},{"RA":59.0918,"DE":33.8749,"AM":11.4000,"name":"IC2003","t":"Ne"},{"RA":262.3354,"DE":-23.7594,"AM":11.4000,"name":"NGC6369","t":"Ne"},{"RA":289.6178,"DE":6.5397,"AM":11.4000,"name":"NGC6781","t":"Ne"},{"RA":292.8185,"DE":10.0560,"AM":11.4000,"name":"NGC6803","t":"Ne"},{"RA":303.1788,"DE":19.9897,"AM":11.4000,"name":"NGC6886","t":"Ne"},{"RA":84.0247,"DE":-67.5686,"AM":11.4700,"name":"NGC2040","t":"Ne"},{"RA":84.5890,"DE":-70.6850,"AM":11.4700,"name":"NGC2075","t":"Ne"},{"RA":67.7126,"DE":35.4462,"AM":11.4900,"name":"IC2067","t":"Ne"},{"RA":323.1290,"DE":44.5966,"AM":11.5000,"name":"IC5117","t":"Ne"},{"RA":61.7474,"DE":60.9207,"AM":11.5000,"name":"NGC1501","t":"Ne"},{"RA":236.9211,"DE":-61.2179,"AM":11.5000,"name":"NGC5979","t":"Ne"},{"RA":258.5179,"DE":-12.9106,"AM":11.5000,"name":"NGC6309","t":"Ne"},{"RA":285.6542,"DE":0.4494,"AM":11.5000,"name":"NGC6741","t":"Ne"},{"RA":325.7460,"DE":66.1130,"AM":11.5000,"name":"NGC7129","t":"Ne"},{"RA":80.5582,"DE":-67.9783,"AM":11.6000,"name":"NGC1936","t":"Ne"},{"RA":85.5259,"DE":9.0865,"AM":11.6000,"name":"NGC2022","t":"Ne"},{"RA":107.3459,"DE":0.8091,"AM":11.6000,"name":"NGC2346","t":"Ne"},{"RA":138.1107,"DE":-42.4275,"AM":11.6000,"name":"NGC2792","t":"Ne"},{"RA":139.0062,"DE":-36.6269,"AM":11.6000,"name":"NGC2818","t":"Ne"},{"RA":152.3374,"DE":-80.8586,"AM":11.6000,"name":"NGC3195","t":"Ne"},{"RA":271.3046,"DE":-19.8430,"AM":11.6000,"name":"NGC6537","t":"Ne"},{"RA":272.9692,"DE":-28.1783,"AM":11.6000,"name":"NGC6565","t":"Ne"},{"RA":73.0369,"DE":-66.9234,"AM":11.6100,"name":"NGC1714","t":"Ne"},{"RA":17.3042,"DE":-73.1941,"AM":11.7000,"name":"IC1644","t":"Ne"},{"RA":243.2425,"DE":-36.2300,"AM":11.7000,"name":"NGC6072","t":"Ne"},{"RA":78.3276,"DE":-69.3621,"AM":11.7100,"name":"NGC1876","t":"Ne"},{"RA":84.9001,"DE":-69.6571,"AM":11.7100,"name":"NGC2077","t":"Ne"},{"RA":70.1521,"DE":50.4617,"AM":11.8000,"name":"NGC1624","t":"Ne"},{"RA":141.7623,"DE":-56.1060,"AM":11.8000,"name":"NGC2899","t":"Ne"},{"RA":84.9067,"DE":-69.7572,"AM":11.8100,"name":"NGC2079","t":"Ne"},{"RA":99.7896,"DE":8.7443,"AM":11.8500,"name":"NGC2261","t":"Ne"},{"RA":3.2543,"DE":72.5219,"AM":11.8900,"name":"NGC0040","t":"Ne"},{"RA":56.8875,"DE":35.0469,"AM":11.9000,"name":"IC0351","t":"Ne"},{"RA":289.1179,"DE":-9.0436,"AM":11.9000,"name":"IC4846","t":"Ne"},{"RA":286.4815,"DE":-5.9923,"AM":11.9000,"name":"NGC6751","t":"Ne"},{"RA":29.3989,"DE":63.3218,"AM":12.0000,"name":"IC1747","t":"Ne"},{"RA":85.1031,"DE":-69.6703,"AM":12.0000,"name":"IC2145","t":"Ne"},{"RA":80.7821,"DE":-66.3786,"AM":12.0000,"name":"NGC1941","t":"Ne"},{"RA":85.0537,"DE":-69.6679,"AM":12.0000,"name":"NGC2086","t":"Ne"},{"RA":116.8599,"DE":-27.3340,"AM":12.0000,"name":"NGC2452","t":"Ne"},{"RA":292.8975,"DE":9.2252,"AM":12.0000,"name":"NGC6804","t":"Ne"},{"RA":293.6396,"DE":5.6842,"AM":12.0000,"name":"NGC6807","t":"Ne"},{"RA":79.4157,"DE":-71.2559,"AM":12.0100,"name":"NGC1914","t":"Ne"},{"RA":107.1617,"DE":-4.3180,"AM":12.0600,"name":"IC0466","t":"Ne"},{"RA":85.0410,"DE":-69.6728,"AM":12.0600,"name":"NGC2085","t":"Ne"},{"RA":278.4775,"DE":-22.6447,"AM":12.1000,"name":"IC4732","t":"Ne"},{"RA":297.4442,"DE":48.9611,"AM":12.1000,"name":"NGC6833","t":"Ne"},{"RA":318.5633,"DE":46.2886,"AM":12.1000,"name":"NGC7048","t":"Ne"},{"RA":83.9816,"DE":-69.6485,"AM":12.1700,"name":"NGC2048","t":"Ne"},{"RA":340.0817,"DE":61.2848,"AM":12.2000,"name":"NGC7354","t":"Ne"},{"RA":83.7489,"DE":-67.5564,"AM":12.2900,"name":"NGC2030","t":"Ne"},{"RA":73.6082,"DE":-69.1841,"AM":12.3000,"name":"NGC1748","t":"Ne"},{"RA":260.5650,"DE":-38.4837,"AM":12.3000,"name":"NGC6337","t":"Ne"},{"RA":289.6035,"DE":-1.5964,"AM":12.3000,"name":"NGC6778","t":"Ne"},{"RA":304.1002,"DE":30.5651,"AM":12.3000,"name":"NGC6894","t":"Ne"},{"RA":81.2701,"DE":-68.4725,"AM":12.3900,"name":"NGC1949","t":"Ne"},{"RA":283.6547,"DE":-8.8270,"AM":12.5000,"name":"IC1295","t":"Ne"},{"RA":256.2951,"DE":-40.8864,"AM":12.5000,"name":"IC4637","t":"Ne"},{"RA":266.3675,"DE":-44.9049,"AM":12.5000,"name":"IC4663","t":"Ne"},{"RA":302.6108,"DE":16.9228,"AM":12.5000,"name":"NGC6879","t":"Ne"},{"RA":80.1396,"DE":-66.7787,"AM":12.5400,"name":"NGC1920","t":"Ne"},{"RA":267.0825,"DE":-16.4789,"AM":12.6000,"name":"NGC6439","t":"Ne"},{"RA":300.1632,"DE":1.7281,"AM":12.6000,"name":"NGC6852","t":"Ne"},{"RA":128.3475,"DE":-16.1494,"AM":12.7000,"name":"NGC2610","t":"Ne"},{"RA":275.7256,"DE":-26.8217,"AM":12.7000,"name":"NGC6620","t":"Ne"},{"RA":288.6513,"DE":-2.7068,"AM":12.7000,"name":"NGC6772","t":"Ne"},{"RA":75.9436,"DE":-67.3007,"AM":12.7600,"name":"NGC1814","t":"Ne"},{"RA":78.2986,"DE":-69.3762,"AM":12.8100,"name":"NGC1874","t":"Ne"},{"RA":78.3549,"DE":-69.3794,"AM":12.8100,"name":"NGC1880","t":"Ne"},{"RA":240.3371,"DE":-34.5442,"AM":12.9000,"name":"NGC6026","t":"Ne"},{"RA":241.1106,"DE":40.6831,"AM":12.9000,"name":"NGC6058","t":"Ne"},{"RA":274.0687,"DE":-20.4509,"AM":12.9000,"name":"NGC6578","t":"Ne"},{"RA":287.7771,"DE":30.5456,"AM":12.9000,"name":"NGC6765","t":"Ne"},{"RA":79.2150,"DE":-67.3296,"AM":12.9300,"name":"NGC1895","t":"Ne"},{"RA":270.8267,"DE":-27.1061,"AM":13.0000,"name":"IC4673","t":"Ne"},{"RA":274.6366,"DE":-45.9831,"AM":13.0000,"name":"IC4699","t":"Ne"},{"RA":181.0657,"DE":-67.3101,"AM":13.0000,"name":"NGC4071","t":"Ne"},{"RA":298.7594,"DE":29.2892,"AM":13.1000,"name":"NGC6842","t":"Ne"},{"RA":47.5802,"DE":61.3168,"AM":13.2000,"name":"IC0289","t":"Ne"},{"RA":326.5358,"DE":63.7919,"AM":13.3000,"name":"NGC7139","t":"Ne"},{"RA":73.5859,"DE":-69.1589,"AM":13.4000,"name":"NGC1745","t":"Ne"},{"RA":284.8329,"DE":48.4653,"AM":13.4000,"name":"NGC6742","t":"Ne"},{"RA":324.2207,"DE":12.7886,"AM":13.4000,"name":"NGC7094","t":"Ne"},{"RA":321.5979,"DE":62.8925,"AM":13.5000,"name":"NGC7076","t":"Ne"},{"RA":211.1080,"DE":-17.2282,"AM":13.9000,"name":"IC0972","t":"Ne"},{"RA":302.7188,"DE":37.4114,"AM":13.9000,"name":"NGC6881","t":"Ne"},{"RA":340.6042,"DE":80.4422,"AM":14.0000,"name":"IC1454","t":"Ne"},{"RA":23.4814,"DE":30.7578,"AM":14.2000,"name":"IC0142","t":"Ne"},{"RA":74.3178,"DE":-66.3890,"AM":14.2100,"name":"IC2116","t":"Ne"},{"RA":84.6499,"DE":-7.0831,"AM":14.4000,"name":"IC0430","t":"Ne"},{"RA":23.1914,"DE":30.6475,"AM":14.4400,"name":"NGC0588","t":"Ne"},{"RA":23.3163,"DE":30.9456,"AM":14.8200,"name":"IC0132","t":"Ne"},{"RA":98.5302,"DE":44.7770,"AM":15.0000,"name":"NGC2242","t":"Ne"},{"RA":6.0223,"DE":-72.0814,"AM":4.0900,"name":"NGC0104","t":"Gc"},{"RA":254.2875,"DE":-4.0993,"AM":4.9800,"name":"M10","t":"Gc"},{"RA":265.1723,"DE":-53.6737,"AM":5.1700,"name":"NGC6397","t":"Gc"},{"RA":201.6912,"DE":-47.4769,"AM":5.3300,"name":"NGC5139","t":"Gc"},{"RA":245.8975,"DE":-26.5255,"AM":5.4000,"name":"M4","t":"Gc"},{"RA":255.6570,"DE":-26.2679,"AM":5.5700,"name":"M19","t":"Gc"},{"RA":138.0106,"DE":-64.8628,"AM":5.6900,"name":"NGC2808","t":"Gc"},{"RA":264.4007,"DE":-3.2459,"AM":5.7300,"name":"M14","t":"Gc"},{"RA":250.4235,"DE":36.4613,"AM":5.8000,"name":"M13","t":"Gc"},{"RA":229.6406,"DE":2.0827,"AM":5.9500,"name":"M5","t":"Gc"},{"RA":251.8105,"DE":-1.9478,"AM":6.0700,"name":"M12","t":"Gc"},{"RA":298.4421,"DE":18.7784,"AM":6.1000,"name":"M71","t":"Gc"},{"RA":279.1008,"DE":-23.9034,"AM":6.1700,"name":"M22","t":"Gc"},{"RA":323.3625,"DE":0.8233,"AM":6.2500,"name":"M2","t":"Gc"},{"RA":287.7157,"DE":-59.9819,"AM":6.2800,"name":"NGC6752","t":"Gc"},{"RA":322.4932,"DE":12.1668,"AM":6.3000,"name":"M15","t":"Gc"},{"RA":205.5468,"DE":28.3754,"AM":6.3900,"name":"M3","t":"Gc"},{"RA":294.9975,"DE":-30.9621,"AM":6.4900,"name":"M55","t":"Gc"},{"RA":259.2803,"DE":43.1365,"AM":6.5200,"name":"M92","t":"Gc"},{"RA":15.8093,"DE":-70.8482,"AM":6.5800,"name":"NGC0362","t":"Gc"},{"RA":276.1370,"DE":-24.8698,"AM":6.9000,"name":"M28","t":"Gc"},{"RA":236.5143,"DE":-37.7861,"AM":6.9200,"name":"NGC5986","t":"Gc"},{"RA":325.0918,"DE":-23.1791,"AM":7.1000,"name":"M30","t":"Gc"},{"RA":253.3557,"DE":-22.1774,"AM":7.2000,"name":"NGC6235","t":"Gc"},{"RA":78.5280,"DE":-40.0466,"AM":7.2300,"name":"NGC1851","t":"Gc"},{"RA":244.2605,"DE":-22.9751,"AM":7.3000,"name":"M80","t":"Gc"},{"RA":272.0097,"DE":-43.7159,"AM":7.3200,"name":"NGC6541","t":"Gc"},{"RA":255.3025,"DE":-30.1124,"AM":7.3900,"name":"M62","t":"Gc"},{"RA":260.8958,"DE":-17.8130,"AM":7.4200,"name":"NGC6356","t":"Gc"},{"RA":256.1198,"DE":-24.7643,"AM":7.4300,"name":"NGC6284","t":"Gc"},{"RA":283.7636,"DE":-30.4785,"AM":7.7000,"name":"M54","t":"Gc"},{"RA":194.8956,"DE":-70.8746,"AM":7.7900,"name":"NGC4833","t":"Gc"},{"RA":198.2301,"DE":18.1691,"AM":7.7900,"name":"M53","t":"Gc"},{"RA":189.8667,"DE":-26.7430,"AM":7.9600,"name":"M68","t":"Gc"},{"RA":267.5535,"DE":-37.0511,"AM":8.0000,"name":"NGC6441","t":"Gc"},{"RA":13.1977,"DE":-26.5899,"AM":8.1300,"name":"NGC0288","t":"Gc"},{"RA":81.0441,"DE":-24.5242,"AM":8.1600,"name":"M79","t":"Gc"},{"RA":274.6569,"DE":-52.2152,"AM":8.1700,"name":"NGC6584","t":"Gc"},{"RA":154.4032,"DE":-46.4112,"AM":8.2400,"name":"NGC3201","t":"Gc"},{"RA":301.5202,"DE":-21.9222,"AM":8.2600,"name":"M75","t":"Gc"},{"RA":206.6108,"DE":-51.3735,"AM":8.3100,"name":"NGC5286","t":"Gc"},{"RA":277.8468,"DE":-32.3480,"AM":8.3100,"name":"M69","t":"Gc"},{"RA":289.1480,"DE":30.1845,"AM":8.4000,"name":"M56","t":"Gc"},{"RA":259.7991,"DE":-18.5162,"AM":8.4200,"name":"M9","t":"Gc"},{"RA":229.3517,"DE":-21.0101,"AM":8.5200,"name":"NGC5897","t":"Gc"},{"RA":225.0802,"DE":-82.2135,"AM":8.5600,"name":"IC4499","t":"Gc"},{"RA":48.0639,"DE":-55.2168,"AM":8.6300,"name":"NGC1261","t":"Gc"},{"RA":283.2704,"DE":-8.7055,"AM":8.6900,"name":"NGC6712","t":"Gc"},{"RA":248.1330,"DE":-13.0536,"AM":8.8500,"name":"M107","t":"Gc"},{"RA":232.0018,"DE":-50.6728,"AM":8.8600,"name":"NGC5927","t":"Gc"},{"RA":262.9785,"DE":-67.0479,"AM":8.8600,"name":"NGC6362","t":"Gc"},{"RA":261.3715,"DE":-48.4227,"AM":8.8700,"name":"NGC6352","t":"Gc"},{"RA":102.2467,"DE":-36.0053,"AM":8.8900,"name":"NGC2298","t":"Gc"},{"RA":77.1864,"DE":-68.7617,"AM":8.9600,"name":"NGC1850","t":"Gc"},{"RA":313.3663,"DE":-12.5371,"AM":8.9600,"name":"M72","t":"Gc"},{"RA":257.5434,"DE":-26.5817,"AM":9.0200,"name":"NGC6293","t":"Gc"},{"RA":258.6355,"DE":-29.4623,"AM":9.0300,"name":"NGC6304","t":"Gc"},{"RA":259.1559,"DE":-28.1400,"AM":9.0300,"name":"NGC6316","t":"Gc"},{"RA":280.8027,"DE":-32.2919,"AM":9.0600,"name":"M70","t":"Gc"},{"RA":273.4111,"DE":-31.8277,"AM":9.4700,"name":"NGC6569","t":"Gc"},{"RA":270.8920,"DE":-30.0340,"AM":9.4800,"name":"NGC6522","t":"Gc"},{"RA":225.9943,"DE":-33.0681,"AM":9.5600,"name":"NGC5824","t":"Gc"},{"RA":246.8089,"DE":-26.0247,"AM":9.6300,"name":"NGC6144","t":"Gc"},{"RA":246.9188,"DE":-38.8498,"AM":9.6800,"name":"NGC6139","t":"Gc"},{"RA":277.7344,"DE":-25.4964,"AM":9.6800,"name":"NGC6638","t":"Gc"},{"RA":211.3640,"DE":28.5345,"AM":9.7000,"name":"NGC5466","t":"Gc"},{"RA":78.4129,"DE":-65.4656,"AM":9.7300,"name":"NGC1866","t":"Gc"},{"RA":278.9406,"DE":-32.9903,"AM":9.7500,"name":"NGC6652","t":"Gc"},{"RA":308.5479,"DE":7.4041,"AM":9.7500,"name":"NGC6934","t":"Gc"},{"RA":287.8003,"DE":1.0305,"AM":9.7800,"name":"NGC6760","t":"Gc"},{"RA":73.8120,"DE":-68.2041,"AM":9.8500,"name":"NGC1755","t":"Gc"},{"RA":186.4391,"DE":-72.6591,"AM":9.8500,"name":"NGC4372","t":"Gc"},{"RA":270.9612,"DE":0.2969,"AM":9.8500,"name":"NGC6535","t":"Gc"},{"RA":251.7453,"DE":47.5278,"AM":9.8600,"name":"NGC6229","t":"Gc"},{"RA":271.8333,"DE":-24.9984,"AM":9.9000,"name":"NGC6544","t":"Gc"},{"RA":199.1125,"DE":17.6977,"AM":9.9600,"name":"NGC5053","t":"Gc"},{"RA":260.2922,"DE":-19.5874,"AM":10.0100,"name":"NGC6342","t":"Gc"},{"RA":114.5331,"DE":38.8800,"AM":10.0500,"name":"NGC2419","t":"Gc"},{"RA":217.4053,"DE":-5.9764,"AM":10.0500,"name":"NGC5634","t":"Gc"},{"RA":77.3724,"DE":-69.1276,"AM":10.0600,"name":"NGC1856","t":"Gc"},{"RA":246.4524,"DE":-72.2016,"AM":10.0800,"name":"NGC6101","t":"Gc"},{"RA":267.2195,"DE":-20.3596,"AM":10.1000,"name":"NGC6440","t":"Gc"},{"RA":89.3949,"DE":-69.1972,"AM":10.1600,"name":"NGC2157","t":"Gc"},{"RA":277.9759,"DE":-23.4761,"AM":10.2400,"name":"NGC6642","t":"Gc"},{"RA":256.2889,"DE":-22.7080,"AM":10.3000,"name":"NGC6287","t":"Gc"},{"RA":89.7344,"DE":-68.5159,"AM":10.3400,"name":"NGC2164","t":"Gc"},{"RA":283.7752,"DE":-22.7016,"AM":10.3500,"name":"NGC6717","t":"Gc"},{"RA":84.1169,"DE":-66.9898,"AM":10.3600,"name":"NGC2041","t":"Gc"},{"RA":79.6520,"DE":-69.4068,"AM":10.3800,"name":"NGC1916","t":"Gc"},{"RA":77.3329,"DE":-68.8474,"AM":10.3900,"name":"NGC1854","t":"Gc"},{"RA":315.3719,"DE":16.1875,"AM":10.4600,"name":"NGC7006","t":"Gc"},{"RA":347.1112,"DE":-15.6115,"AM":10.4800,"name":"NGC7492","t":"Gc"},{"RA":17.0715,"DE":-72.8835,"AM":10.5000,"name":"NGC0419","t":"Gc"},{"RA":76.2774,"DE":-69.4039,"AM":10.6000,"name":"NGC1835","t":"Gc"},{"RA":271.2067,"DE":-30.0558,"AM":10.6500,"name":"NGC6528","t":"Gc"},{"RA":82.1880,"DE":-66.2359,"AM":10.7000,"name":"NGC1978","t":"Gc"},{"RA":88.2406,"DE":-69.4928,"AM":10.7000,"name":"NGC2136","t":"Gc"},{"RA":264.6539,"DE":-23.9088,"AM":10.7100,"name":"NGC6401","t":"Gc"},{"RA":233.8690,"DE":-50.6597,"AM":10.7200,"name":"NGC5946","t":"Gc"},{"RA":182.5257,"DE":18.5421,"AM":10.7400,"name":"NGC4147","t":"Gc"},{"RA":83.4243,"DE":-70.9868,"AM":10.8300,"name":"NGC2031","t":"Gc"},{"RA":82.5862,"DE":-66.8850,"AM":10.8400,"name":"NGC2002","t":"Gc"},{"RA":82.9861,"DE":-70.1596,"AM":10.8600,"name":"NGC2019","t":"Gc"},{"RA":219.9021,"DE":-26.5383,"AM":10.8900,"name":"NGC5694","t":"Gc"},{"RA":74.7867,"DE":-65.9873,"AM":10.9300,"name":"NGC1783","t":"Gc"},{"RA":92.8807,"DE":-69.1214,"AM":10.9400,"name":"NGC2210","t":"Gc"},{"RA":78.2949,"DE":-69.3116,"AM":11.0400,"name":"NGC1872","t":"Gc"},{"RA":260.9944,"DE":-26.3534,"AM":11.0500,"name":"NGC6355","t":"Gc"},{"RA":81.9087,"DE":-69.9736,"AM":11.0700,"name":"NGC1986","t":"Gc"},{"RA":72.6505,"DE":-69.9854,"AM":11.1000,"name":"NGC1711","t":"Gc"},{"RA":76.5697,"DE":-64.9175,"AM":11.1800,"name":"NGC1831","t":"Gc"},{"RA":6.7010,"DE":-71.5357,"AM":11.2400,"name":"NGC0121","t":"Gc"},{"RA":78.2913,"DE":-69.1169,"AM":11.2600,"name":"NGC1870","t":"Gc"},{"RA":91.1773,"DE":-75.4384,"AM":11.2900,"name":"NGC2203","t":"Gc"},{"RA":272.5766,"DE":-31.7635,"AM":11.2900,"name":"NGC6558","t":"Gc"},{"RA":82.7300,"DE":-66.4666,"AM":11.3000,"name":"NGC2003","t":"Gc"},{"RA":76.8914,"DE":-67.4615,"AM":11.3100,"name":"NGC1846","t":"Gc"},{"RA":89.4570,"DE":-68.4608,"AM":11.3800,"name":"NGC2156","t":"Gc"},{"RA":89.5162,"DE":-68.6229,"AM":11.3800,"name":"NGC2159","t":"Gc"},{"RA":71.3473,"DE":-83.9991,"AM":11.4300,"name":"NGC1841","t":"Gc"},{"RA":73.5790,"DE":-70.4425,"AM":11.5700,"name":"NGC1754","t":"Gc"},{"RA":78.6513,"DE":-63.9545,"AM":11.5700,"name":"NGC1868","t":"Gc"},{"RA":82.5452,"DE":-69.7524,"AM":11.5700,"name":"NGC2005","t":"Gc"},{"RA":56.1390,"DE":-71.6716,"AM":11.5900,"name":"NGC1466","t":"Gc"},{"RA":73.5524,"DE":-69.8058,"AM":11.7300,"name":"NGC1751","t":"Gc"},{"RA":81.3659,"DE":-68.8383,"AM":11.7400,"name":"NGC1953","t":"Gc"},{"RA":16.9937,"DE":-72.3551,"AM":11.7600,"name":"NGC0416","t":"Gc"},{"RA":80.1476,"DE":-69.5253,"AM":11.7900,"name":"NGC1926","t":"Gc"},{"RA":89.4062,"DE":-67.2638,"AM":11.7900,"name":"NGC2154","t":"Gc"},{"RA":80.3609,"DE":-69.9497,"AM":11.8300,"name":"NGC1939","t":"Gc"},{"RA":80.4893,"DE":-72.4941,"AM":11.8400,"name":"NGC1944","t":"Gc"},{"RA":79.3429,"DE":-69.3353,"AM":11.8600,"name":"NGC1903","t":"Gc"},{"RA":80.6197,"DE":-70.1549,"AM":11.8800,"name":"NGC1943","t":"Gc"},{"RA":89.4953,"DE":-72.9745,"AM":11.8800,"name":"NGC2173","t":"Gc"},{"RA":80.6822,"DE":-67.1866,"AM":11.9100,"name":"NGC1940","t":"Gc"},{"RA":77.3491,"DE":-67.7763,"AM":12.0100,"name":"NGC1852","t":"Gc"},{"RA":88.3976,"DE":-67.4295,"AM":12.0500,"name":"NGC2135","t":"Gc"},{"RA":72.2710,"DE":-69.1151,"AM":12.0700,"name":"NGC1698","t":"Gc"},{"RA":88.0988,"DE":-67.3341,"AM":12.1000,"name":"NGC2130","t":"Gc"},{"RA":71.9353,"DE":-69.3738,"AM":12.1600,"name":"NGC1695","t":"Gc"},{"RA":75.1438,"DE":-69.6137,"AM":12.1600,"name":"NGC1801","t":"Gc"},{"RA":86.0799,"DE":-66.9176,"AM":12.1900,"name":"NGC2105","t":"Gc"},{"RA":14.4253,"DE":-74.4734,"AM":12.2100,"name":"NGC0339","t":"Gc"},{"RA":96.4565,"DE":-68.9198,"AM":12.2300,"name":"NGC2249","t":"Gc"},{"RA":73.7076,"DE":-69.2376,"AM":12.2400,"name":"NGC1756","t":"Gc"},{"RA":69.3845,"DE":-70.5859,"AM":12.2800,"name":"NGC1651","t":"Gc"},{"RA":85.9870,"DE":-69.1821,"AM":12.3200,"name":"NGC2108","t":"Gc"},{"RA":79.7582,"DE":-68.9990,"AM":12.3300,"name":"NGC1917","t":"Gc"},{"RA":87.0535,"DE":-71.4798,"AM":12.3700,"name":"NGC2121","t":"Gc"},{"RA":286.3150,"DE":1.9006,"AM":12.4000,"name":"NGC6749","t":"Gc"},{"RA":84.4455,"DE":-74.7832,"AM":12.4100,"name":"IC2146","t":"Gc"},{"RA":87.9305,"DE":-65.3215,"AM":12.5600,"name":"NGC2123","t":"Gc"},{"RA":89.6384,"DE":-65.4765,"AM":12.6000,"name":"NGC2155","t":"Gc"},{"RA":72.1492,"DE":-68.5584,"AM":12.6200,"name":"NGC1697","t":"Gc"},{"RA":97.5577,"DE":-64.3256,"AM":12.6200,"name":"NGC2257","t":"Gc"},{"RA":87.6442,"DE":-63.6776,"AM":12.6700,"name":"NGC2120","t":"Gc"},{"RA":67.4038,"DE":-71.8383,"AM":12.6800,"name":"NGC1629","t":"Gc"},{"RA":90.1257,"DE":-63.7214,"AM":12.7000,"name":"NGC2162","t":"Gc"},{"RA":73.9486,"DE":-74.2854,"AM":12.8000,"name":"NGC1777","t":"Gc"},{"RA":69.4170,"DE":-66.1991,"AM":12.8900,"name":"NGC1644","t":"Gc"},{"RA":71.9115,"DE":-69.3436,"AM":12.8900,"name":"NGC1693","t":"Gc"},{"RA":90.2575,"DE":-74.7254,"AM":12.9400,"name":"NGC2190","t":"Gc"},{"RA":88.9294,"DE":-74.3539,"AM":12.9500,"name":"NGC2161","t":"Gc"},{"RA":81.3772,"DE":-69.8368,"AM":12.9900,"name":"NGC1958","t":"Gc"},{"RA":89.4655,"DE":-66.4007,"AM":13.0500,"name":"NGC2153","t":"Gc"},{"RA":74.4653,"DE":-71.9020,"AM":13.0600,"name":"NGC1789","t":"Gc"},{"RA":80.3530,"DE":-69.9394,"AM":13.0900,"name":"NGC1938","t":"Gc"},{"RA":69.5952,"DE":-68.6729,"AM":13.1300,"name":"NGC1649","t":"Gc"},{"RA":92.1496,"DE":-73.8384,"AM":13.1500,"name":"NGC2209","t":"Gc"},{"RA":95.1790,"DE":-67.5185,"AM":13.2000,"name":"NGC2231","t":"Gc"},{"RA":91.5730,"DE":-65.0988,"AM":13.4200,"name":"NGC2193","t":"Gc"},{"RA":91.5305,"DE":-67.0972,"AM":13.4500,"name":"NGC2197","t":"Gc"},{"RA":83.3413,"DE":-75.3754,"AM":13.4800,"name":"IC2140","t":"Gc"},{"RA":90.6819,"DE":-65.2649,"AM":13.6400,"name":"NGC2181","t":"Gc"},{"RA":86.0667,"DE":-62.7856,"AM":13.6700,"name":"NGC2097","t":"Gc"},{"RA":88.7091,"DE":-65.8371,"AM":13.7600,"name":"NGC2138","t":"Gc"},{"RA":80.7743,"DE":-75.4468,"AM":13.9400,"name":"IC2134","t":"Gc"},{"RA":84.7994,"DE":-75.5624,"AM":14.2300,"name":"IC2148","t":"Gc"},{"RA":89.3536,"DE":-75.1395,"AM":14.2400,"name":"IC2161","t":"Gc"},{"DE":-1,"RA":-1,"AM":-1,"name":"Mercury","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Venus","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Mars","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Jupiter","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Saturn","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Neptune","t":"P"},{"DE":-1,"RA":-1,"AM":-1,"name":"Uranus","t":"P"},{"DE":-75.0000,"RA":240.0000,"AM":-1,"name":"Apus","t":"Ca"},{"DE":5.0000,"RA":300.0000,"AM":-1,"name":"Aquila","t":"Ca"},{"DE":20.0000,"RA":45.0000,"AM":-1,"name":"Aries","t":"Ca"},{"DE":70.0000,"RA":90.0000,"AM":-1,"name":"Camelopardus","t":"Ca"},{"DE":-20.0000,"RA":315.0000,"AM":-1,"name":"Capricornus","t":"Ca"},{"DE":-80.0000,"RA":165.0000,"AM":-1,"name":"Chamaeleon","t":"Ca"},{"DE":-20.0000,"RA":105.0000,"AM":-1,"name":"Canis Major","t":"Ca"},{"DE":5.0000,"RA":120.0000,"AM":-1,"name":"Canis Minor","t":"Ca"},{"DE":20.0000,"RA":135.0000,"AM":-1,"name":"Cancer","t":"Ca"},{"DE":-35.0000,"RA":90.0000,"AM":-1,"name":"Columba","t":"Ca"},{"DE":-20.0000,"RA":180.0000,"AM":-1,"name":"Corvus","t":"Ca"},{"DE":40.0000,"RA":195.0000,"AM":-1,"name":"Canes Venatici","t":"Ca"},{"DE":40.0000,"RA":315.0000,"AM":-1,"name":"Cygnus","t":"Ca"},{"DE":10.0000,"RA":315.0000,"AM":-1,"name":"Delphinus","t":"Ca"},{"DE":-65.0000,"RA":75.0000,"AM":-1,"name":"Dorado","t":"Ca"},{"DE":10.0000,"RA":315.0000,"AM":-1,"name":"Equuleus","t":"Ca"},{"DE":-45.0000,"RA":330.0000,"AM":-1,"name":"Grus","t":"Ca"},{"DE":-75.0000,"RA":30.0000,"AM":-1,"name":"Hydrus","t":"Ca"},{"DE":45.0000,"RA":330.0000,"AM":-1,"name":"Lacerta","t":"Ca"},{"DE":15.0000,"RA":165.0000,"AM":-1,"name":"Leo","t":"Ca"},{"DE":-20.0000,"RA":90.0000,"AM":-1,"name":"Lepus","t":"Ca"},{"DE":35.0000,"RA":150.0000,"AM":-1,"name":"Leo Minor","t":"Ca"},{"DE":-45.0000,"RA":225.0000,"AM":-1,"name":"Lupus","t":"Ca"},{"DE":45.0000,"RA":120.0000,"AM":-1,"name":"Lynx","t":"Ca"},{"DE":-70.0000,"RA":180.0000,"AM":-1,"name":"Musca","t":"Ca"},{"DE":-65.0000,"RA":300.0000,"AM":-1,"name":"Pavo","t":"Ca"},{"DE":-30.0000,"RA":330.0000,"AM":-1,"name":"Piscis Austrinus","t":"Ca"},{"DE":15.0000,"RA":15.0000,"AM":-1,"name":"Pisces","t":"Ca"},{"DE":-40.0000,"RA":255.0000,"AM":-1,"name":"Scorpius","t":"Ca"},{"DE":0.0000,"RA":255.0000,"AM":-1,"name":"Serpens","t":"Ca"},{"DE":15.0000,"RA":60.0000,"AM":-1,"name":"Taurus","t":"Ca"},{"DE":-65.0000,"RA":0.0000,"AM":-1,"name":"Tucana","t":"Ca"},{"DE":50.0000,"RA":165.0000,"AM":-1,"name":"Ursa Major","t":"Ca"},{"DE":70.0000,"RA":225.0000,"AM":-1,"name":"Ursa Minor","t":"Ca"},{"DE":-70.0000,"RA":120.0000,"AM":-1,"name":"Volans","t":"Ca"},{"DE":25.0000,"RA":300.0000,"AM":-1,"name":"Vulpecula","t":"Ca"},{"DE":-50.0000,"RA":195.0000,"AM":-1,"name":"Centaurus","t":"Ca"},{"DE":-10.0000,"RA":30.0000,"AM":-1,"name":"Cetus","t":"Ca"},{"DE":65.0000,"RA":255.0000,"AM":-1,"name":"Draco","t":"Ca"},{"DE":-20.0000,"RA":150.0000,"AM":-1,"name":"Hydra","t":"Ca"},{"DE":-5.0000,"RA":105.0000,"AM":-1,"name":"Monoceros","t":"Ca"},{"DE":20.0000,"RA":330.0000,"AM":-1,"name":"Pegasus","t":"Ca"},{"DE":-50.0000,"RA":15.0000,"AM":-1,"name":"Phoenix","t":"Ca"},{"DE":40.0000,"RA":15.0000,"AM":-1,"name":"Andromeda","t":"Ca"},{"DE":-15.0000,"RA":345.0000,"AM":-1,"name":"Aquarius","t":"Ca"},{"DE":40.0000,"RA":90.0000,"AM":-1,"name":"Auriga","t":"Ca"},{"DE":30.0000,"RA":225.0000,"AM":-1,"name":"Bo\u00f6tes","t":"Ca"},{"DE":60.0000,"RA":15.0000,"AM":-1,"name":"Cassiopeia","t":"Ca"},{"DE":70.0000,"RA":330.0000,"AM":-1,"name":"Cepheus","t":"Ca"},{"DE":20.0000,"RA":195.0000,"AM":-1,"name":"Coma Berenices","t":"Ca"},{"DE":20.0000,"RA":105.0000,"AM":-1,"name":"Gemini","t":"Ca"},{"DE":30.0000,"RA":255.0000,"AM":-1,"name":"Hercules","t":"Ca"},{"DE":-55.0000,"RA":315.0000,"AM":-1,"name":"Indus","t":"Ca"},{"DE":0.0000,"RA":255.0000,"AM":-1,"name":"Ophiuchus","t":"Ca"},{"DE":5.0000,"RA":75.0000,"AM":-1,"name":"Orion","t":"Ca"},{"DE":45.0000,"RA":45.0000,"AM":-1,"name":"Perseus","t":"Ca"},{"DE":-25.0000,"RA":285.0000,"AM":-1,"name":"Sagittarius","t":"Ca"},{"DE":0.0000,"RA":195.0000,"AM":-1,"name":"Virgo","t":"Ca"},{"DE":-35.0000,"RA":150.0000,"AM":-1,"name":"Antila","t":"Ca"},{"DE":-55.0000,"RA":255.0000,"AM":-1,"name":"Ara","t":"Ca"},{"DE":-40.0000,"RA":75.0000,"AM":-1,"name":"Caelum","t":"Ca"},{"DE":-60.0000,"RA":135.0000,"AM":-1,"name":"Carina","t":"Ca"},{"DE":-60.0000,"RA":225.0000,"AM":-1,"name":"Circinus","t":"Ca"},{"DE":-40.0000,"RA":285.0000,"AM":-1,"name":"Corona Australis","t":"Ca"},{"DE":30.0000,"RA":240.0000,"AM":-1,"name":"Corona Borealis","t":"Ca"},{"DE":-15.0000,"RA":165.0000,"AM":-1,"name":"Crater","t":"Ca"},{"DE":-60.0000,"RA":180.0000,"AM":-1,"name":"Crux","t":"Ca"},{"DE":-20.0000,"RA":45.0000,"AM":-1,"name":"Eridanus","t":"Ca"},{"DE":-30.0000,"RA":45.0000,"AM":-1,"name":"Fornax","t":"Ca"},{"DE":-60.0000,"RA":45.0000,"AM":-1,"name":"Horologium","t":"Ca"},{"DE":-15.0000,"RA":225.0000,"AM":-1,"name":"Libra","t":"Ca"},{"DE":40.0000,"RA":285.0000,"AM":-1,"name":"Lyra","t":"Ca"},{"DE":-80.0000,"RA":75.0000,"AM":-1,"name":"Mensa","t":"Ca"},{"DE":-35.0000,"RA":315.0000,"AM":-1,"name":"Microscopium","t":"Ca"},{"DE":-50.0000,"RA":240.0000,"AM":-1,"name":"Norma","t":"Ca"},{"DE":-85.0000,"RA":330.0000,"AM":-1,"name":"Octans","t":"Ca"},{"DE":-55.0000,"RA":90.0000,"AM":-1,"name":"Pictor","t":"Ca"},{"DE":-40.0000,"RA":120.0000,"AM":-1,"name":"Puppis","t":"Ca"},{"DE":-30.0000,"RA":135.0000,"AM":-1,"name":"Pyxis","t":"Ca"},{"DE":-60.0000,"RA":60.0000,"AM":-1,"name":"Reticulum","t":"Ca"},{"DE":-30.0000,"RA":0.0000,"AM":-1,"name":"Sculptor","t":"Ca"},{"DE":-10.0000,"RA":285.0000,"AM":-1,"name":"Scutum","t":"Ca"},{"DE":0.0000,"RA":150.0000,"AM":-1,"name":"Sextans","t":"Ca"},{"DE":10.0000,"RA":300.0000,"AM":-1,"name":"Sagitta","t":"Ca"},{"DE":-50.0000,"RA":285.0000,"AM":-1,"name":"Telescopium","t":"Ca"},{"DE":-65.0000,"RA":240.0000,"AM":-1,"name":"Triangulum Australe","t":"Ca"},{"DE":30.0000,"RA":30.0000,"AM":-1,"name":"Triangulum","t":"Ca"},{"DE":-50.0000,"RA":135.0000,"AM":-1,"name":"Vela","t":"Ca"},{"DE":-16.7161,"RA":101.2872,"AM":-1.4400,"t":"S","name":"Sirius"},{"DE":-52.6957,"RA":95.9879,"AM":-0.6200,"t":"S","name":"Canopus"},{"DE":19.1824,"RA":213.9154,"AM":-0.0500,"t":"S","name":"Arcturus"},{"DE":-60.8340,"RA":219.9115,"AM":-0.0100,"t":"S","name":"Rigil Kentaurus"},{"DE":38.7837,"RA":279.2346,"AM":0.0300,"t":"S","name":"Vega"},{"DE":45.9980,"RA":79.1723,"AM":0.0800,"t":"S","name":"Capella"},{"DE":-8.2016,"RA":78.6345,"AM":0.1800,"t":"S","name":"Rigel"},{"DE":5.2250,"RA":114.8255,"AM":0.4000,"t":"S","name":"Procyon"},{"DE":-57.2368,"RA":24.4283,"AM":0.4500,"t":"S","name":"Achernar"},{"DE":7.4071,"RA":88.7929,"AM":0.4500,"t":"S","name":"Betelgeuse"},{"DE":-60.3730,"RA":210.9559,"AM":0.6100,"t":"S","name":"Hadar"},{"DE":8.8683,"RA":297.6958,"AM":0.7600,"t":"S","name":"Altair"},{"DE":-63.0991,"RA":186.6497,"AM":0.7700,"t":"S","name":"Acrux"},{"DE":16.5093,"RA":68.9802,"AM":0.8700,"t":"S","name":"Aldebaran"},{"DE":46.0008,"RA":79.1689,"AM":0.9600,"t":"S"},{"DE":-11.1613,"RA":201.2982,"AM":0.9800,"t":"S","name":"Spica"},{"DE":-26.4320,"RA":247.3519,"AM":1.0600,"t":"S","name":"Antares"},{"DE":28.0262,"RA":116.3292,"AM":1.1600,"t":"S","name":"Pollux"},{"DE":-29.6222,"RA":344.4126,"AM":1.1700,"t":"S","name":"Fomalhaut"},{"DE":-59.6888,"RA":191.9304,"AM":1.2500,"t":"S","name":"Becrux"},{"DE":45.2803,"RA":310.3580,"AM":1.2500,"t":"S","name":"Deneb"},{"DE":-60.8383,"RA":219.9052,"AM":1.3500,"t":"S"},{"DE":11.9672,"RA":152.0930,"AM":1.3600,"t":"S","name":"Regulus"},{"DE":-28.9721,"RA":104.6565,"AM":1.5000,"t":"S","name":"Adhara"},{"DE":31.8883,"RA":113.6495,"AM":1.5800,"t":"S","name":"Castor"},{"DE":-57.1132,"RA":187.7914,"AM":1.5900,"t":"S","name":"Gacrux"},{"DE":-37.1038,"RA":263.4022,"AM":1.6200,"t":"S","name":"Shaula"},{"DE":6.3497,"RA":81.2828,"AM":1.6400,"t":"S","name":"Bellatrix"},{"DE":28.6075,"RA":81.5730,"AM":1.6500,"t":"S","name":"Alnath"},{"DE":-69.7172,"RA":138.3006,"AM":1.6700,"t":"S","name":"Miaplacidus"},{"DE":-1.2019,"RA":84.0534,"AM":1.6900,"t":"S","name":"Alnilam"},{"DE":-46.9610,"RA":332.0581,"AM":1.7300,"t":"S","name":"Alnair"},{"DE":-1.9426,"RA":85.1897,"AM":1.7400,"t":"S","name":"Alnitak"},{"DE":-47.3366,"RA":122.3831,"AM":1.7500,"t":"S"},{"DE":55.9598,"RA":193.5071,"AM":1.7600,"t":"S","name":"Alioth"},{"DE":49.8612,"RA":51.0807,"AM":1.7900,"t":"S","name":"Mirphak"},{"DE":-34.3846,"RA":276.0430,"AM":1.7900,"t":"S","name":"Kaus Australis"},{"DE":61.7510,"RA":165.9323,"AM":1.8100,"t":"S","name":"Dubhe"},{"DE":-26.3932,"RA":107.0979,"AM":1.8300,"t":"S","name":"Wezen"},{"DE":49.3133,"RA":206.8853,"AM":1.8500,"t":"S","name":"Alkaid"},{"DE":-59.5095,"RA":125.6285,"AM":1.8600,"t":"S","name":"Avior"},{"DE":-42.9978,"RA":264.3297,"AM":1.8600,"t":"S","name":"Sargas"},{"DE":44.9474,"RA":89.8822,"AM":1.9000,"t":"S","name":"Menkalinan"},{"DE":-69.0277,"RA":252.1662,"AM":1.9100,"t":"S","name":"Atria"},{"DE":16.3993,"RA":99.4279,"AM":1.9300,"t":"S","name":"Alhena"},{"DE":-54.7088,"RA":131.1759,"AM":1.9300,"t":"S"},{"DE":-56.7351,"RA":306.4119,"AM":1.9400,"t":"S","name":"Peacock"},{"DE":89.2641,"RA":37.9462,"AM":1.9700,"t":"S","name":"Polaris"},{"DE":-17.9559,"RA":95.6749,"AM":1.9800,"t":"S","name":"Mirzam"},{"DE":-8.6586,"RA":141.8969,"AM":1.9900,"t":"S","name":"Alphard"},{"DE":23.4624,"RA":31.7933,"AM":2.0100,"t":"S","name":"Hamal"},{"DE":19.8415,"RA":154.9931,"AM":2.0100,"t":"S","name":"Algieba"},{"DE":-17.9866,"RA":10.8973,"AM":2.0400,"t":"S","name":"Diphda"},{"DE":-26.2967,"RA":283.8163,"AM":2.0500,"t":"S","name":"Nunki"},{"DE":-36.3700,"RA":211.6709,"AM":2.0600,"t":"S","name":"Menkent"},{"DE":29.0904,"RA":2.0969,"AM":2.0700,"t":"S","name":"Alpheratz"},{"DE":35.6206,"RA":17.4329,"AM":2.0700,"t":"S","name":"Mirach"},{"DE":-9.6696,"RA":86.9391,"AM":2.0700,"t":"S","name":"Saiph"},{"DE":74.1555,"RA":222.6766,"AM":2.0700,"t":"S","name":"Kochab"},{"DE":-46.8846,"RA":340.6667,"AM":2.0700,"t":"S"},{"DE":12.5600,"RA":263.7336,"AM":2.0800,"t":"S","name":"Rasalhague"},{"DE":40.9556,"RA":47.0422,"AM":2.0900,"t":"S","name":"Algol"},{"DE":42.3297,"RA":30.9748,"AM":2.1000,"t":"S","name":"Almaak"},{"DE":14.5721,"RA":177.2649,"AM":2.1400,"t":"S","name":"Denebola"},{"DE":60.7167,"RA":14.1771,"AM":2.1500,"t":"S","name":"Cih"},{"DE":-48.9599,"RA":190.3796,"AM":2.2000,"t":"S"},{"DE":-40.0031,"RA":120.8961,"AM":2.2100,"t":"S","name":"Naos"},{"DE":-59.2752,"RA":139.2726,"AM":2.2100,"t":"S","name":"Tureis"},{"DE":26.7147,"RA":233.6719,"AM":2.2200,"t":"S","name":"Alphekka"},{"DE":-43.4326,"RA":136.9990,"AM":2.2300,"t":"S"},{"DE":54.9254,"RA":200.9812,"AM":2.2300,"t":"S","name":"Mizar"},{"DE":40.2567,"RA":305.5571,"AM":2.2300,"t":"S","name":"Sadr"},{"DE":56.5373,"RA":10.1267,"AM":2.2400,"t":"S","name":"Shedir"},{"DE":51.4889,"RA":269.1516,"AM":2.2400,"t":"S","name":"Etamin"},{"DE":-0.2991,"RA":83.0017,"AM":2.2500,"t":"S","name":"Mintaka"},{"DE":59.1498,"RA":2.2933,"AM":2.2800,"t":"S","name":"Caph"},{"DE":-53.4664,"RA":204.9719,"AM":2.2900,"t":"S"},{"DE":-22.6217,"RA":240.0834,"AM":2.2900,"t":"S","name":"Dschubba"},{"DE":-34.2932,"RA":252.5412,"AM":2.2900,"t":"S"},{"DE":-47.3882,"RA":220.4823,"AM":2.3000,"t":"S"},{"DE":-42.1578,"RA":218.8768,"AM":2.3300,"t":"S"},{"DE":56.3824,"RA":165.4602,"AM":2.3400,"t":"S","name":"Merak"},{"DE":27.0742,"RA":221.2468,"AM":2.3500,"t":"S","name":"Izar"},{"DE":9.8750,"RA":326.0465,"AM":2.3800,"t":"S","name":"Enif"},{"DE":-39.0300,"RA":265.6220,"AM":2.3900,"t":"S"},{"DE":-42.3060,"RA":6.5708,"AM":2.4000,"t":"S","name":"Ankaa"},{"DE":53.6948,"RA":178.4575,"AM":2.4100,"t":"S","name":"Phad"},{"DE":-15.7249,"RA":257.5945,"AM":2.4300,"t":"S"},{"DE":28.0828,"RA":345.9435,"AM":2.4400,"t":"S","name":"Scheat"},{"DE":-29.3031,"RA":111.0238,"AM":2.4500,"t":"S","name":"Aludra"},{"DE":62.5856,"RA":319.6445,"AM":2.4500,"t":"S","name":"Alderamin"},{"DE":-55.0107,"RA":140.5284,"AM":2.4700,"t":"S"},{"DE":33.9703,"RA":311.5527,"AM":2.4800,"t":"S","name":"Gienah"},{"DE":15.2053,"RA":346.1902,"AM":2.4900,"t":"S","name":"Markab"},{"DE":4.0897,"RA":45.5699,"AM":2.5400,"t":"S","name":"Menkar"},{"DE":-10.5671,"RA":249.2897,"AM":2.5400,"t":"S"},{"DE":-47.2884,"RA":208.8850,"AM":2.5500,"t":"S"},{"DE":20.5237,"RA":168.5271,"AM":2.5600,"t":"S","name":"Zosma"},{"DE":-19.8055,"RA":241.3593,"AM":2.5600,"t":"S","name":"Graffias"},{"DE":-17.8223,"RA":83.1826,"AM":2.5800,"t":"S","name":"Arneb"},{"DE":-50.7224,"RA":182.0897,"AM":2.5800,"t":"S"},{"DE":-17.5419,"RA":183.9516,"AM":2.5800,"t":"S","name":"Gienah Ghurab"},{"DE":-29.8801,"RA":285.6530,"AM":2.6000,"t":"S"},{"DE":-9.3829,"RA":229.2517,"AM":2.6100,"t":"S","name":"Zubeneschemali"},{"DE":6.4256,"RA":236.0670,"AM":2.6300,"t":"S","name":"Unukalhai"},{"DE":20.8080,"RA":28.6600,"AM":2.6400,"t":"S","name":"Sheratan"},{"DE":-34.0741,"RA":84.9123,"AM":2.6500,"t":"S","name":"Phakt"},{"DE":37.2126,"RA":89.9303,"AM":2.6500,"t":"S"},{"DE":-23.3968,"RA":188.5968,"AM":2.6500,"t":"S","name":"Kraz"},{"DE":60.2353,"RA":21.4532,"AM":2.6600,"t":"S","name":"Ruchbah"},{"DE":18.3977,"RA":208.6712,"AM":2.6800,"t":"S","name":"Mufrid"},{"DE":-43.1340,"RA":224.6331,"AM":2.6800,"t":"S"},{"DE":33.1661,"RA":74.2484,"AM":2.6900,"t":"S","name":"Hassaleh"},{"DE":-49.4203,"RA":161.6923,"AM":2.6900,"t":"S"},{"DE":-69.1356,"RA":189.2961,"AM":2.6900,"t":"S"},{"DE":-37.2958,"RA":262.6910,"AM":2.7000,"t":"S"},{"DE":-37.0975,"RA":109.2857,"AM":2.7100,"t":"S"},{"DE":-29.8281,"RA":275.2485,"AM":2.7200,"t":"S","name":"Kaus Meridionalis"},{"DE":10.6133,"RA":296.5649,"AM":2.7200,"t":"S","name":"Tarazed"},{"DE":-3.6943,"RA":243.5864,"AM":2.7300,"t":"S"},{"DE":61.5142,"RA":245.9979,"AM":2.7300,"t":"S"},{"DE":-64.3945,"RA":160.7392,"AM":2.7400,"t":"S"},{"DE":-1.4494,"RA":190.4152,"AM":2.7400,"t":"S","name":"Porrima"},{"DE":-5.9099,"RA":83.8583,"AM":2.7500,"t":"S","name":"Hatsya"},{"DE":-36.7123,"RA":200.1494,"AM":2.7500,"t":"S"},{"DE":-16.0418,"RA":222.7197,"AM":2.7500,"t":"S","name":"Zubenelgenubi"},{"DE":4.5673,"RA":265.8681,"AM":2.7600,"t":"S","name":"Cebalrai"},{"DE":-5.0864,"RA":76.9624,"AM":2.7800,"t":"S","name":"Cursa"},{"DE":21.4896,"RA":247.5550,"AM":2.7800,"t":"S","name":"Kornephoros"},{"DE":14.3903,"RA":258.6619,"AM":2.7800,"t":"S","name":"Rasalgethi"},{"DE":-58.7489,"RA":183.7864,"AM":2.7900,"t":"S"},{"DE":52.3014,"RA":262.6082,"AM":2.7900,"t":"S","name":"Rastaban"},{"DE":-41.1668,"RA":233.7852,"AM":2.8000,"t":"S"},{"DE":-20.7594,"RA":82.0613,"AM":2.8100,"t":"S","name":"Nihal"},{"DE":31.6027,"RA":250.3217,"AM":2.8100,"t":"S"},{"DE":-77.2542,"RA":6.4187,"AM":2.8200,"t":"S"},{"DE":-28.2160,"RA":248.9706,"AM":2.8200,"t":"S"},{"DE":-25.4217,"RA":276.9927,"AM":2.8200,"t":"S","name":"Kaus Borealis"},{"DE":15.1836,"RA":3.3090,"AM":2.8300,"t":"S","name":"Algenib"},{"DE":-24.3043,"RA":121.8861,"AM":2.8300,"t":"S"},{"DE":-63.4307,"RA":238.7862,"AM":2.8300,"t":"S"},{"DE":31.8836,"RA":58.5330,"AM":2.8400,"t":"S"},{"DE":-55.5299,"RA":261.3250,"AM":2.8400,"t":"S"},{"DE":-49.8761,"RA":262.9604,"AM":2.8400,"t":"S"},{"DE":24.1051,"RA":56.8712,"AM":2.8500,"t":"S","name":"Alcyone"},{"DE":10.9591,"RA":195.5442,"AM":2.8500,"t":"S","name":"Vindemiatrix"},{"DE":-16.1273,"RA":326.7602,"AM":2.8500,"t":"S"},{"DE":31.8905,"RA":113.6524,"AM":2.8500,"t":"S"},{"DE":-61.5699,"RA":29.6918,"AM":2.8600,"t":"S"},{"DE":45.1308,"RA":296.2436,"AM":2.8600,"t":"S"},{"DE":22.5136,"RA":95.7401,"AM":2.8700,"t":"S"},{"DE":-68.6795,"RA":229.7277,"AM":2.8700,"t":"S"},{"DE":-60.2596,"RA":334.6256,"AM":2.8700,"t":"S"},{"DE":-40.3047,"RA":44.5653,"AM":2.8800,"t":"S","name":"Acamar"},{"DE":-21.0236,"RA":287.4410,"AM":2.8800,"t":"S","name":"Albaldah"},{"DE":8.2893,"RA":111.7877,"AM":2.8900,"t":"S","name":"Gomeisa"},{"DE":38.3184,"RA":194.0071,"AM":2.8900,"t":"S","name":"Cor Caroli"},{"DE":-26.1141,"RA":239.7130,"AM":2.8900,"t":"S"},{"DE":40.0102,"RA":59.4635,"AM":2.9000,"t":"S"},{"DE":-25.5928,"RA":245.2971,"AM":2.9000,"t":"S"},{"DE":-5.5712,"RA":322.8897,"AM":2.9000,"t":"S","name":"Sadalsuud"},{"DE":53.5064,"RA":46.1991,"AM":2.9100,"t":"S"},{"DE":-65.0720,"RA":146.7755,"AM":2.9200,"t":"S"},{"DE":30.2212,"RA":340.7506,"AM":2.9300,"t":"S","name":"Matar"},{"DE":-50.6146,"RA":102.4840,"AM":2.9400,"t":"S"},{"DE":-16.5154,"RA":187.4661,"AM":2.9400,"t":"S","name":"Algorab"},{"DE":-0.3199,"RA":331.4460,"AM":2.9500,"t":"S","name":"Sadalmelik"},{"DE":-13.5085,"RA":59.5074,"AM":2.9700,"t":"S","name":"Zaurak"},{"DE":21.1425,"RA":84.4112,"AM":2.9700,"t":"S"},{"DE":23.7743,"RA":146.4628,"AM":2.9700,"t":"S","name":"Ras Elased Australis"},{"DE":-30.4241,"RA":271.4520,"AM":2.9800,"t":"S","name":"Nash"},{"DE":-23.1715,"RA":199.7304,"AM":2.9900,"t":"S"},{"DE":-40.1270,"RA":266.8962,"AM":2.9900,"t":"S"},{"DE":13.8635,"RA":286.3525,"AM":2.9900,"t":"S"},{"DE":34.9873,"RA":32.3859,"AM":3.0000,"t":"S"},{"DE":44.4985,"RA":167.4159,"AM":3.0000,"t":"S"},{"DE":71.8340,"RA":230.1822,"AM":3.0000,"t":"S"},{"DE":-38.0474,"RA":252.9676,"AM":3.0000,"t":"S"},{"DE":-37.3649,"RA":328.4821,"AM":3.0000,"t":"S"},{"DE":47.7876,"RA":55.7312,"AM":3.0100,"t":"S"},{"DE":-30.0634,"RA":95.0783,"AM":3.0200,"t":"S"},{"DE":-23.8333,"RA":105.7561,"AM":3.0200,"t":"S"},{"DE":-22.6198,"RA":182.5312,"AM":3.0200,"t":"S"},{"DE":43.8233,"RA":75.4922,"AM":3.0300,"t":"S"},{"DE":-68.1081,"RA":191.5702,"AM":3.0400,"t":"S"},{"DE":38.3083,"RA":218.0195,"AM":3.0400,"t":"S"},{"DE":27.9597,"RA":292.6803,"AM":3.0500,"t":"S","name":"Albireo"},{"DE":-14.7814,"RA":305.2528,"AM":3.0500,"t":"S"},{"DE":25.1311,"RA":100.9830,"AM":3.0600,"t":"S"},{"DE":41.4995,"RA":155.5823,"AM":3.0600,"t":"S"},{"DE":67.6615,"RA":288.1384,"AM":3.0700,"t":"S"},{"DE":-36.7617,"RA":274.4069,"AM":3.1000,"t":"S"},{"DE":5.9456,"RA":133.8485,"AM":3.1100,"t":"S"},{"DE":-16.1936,"RA":162.4062,"AM":3.1100,"t":"S"},{"DE":-63.0198,"RA":173.9454,"AM":3.1100,"t":"S"},{"DE":-47.2915,"RA":309.3917,"AM":3.1100,"t":"S"},{"DE":-35.7683,"RA":87.7399,"AM":3.1200,"t":"S"},{"DE":48.0418,"RA":134.8024,"AM":3.1200,"t":"S"},{"DE":-55.9901,"RA":254.6551,"AM":3.1200,"t":"S"},{"DE":24.8392,"RA":258.7580,"AM":3.1200,"t":"S"},{"DE":-42.1042,"RA":224.7904,"AM":3.1300,"t":"S"},{"DE":34.3926,"RA":140.2639,"AM":3.1400,"t":"S"},{"DE":-57.0344,"RA":142.8056,"AM":3.1600,"t":"S"},{"DE":36.8092,"RA":258.7618,"AM":3.1600,"t":"S"},{"DE":-43.1959,"RA":99.4403,"AM":3.1700,"t":"S"},{"DE":51.6773,"RA":143.2157,"AM":3.1700,"t":"S"},{"DE":65.7147,"RA":257.1967,"AM":3.1700,"t":"S"},{"DE":-26.9908,"RA":281.4141,"AM":3.1700,"t":"S"},{"DE":41.2345,"RA":76.6287,"AM":3.1800,"t":"S"},{"DE":-64.9751,"RA":220.6274,"AM":3.1800,"t":"S"},{"DE":6.9613,"RA":72.4600,"AM":3.1900,"t":"S"},{"DE":-22.3710,"RA":76.3653,"AM":3.1900,"t":"S"},{"DE":9.3750,"RA":254.4171,"AM":3.1900,"t":"S"},{"DE":-37.0433,"RA":267.4645,"AM":3.1900,"t":"S"},{"DE":30.2269,"RA":318.2341,"AM":3.2100,"t":"S"},{"DE":77.6323,"RA":354.8373,"AM":3.2100,"t":"S"},{"DE":-40.6475,"RA":230.3430,"AM":3.2200,"t":"S"},{"DE":-4.6925,"RA":244.5804,"AM":3.2300,"t":"S"},{"DE":-2.8988,"RA":275.3275,"AM":3.2300,"t":"S"},{"DE":70.5607,"RA":322.1649,"AM":3.2300,"t":"S"},{"DE":-61.9414,"RA":102.0479,"AM":3.2400,"t":"S"},{"DE":-0.8215,"RA":302.8262,"AM":3.2400,"t":"S"},{"DE":-43.3014,"RA":112.3077,"AM":3.2500,"t":"S"},{"DE":-26.6824,"RA":211.5929,"AM":3.2500,"t":"S"},{"DE":-25.2820,"RA":226.0176,"AM":3.2500,"t":"S"},{"DE":32.6896,"RA":284.7359,"AM":3.2500,"t":"S"},{"DE":-74.2390,"RA":56.8094,"AM":3.2600,"t":"S"},{"DE":30.8610,"RA":9.8319,"AM":3.2700,"t":"S"},{"DE":-24.9995,"RA":260.5024,"AM":3.2700,"t":"S"},{"DE":-15.8208,"RA":343.6626,"AM":3.2700,"t":"S"},{"DE":-16.2055,"RA":78.2329,"AM":3.2900,"t":"S"},{"DE":-70.0379,"RA":153.4344,"AM":3.2900,"t":"S"},{"DE":58.9661,"RA":231.2324,"AM":3.2900,"t":"S"},{"DE":-55.0450,"RA":68.4990,"AM":3.3000,"t":"S"},{"DE":-61.6853,"RA":158.0061,"AM":3.3000,"t":"S"},{"DE":22.5068,"RA":93.7194,"AM":3.3100,"t":"S"},{"DE":-56.3777,"RA":261.3486,"AM":3.3100,"t":"S"},{"DE":-46.7184,"RA":16.5211,"AM":3.3200,"t":"S"},{"DE":38.8403,"RA":46.2940,"AM":3.3200,"t":"S"},{"DE":57.0326,"RA":183.8563,"AM":3.3200,"t":"S","name":"Megrez"},{"DE":-43.2392,"RA":258.0383,"AM":3.3200,"t":"S"},{"DE":-9.7736,"RA":269.7566,"AM":3.3200,"t":"S"},{"DE":-27.6704,"RA":286.7351,"AM":3.3200,"t":"S"},{"DE":-62.4739,"RA":63.6061,"AM":3.3300,"t":"S"},{"DE":15.4296,"RA":168.5600,"AM":3.3300,"t":"S"},{"DE":-24.8598,"RA":117.3236,"AM":3.3400,"t":"S"},{"DE":63.6701,"RA":28.5988,"AM":3.3500,"t":"S"},{"DE":-2.3971,"RA":81.1192,"AM":3.3500,"t":"S"},{"DE":12.8956,"RA":101.3224,"AM":3.3500,"t":"S"},{"DE":60.7182,"RA":127.5665,"AM":3.3500,"t":"S"},{"DE":3.1148,"RA":291.3746,"AM":3.3600,"t":"S"},{"DE":-44.6896,"RA":230.6703,"AM":3.3700,"t":"S"},{"DE":6.4188,"RA":131.6938,"AM":3.3800,"t":"S"},{"DE":-0.5958,"RA":203.6733,"AM":3.3800,"t":"S"},{"DE":9.9342,"RA":83.7845,"AM":3.3900,"t":"S"},{"DE":-61.3323,"RA":154.2708,"AM":3.3900,"t":"S"},{"DE":3.3975,"RA":193.9009,"AM":3.3900,"t":"S"},{"DE":58.2013,"RA":332.7136,"AM":3.3900,"t":"S"},{"DE":15.8709,"RA":67.1656,"AM":3.4000,"t":"S"},{"DE":-15.7269,"RA":257.5917,"AM":3.4000,"t":"S"},{"DE":-43.3182,"RA":22.0914,"AM":3.4100,"t":"S"},{"DE":12.4903,"RA":60.1701,"AM":3.4100,"t":"S"},{"DE":-41.6877,"RA":207.3762,"AM":3.4100,"t":"S"},{"DE":-52.0992,"RA":228.0714,"AM":3.4100,"t":"S"},{"DE":61.8388,"RA":311.3222,"AM":3.4100,"t":"S"},{"DE":10.8314,"RA":340.3655,"AM":3.4100,"t":"S"},{"DE":29.5788,"RA":28.2704,"AM":3.4200,"t":"S"},{"DE":-38.3967,"RA":240.0305,"AM":3.4200,"t":"S"},{"DE":27.7207,"RA":266.6148,"AM":3.4200,"t":"S"},{"DE":-66.2032,"RA":311.2397,"AM":3.4200,"t":"S"},{"DE":-58.9669,"RA":137.7421,"AM":3.4300,"t":"S"},{"DE":23.4173,"RA":154.1726,"AM":3.4300,"t":"S"},{"DE":-4.8826,"RA":286.5623,"AM":3.4300,"t":"S"},{"DE":42.9144,"RA":154.2743,"AM":3.4500,"t":"S"},{"DE":57.8152,"RA":12.2739,"AM":3.4600,"t":"S"},{"DE":-10.1823,"RA":17.1475,"AM":3.4600,"t":"S"},{"DE":-52.9824,"RA":119.1947,"AM":3.4600,"t":"S"},{"DE":33.3148,"RA":228.8756,"AM":3.4600,"t":"S"},{"DE":3.2358,"RA":40.8252,"AM":3.4700,"t":"S"},{"DE":-42.4737,"RA":207.4041,"AM":3.4700,"t":"S"},{"DE":16.7627,"RA":151.8331,"AM":3.4800,"t":"S"},{"DE":38.9223,"RA":250.7240,"AM":3.4800,"t":"S"},{"DE":-15.9375,"RA":26.0172,"AM":3.4900,"t":"S"},{"DE":-27.9348,"RA":105.4298,"AM":3.4900,"t":"S"},{"DE":33.0943,"RA":169.6197,"AM":3.4900,"t":"S"},{"DE":40.3906,"RA":225.4865,"AM":3.4900,"t":"S"},{"DE":-45.9685,"RA":276.7434,"AM":3.4900,"t":"S"},{"DE":-51.3169,"RA":342.1386,"AM":3.4900,"t":"S"},{"DE":-32.5085,"RA":102.4602,"AM":3.5000,"t":"S"},{"DE":21.9823,"RA":110.0307,"AM":3.5000,"t":"S"},{"DE":66.2004,"RA":342.4203,"AM":3.5000,"t":"S"},{"DE":19.4921,"RA":299.6893,"AM":3.5100,"t":"S"},{"DE":24.6016,"RA":342.5008,"AM":3.5100,"t":"S"},{"DE":-9.7634,"RA":55.8121,"AM":3.5200,"t":"S"},{"DE":9.8923,"RA":145.2876,"AM":3.5200,"t":"S"},{"DE":-54.5678,"RA":149.2156,"AM":3.5200,"t":"S"},{"DE":33.3627,"RA":282.5200,"AM":3.5200,"t":"S","name":"Sheliak"},{"DE":-21.1067,"RA":284.4325,"AM":3.5200,"t":"S"},{"DE":6.1979,"RA":332.5499,"AM":3.5200,"t":"S"},{"DE":-1.4492,"RA":190.4126,"AM":3.5200,"t":"S"},{"DE":19.1804,"RA":67.1541,"AM":3.5300,"t":"S"},{"DE":9.1855,"RA":124.1288,"AM":3.5300,"t":"S"},{"DE":-31.8576,"RA":173.2506,"AM":3.5400,"t":"S"},{"DE":-3.4302,"RA":237.4050,"AM":3.5400,"t":"S"},{"DE":-15.3986,"RA":264.3967,"AM":3.5400,"t":"S"},{"DE":-33.7983,"RA":64.4736,"AM":3.5500,"t":"S"},{"DE":-14.8219,"RA":86.7389,"AM":3.5500,"t":"S"},{"DE":-46.0581,"RA":214.8509,"AM":3.5500,"t":"S"},{"DE":72.7328,"RA":275.2610,"AM":3.5500,"t":"S"},{"DE":-66.1821,"RA":302.1774,"AM":3.5500,"t":"S"},{"DE":-8.8239,"RA":4.8570,"AM":3.5600,"t":"S"},{"DE":-51.5122,"RA":34.1273,"AM":3.5600,"t":"S"},{"DE":-14.7785,"RA":169.8352,"AM":3.5600,"t":"S"},{"DE":-38.0175,"RA":253.0839,"AM":3.5600,"t":"S"},{"DE":24.3980,"RA":116.1119,"AM":3.5700,"t":"S"},{"DE":47.1565,"RA":135.9064,"AM":3.5700,"t":"S"},{"DE":30.3714,"RA":217.9575,"AM":3.5700,"t":"S"},{"DE":-36.2614,"RA":230.4516,"AM":3.5700,"t":"S"},{"DE":16.5404,"RA":109.5232,"AM":3.5800,"t":"S"},{"DE":-12.5449,"RA":304.5136,"AM":3.5800,"t":"S"},{"DE":48.6282,"RA":24.4981,"AM":3.5900,"t":"S"},{"DE":-6.8444,"RA":79.4016,"AM":3.5900,"t":"S"},{"DE":-22.4484,"RA":86.1159,"AM":3.5900,"t":"S"},{"DE":1.7647,"RA":177.6738,"AM":3.5900,"t":"S"},{"DE":-60.4011,"RA":185.3405,"AM":3.5900,"t":"S"},{"DE":-8.1833,"RA":21.0058,"AM":3.6000,"t":"S"},{"DE":33.9613,"RA":103.1972,"AM":3.6000,"t":"S"},{"DE":-52.9219,"RA":130.0733,"AM":3.6000,"t":"S"},{"DE":-40.4668,"RA":142.6751,"AM":3.6000,"t":"S"},{"DE":-28.1351,"RA":234.2560,"AM":3.6000,"t":"S"},{"DE":-60.6838,"RA":262.7748,"AM":3.6000,"t":"S"},{"DE":27.2605,"RA":42.4959,"AM":3.6100,"t":"S"},{"DE":9.0289,"RA":51.2033,"AM":3.6100,"t":"S"},{"DE":-12.3541,"RA":152.6470,"AM":3.6100,"t":"S"},{"DE":-71.5489,"RA":195.5664,"AM":3.6100,"t":"S"},{"DE":-64.7239,"RA":266.4333,"AM":3.6100,"t":"S"},{"DE":15.3458,"RA":22.8709,"AM":3.6200,"t":"S"},{"DE":24.0534,"RA":57.2906,"AM":3.6200,"t":"S"},{"DE":-37.9686,"RA":116.3137,"AM":3.6200,"t":"S"},{"DE":-42.3613,"RA":253.6460,"AM":3.6200,"t":"S"},{"DE":42.3260,"RA":345.4803,"AM":3.6200,"t":"S"},{"DE":-66.7288,"RA":176.4021,"AM":3.6300,"t":"S"},{"DE":14.5951,"RA":309.3872,"AM":3.6400,"t":"S"},{"DE":15.6276,"RA":64.9483,"AM":3.6500,"t":"S"},{"DE":63.0619,"RA":142.8818,"AM":3.6500,"t":"S"},{"DE":15.4218,"RA":236.5469,"AM":3.6500,"t":"S"},{"DE":-50.0915,"RA":271.6578,"AM":3.6500,"t":"S"},{"DE":-0.0200,"RA":337.2080,"AM":3.6500,"t":"S"},{"DE":29.1057,"RA":231.9573,"AM":3.6600,"t":"S"},{"DE":-29.7778,"RA":234.6641,"AM":3.6600,"t":"S"},{"DE":64.3758,"RA":211.0975,"AM":3.6700,"t":"S","name":"Thuban"},{"DE":-58.4542,"RA":313.7025,"AM":3.6700,"t":"S"},{"DE":5.6051,"RA":72.8015,"AM":3.6800,"t":"S"},{"DE":-33.1864,"RA":130.8981,"AM":3.6800,"t":"S"},{"DE":18.5343,"RA":296.8469,"AM":3.6800,"t":"S"},{"DE":-21.1724,"RA":347.3616,"AM":3.6800,"t":"S"},{"DE":53.8969,"RA":9.2428,"AM":3.6900,"t":"S"},{"DE":-51.6089,"RA":28.9885,"AM":3.6900,"t":"S"},{"DE":41.0758,"RA":75.6195,"AM":3.6900,"t":"S"},{"DE":-62.5079,"RA":146.3118,"AM":3.6900,"t":"S"},{"DE":47.7794,"RA":176.5127,"AM":3.6900,"t":"S"},{"DE":-16.6623,"RA":325.0227,"AM":3.6900,"t":"S"},{"DE":-21.7579,"RA":49.8792,"AM":3.7000,"t":"S"},{"DE":29.2479,"RA":269.4412,"AM":3.7000,"t":"S"},{"DE":3.2823,"RA":349.2914,"AM":3.7000,"t":"S"},{"DE":2.4407,"RA":73.5629,"AM":3.7100,"t":"S"},{"DE":-14.1677,"RA":89.1012,"AM":3.7100,"t":"S"},{"DE":-40.5758,"RA":118.0543,"AM":3.7100,"t":"S"},{"DE":4.4777,"RA":237.7040,"AM":3.7100,"t":"S"},{"DE":9.5638,"RA":271.8374,"AM":3.7100,"t":"S"},{"DE":6.4068,"RA":298.8283,"AM":3.7100,"t":"S","name":"Alshain"},{"DE":-9.4583,"RA":53.2327,"AM":3.7200,"t":"S"},{"DE":24.1133,"RA":56.2189,"AM":3.7200,"t":"S"},{"DE":54.2847,"RA":89.8817,"AM":3.7200,"t":"S"},{"DE":43.9279,"RA":316.2328,"AM":3.7200,"t":"S"},{"DE":9.7327,"RA":51.7923,"AM":3.7300,"t":"S"},{"DE":1.8929,"RA":221.5622,"AM":3.7300,"t":"S"},{"DE":56.8726,"RA":268.3820,"AM":3.7300,"t":"S"},{"DE":-77.3900,"RA":325.3688,"AM":3.7300,"t":"S"},{"DE":-7.5796,"RA":343.1536,"AM":3.7300,"t":"S"},{"DE":-10.3350,"RA":27.8651,"AM":3.7400,"t":"S"},{"DE":19.1531,"RA":245.4801,"AM":3.7400,"t":"S"},{"DE":38.0453,"RA":318.6978,"AM":3.7400,"t":"S"},{"DE":-47.0977,"RA":136.0387,"AM":3.7500,"t":"S"},{"DE":2.7073,"RA":266.9732,"AM":3.7500,"t":"S"},{"DE":-62.4898,"RA":83.4063,"AM":3.7600,"t":"S"},{"DE":-20.8791,"RA":87.8304,"AM":3.7600,"t":"S"},{"DE":-7.0331,"RA":97.2045,"AM":3.7600,"t":"S"},{"DE":-21.7415,"RA":286.1707,"AM":3.7600,"t":"S"},{"DE":51.7298,"RA":292.4265,"AM":3.7600,"t":"S"},{"DE":50.2825,"RA":337.8227,"AM":3.7600,"t":"S"},{"DE":55.8955,"RA":42.6742,"AM":3.7700,"t":"S"},{"DE":42.5785,"RA":56.2985,"AM":3.7700,"t":"S"},{"DE":17.5425,"RA":65.7337,"AM":3.7700,"t":"S"},{"DE":-2.6001,"RA":84.6865,"AM":3.7700,"t":"S"},{"DE":-66.1369,"RA":126.4343,"AM":3.7700,"t":"S"},{"DE":-46.6487,"RA":130.1565,"AM":3.7700,"t":"S"},{"DE":-59.0414,"RA":252.4464,"AM":3.7700,"t":"S"},{"DE":15.9121,"RA":309.9095,"AM":3.7700,"t":"S"},{"DE":-22.4113,"RA":321.6668,"AM":3.7700,"t":"S"},{"DE":25.3451,"RA":331.7527,"AM":3.7700,"t":"S"},{"DE":-70.4989,"RA":107.1868,"AM":3.7800,"t":"S"},{"DE":27.7981,"RA":111.4317,"AM":3.7800,"t":"S"},{"DE":59.0387,"RA":147.7480,"AM":3.7800,"t":"S"},{"DE":-58.8532,"RA":163.3734,"AM":3.7800,"t":"S"},{"DE":13.7283,"RA":220.2873,"AM":3.7800,"t":"S"},{"DE":-9.4958,"RA":311.9190,"AM":3.7800,"t":"S"},{"DE":44.8575,"RA":47.3739,"AM":3.7900,"t":"S"},{"DE":34.2149,"RA":163.3279,"AM":3.7900,"t":"S"},{"DE":-28.9876,"RA":48.0187,"AM":3.8000,"t":"S"},{"DE":-26.8038,"RA":114.7078,"AM":3.8000,"t":"S"},{"DE":10.5389,"RA":233.7006,"AM":3.8000,"t":"S"},{"DE":53.3685,"RA":289.2756,"AM":3.8000,"t":"S"},{"DE":46.7413,"RA":303.4079,"AM":3.8000,"t":"S"},{"DE":-30.5623,"RA":68.8877,"AM":3.8100,"t":"S"},{"DE":-58.7394,"RA":156.9697,"AM":3.8100,"t":"S"},{"DE":26.2956,"RA":235.6857,"AM":3.8100,"t":"S"},{"DE":46.4582,"RA":354.3908,"AM":3.8100,"t":"S"},{"DE":2.7638,"RA":30.5118,"AM":3.8200,"t":"S"},{"DE":36.8026,"RA":139.7110,"AM":3.8200,"t":"S"},{"DE":69.3311,"RA":172.8511,"AM":3.8200,"t":"S"},{"DE":1.9839,"RA":247.7284,"AM":3.8200,"t":"S"},{"DE":46.0063,"RA":264.8662,"AM":3.8200,"t":"S"},{"DE":-16.8363,"RA":156.5226,"AM":3.8300,"t":"S"},{"DE":-42.1008,"RA":209.5678,"AM":3.8300,"t":"S"},{"DE":-79.0448,"RA":221.9655,"AM":3.8300,"t":"S"},{"DE":-64.8069,"RA":56.0489,"AM":3.8400,"t":"S"},{"DE":32.2882,"RA":56.0797,"AM":3.8400,"t":"S"},{"DE":15.9622,"RA":67.1437,"AM":3.8400,"t":"S"},{"DE":-60.6446,"RA":133.7619,"AM":3.8400,"t":"S"},{"DE":9.3066,"RA":158.2028,"AM":3.8400,"t":"S"},{"DE":-48.2256,"RA":159.3258,"AM":3.8400,"t":"S"},{"DE":-72.1330,"RA":188.1170,"AM":3.8400,"t":"S"},{"DE":28.7625,"RA":271.8856,"AM":3.8400,"t":"S"},{"DE":-21.0588,"RA":273.4409,"AM":3.8400,"t":"S"},{"DE":70.2679,"RA":297.0428,"AM":3.8400,"t":"S"},{"DE":-42.2944,"RA":63.5004,"AM":3.8500,"t":"S"},{"DE":-51.0665,"RA":86.8212,"AM":3.8500,"t":"S"},{"DE":-33.4364,"RA":95.5285,"AM":3.8500,"t":"S"},{"DE":-42.1219,"RA":153.6841,"AM":3.8500,"t":"S"},{"DE":69.7882,"RA":188.3709,"AM":3.8500,"t":"S"},{"DE":-48.5413,"RA":189.4259,"AM":3.8500,"t":"S"},{"DE":15.6616,"RA":239.1132,"AM":3.8500,"t":"S"},{"DE":21.7698,"RA":275.9245,"AM":3.8500,"t":"S"},{"DE":-8.2441,"RA":278.8018,"AM":3.8500,"t":"S"},{"DE":38.4993,"RA":14.1883,"AM":3.8600,"t":"S"},{"DE":-14.3040,"RA":69.5451,"AM":3.8600,"t":"S"},{"DE":-35.4705,"RA":82.8031,"AM":3.8600,"t":"S"},{"DE":-63.6857,"RA":243.8595,"AM":3.8600,"t":"S"},{"DE":-78.8971,"RA":248.3641,"AM":3.8600,"t":"S"},{"DE":37.2505,"RA":269.0633,"AM":3.8600,"t":"S"},{"DE":-1.3873,"RA":335.4141,"AM":3.8600,"t":"S"},{"DE":24.3677,"RA":56.4567,"AM":3.8700,"t":"S"},{"DE":-46.0415,"RA":131.5069,"AM":3.8700,"t":"S"},{"DE":-44.8036,"RA":209.6698,"AM":3.8700,"t":"S"},{"DE":-5.6582,"RA":220.7651,"AM":3.8700,"t":"S"},{"DE":-29.2141,"RA":239.2212,"AM":3.8700,"t":"S"},{"DE":1.0057,"RA":298.1182,"AM":3.8700,"t":"S"},{"DE":-45.7474,"RA":2.3525,"AM":3.8800,"t":"S"},{"DE":19.2939,"RA":28.3825,"AM":3.8800,"t":"S"},{"DE":26.0070,"RA":148.1910,"AM":3.8800,"t":"S"},{"DE":-48.7378,"RA":227.9838,"AM":3.8800,"t":"S"},{"DE":-45.2467,"RA":347.5896,"AM":3.8800,"t":"S"},{"DE":-8.8981,"RA":44.1069,"AM":3.8900,"t":"S"},{"DE":-24.1842,"RA":103.5331,"AM":3.8900,"t":"S"},{"DE":2.3143,"RA":138.5911,"AM":3.8900,"t":"S"},{"DE":-0.6668,"RA":184.9765,"AM":3.8900,"t":"S"},{"DE":35.0834,"RA":299.0766,"AM":3.8900,"t":"S"},{"DE":-1.1428,"RA":144.9640,"AM":3.9000,"t":"S"},{"DE":-54.4910,"RA":170.2518,"AM":3.9000,"t":"S"},{"DE":-39.4073,"RA":202.7611,"AM":3.9000,"t":"S"},{"DE":5.9893,"RA":60.7891,"AM":3.9100,"t":"S"},{"DE":-3.9064,"RA":126.4151,"AM":3.9100,"t":"S"},{"DE":-50.2306,"RA":187.0100,"AM":3.9100,"t":"S"},{"DE":-47.0512,"RA":226.2795,"AM":3.9100,"t":"S"},{"DE":-14.7895,"RA":233.8816,"AM":3.9100,"t":"S"},{"DE":46.3134,"RA":244.9352,"AM":3.9100,"t":"S"},{"DE":30.9264,"RA":255.0724,"AM":3.9200,"t":"S"},{"DE":-17.8472,"RA":290.4182,"AM":3.9200,"t":"S"},{"DE":5.2478,"RA":318.9560,"AM":3.9200,"t":"S"},{"DE":-43.6798,"RA":6.5507,"AM":3.9300,"t":"S"},{"DE":-49.0727,"RA":22.8128,"AM":3.9300,"t":"S"},{"DE":52.7625,"RA":43.5644,"AM":3.9300,"t":"S"},{"DE":-3.3525,"RA":69.0798,"AM":3.9300,"t":"S"},{"DE":-72.6061,"RA":115.4551,"AM":3.9300,"t":"S"},{"DE":-58.9750,"RA":167.1475,"AM":3.9300,"t":"S"},{"DE":-20.6692,"RA":241.7018,"AM":3.9300,"t":"S"},{"DE":2.9316,"RA":270.1613,"AM":3.9300,"t":"S"},{"DE":-55.2458,"RA":17.0961,"AM":3.9400,"t":"S"},{"DE":-9.5511,"RA":115.3118,"AM":3.9400,"t":"S"},{"DE":-28.9548,"RA":115.9519,"AM":3.9400,"t":"S"},{"DE":18.1543,"RA":131.1712,"AM":3.9400,"t":"S"},{"DE":41.1671,"RA":314.2934,"AM":3.9400,"t":"S"},{"DE":72.4213,"RA":30.8590,"AM":3.9500,"t":"S"},{"DE":-19.2559,"RA":99.1710,"AM":3.9500,"t":"S"},{"DE":54.9205,"RA":200.9849,"AM":3.9500,"t":"S"},{"DE":47.7125,"RA":62.1654,"AM":3.9600,"t":"S"},{"DE":-42.8151,"RA":89.7867,"AM":3.9600,"t":"S"},{"DE":41.7829,"RA":135.1603,"AM":3.9600,"t":"S"},{"DE":-62.3170,"RA":137.8198,"AM":3.9600,"t":"S"},{"DE":-44.4590,"RA":290.6595,"AM":3.9600,"t":"S"},{"DE":-40.6159,"RA":290.9715,"AM":3.9600,"t":"S"},{"DE":47.7142,"RA":303.8680,"AM":3.9600,"t":"S"},{"DE":-20.1006,"RA":350.7426,"AM":3.9600,"t":"S"},{"DE":-34.0168,"RA":66.0092,"AM":3.9700,"t":"S"},{"DE":39.1485,"RA":87.8725,"AM":3.9700,"t":"S"},{"DE":-67.9572,"RA":109.2076,"AM":3.9700,"t":"S"},{"DE":-35.3084,"RA":130.0256,"AM":3.9700,"t":"S"},{"DE":-52.3685,"RA":182.9130,"AM":3.9700,"t":"S"},{"DE":-33.6272,"RA":237.7397,"AM":3.9700,"t":"S"},{"DE":-72.9105,"RA":300.1477,"AM":3.9700,"t":"S"},{"DE":-43.4956,"RA":337.3174,"AM":3.9700,"t":"S"},{"DE":23.5657,"RA":341.6328,"AM":3.9700,"t":"S"},{"DE":35.7910,"RA":59.7412,"AM":3.9800,"t":"S"},{"DE":45.5918,"RA":323.4952,"AM":3.9800,"t":"S"},{"DE":-21.0778,"RA":30.0013,"AM":3.9900,"t":"S"},{"DE":-6.2748,"RA":93.7139,"AM":3.9900,"t":"S"},{"DE":-74.0316,"RA":156.0989,"AM":3.9900,"t":"S"},{"DE":54.9880,"RA":201.3062,"AM":3.9900,"t":"S","name":"Alcor"},{"DE":-58.2357,"RA":349.3575,"AM":3.9900,"t":"S"},{"DE":-66.3961,"RA":135.6117,"AM":4.0000,"t":"S"},{"DE":10.5295,"RA":170.9810,"AM":4.0000,"t":"S"},{"DE":-19.4607,"RA":242.9989,"AM":4.0000,"t":"S"},{"DE":50.6887,"RA":25.9151,"AM":4.0100,"t":"S"},{"DE":-3.2547,"RA":71.3756,"AM":4.0100,"t":"S"},{"DE":20.5703,"RA":106.0272,"AM":4.0100,"t":"S"},{"DE":-26.7727,"RA":108.7027,"AM":4.0100,"t":"S"},{"DE":-37.7935,"RA":220.4900,"AM":4.0100,"t":"S"},{"DE":58.5653,"RA":240.4730,"AM":4.0100,"t":"S"},{"DE":-50.1555,"RA":244.9603,"AM":4.0100,"t":"S"},{"DE":-71.4281,"RA":280.7589,"AM":4.0100,"t":"S"},{"DE":30.3686,"RA":307.3489,"AM":4.0100,"t":"S"},{"DE":-27.7098,"RA":132.6331,"AM":4.0200,"t":"S"},{"DE":-24.7289,"RA":182.1034,"AM":4.0200,"t":"S"},{"DE":15.0683,"RA":284.9057,"AM":4.0200,"t":"S"},{"DE":-5.7391,"RA":285.4201,"AM":4.0200,"t":"S"},{"DE":33.8472,"RA":34.3286,"AM":4.0300,"t":"S"},{"DE":60.4422,"RA":75.8545,"AM":4.0300,"t":"S"},{"DE":28.7599,"RA":131.6743,"AM":4.0300,"t":"S"},{"DE":-57.1779,"RA":193.6485,"AM":4.0300,"t":"S"},{"DE":2.5001,"RA":271.3637,"AM":4.0300,"t":"S"},{"DE":11.3033,"RA":308.3032,"AM":4.0300,"t":"S"},{"DE":6.8633,"RA":359.8279,"AM":4.0300,"t":"S"},{"DE":-6.8376,"RA":62.9664,"AM":4.0400,"t":"S"},{"DE":6.5294,"RA":176.4648,"AM":4.0400,"t":"S"},{"DE":51.8507,"RA":216.2995,"AM":4.0400,"t":"S"},{"DE":-0.1175,"RA":338.8391,"AM":4.0400,"t":"S"},{"DE":49.6133,"RA":47.2651,"AM":4.0500,"t":"S"},{"DE":-76.9197,"RA":124.6305,"AM":4.0500,"t":"S"},{"DE":-42.6493,"RA":131.0998,"AM":4.0500,"t":"S"},{"DE":6.0293,"RA":170.2841,"AM":4.0500,"t":"S"},{"DE":15.7979,"RA":207.3693,"AM":4.0500,"t":"S"},{"DE":-37.8853,"RA":215.1393,"AM":4.0500,"t":"S"},{"DE":-49.4258,"RA":219.4718,"AM":4.0500,"t":"S"},{"DE":-13.5926,"RA":342.3979,"AM":4.0500,"t":"S"},{"DE":13.5145,"RA":74.0928,"AM":4.0600,"t":"S"},{"DE":26.8957,"RA":113.9806,"AM":4.0600,"t":"S"},{"DE":-17.6840,"RA":171.2205,"AM":4.0600,"t":"S"},{"DE":-67.9607,"RA":184.3938,"AM":4.0600,"t":"S"},{"DE":-64.0031,"RA":184.6095,"AM":4.0600,"t":"S"},{"DE":-35.1737,"RA":220.9144,"AM":4.0600,"t":"S"},{"DE":-53.1604,"RA":254.8960,"AM":4.0600,"t":"S"},{"DE":-6.0005,"RA":214.0036,"AM":4.0700,"t":"S"},{"DE":-45.2799,"RA":227.2109,"AM":4.0700,"t":"S"},{"DE":-58.8012,"RA":229.3788,"AM":4.0700,"t":"S"},{"DE":58.4152,"RA":337.2927,"AM":4.0700,"t":"S"},{"DE":24.2672,"RA":11.8347,"AM":4.0800,"t":"S"},{"DE":-68.6594,"RA":35.4375,"AM":4.0800,"t":"S"},{"DE":0.3285,"RA":39.8707,"AM":4.0800,"t":"S"},{"DE":-23.6245,"RA":45.5979,"AM":4.0800,"t":"S"},{"DE":-12.0386,"RA":103.5475,"AM":4.0800,"t":"S"},{"DE":-59.2298,"RA":143.6111,"AM":4.0800,"t":"S"},{"DE":-18.2988,"RA":164.9437,"AM":4.0800,"t":"S"},{"DE":43.9461,"RA":283.8337,"AM":4.0800,"t":"S"},{"DE":-17.2329,"RA":316.4868,"AM":4.0800,"t":"S"},{"DE":19.8045,"RA":320.5217,"AM":4.0800,"t":"S"},{"DE":9.2907,"RA":84.2266,"AM":4.0900,"t":"S"},{"DE":18.1416,"RA":237.1849,"AM":4.0900,"t":"S"},{"DE":41.4055,"RA":24.1995,"AM":4.1000,"t":"S"},{"DE":49.2284,"RA":41.0495,"AM":4.1000,"t":"S"},{"DE":-46.3732,"RA":117.3096,"AM":4.1000,"t":"S"},{"DE":-49.0706,"RA":277.2076,"AM":4.1000,"t":"S"},{"DE":-39.3408,"RA":287.5073,"AM":4.1000,"t":"S"},{"DE":-39.8554,"RA":40.1667,"AM":4.1100,"t":"S"},{"DE":-15.6333,"RA":105.9396,"AM":4.1100,"t":"S"},{"DE":-42.9891,"RA":129.4110,"AM":4.1100,"t":"S"},{"DE":-14.8466,"RA":147.8696,"AM":4.1100,"t":"S"},{"DE":-78.6078,"RA":158.8675,"AM":4.1100,"t":"S"},{"DE":-61.1784,"RA":176.6285,"AM":4.1100,"t":"S"},{"DE":-66.3170,"RA":234.1800,"AM":4.1100,"t":"S"},{"DE":-37.9045,"RA":287.3680,"AM":4.1100,"t":"S"},{"DE":-52.7541,"RA":345.2202,"AM":4.1100,"t":"S"},{"DE":-68.2669,"RA":39.8970,"AM":4.1200,"t":"S"},{"DE":48.4093,"RA":63.7244,"AM":4.1200,"t":"S"},{"DE":9.6473,"RA":90.5958,"AM":4.1200,"t":"S"},{"DE":8.7330,"RA":181.3023,"AM":4.1200,"t":"S"},{"DE":-41.8683,"RA":298.8154,"AM":4.1200,"t":"S"},{"DE":-26.9191,"RA":312.9554,"AM":4.1200,"t":"S"},{"DE":-43.7492,"RA":337.4393,"AM":4.1200,"t":"S"},{"DE":-7.8081,"RA":80.9868,"AM":4.1300,"t":"S"},{"DE":20.2121,"RA":97.2408,"AM":4.1300,"t":"S"},{"DE":-16.7293,"RA":238.4564,"AM":4.1300,"t":"S"},{"DE":-25.2709,"RA":311.5239,"AM":4.1300,"t":"S"},{"DE":-81.3816,"RA":341.5154,"AM":4.1300,"t":"S"},{"DE":5.6263,"RA":354.9877,"AM":4.1300,"t":"S"},{"DE":12.9367,"RA":52.7182,"AM":4.1400,"t":"S"},{"DE":23.9484,"RA":56.5816,"AM":4.1400,"t":"S"},{"DE":5.7038,"RA":129.4140,"AM":4.1400,"t":"S"},{"DE":-64.6137,"RA":181.7203,"AM":4.1400,"t":"S"},{"DE":31.3591,"RA":233.2324,"AM":4.1400,"t":"S"},{"DE":26.8779,"RA":239.3969,"AM":4.1400,"t":"S"},{"DE":25.6450,"RA":326.1614,"AM":4.1400,"t":"S"},{"DE":37.7487,"RA":333.9924,"AM":4.1400,"t":"S"},{"DE":-0.4928,"RA":107.9661,"AM":4.1500,"t":"S"},{"DE":37.1459,"RA":260.9206,"AM":4.1500,"t":"S"},{"DE":44.3339,"RA":355.1020,"AM":4.1500,"t":"S"},{"DE":23.2633,"RA":91.0301,"AM":4.1600,"t":"S"},{"DE":31.7845,"RA":112.2779,"AM":4.1600,"t":"S"},{"DE":-24.1753,"RA":261.5926,"AM":4.1600,"t":"S"},{"DE":62.9318,"RA":8.2500,"AM":4.1700,"t":"S"},{"DE":-36.2002,"RA":57.3636,"AM":4.1700,"t":"S"},{"DE":-7.7833,"RA":334.2085,"AM":4.1700,"t":"S"},{"DE":-10.2737,"RA":213.2239,"AM":4.1800,"t":"S"},{"DE":46.0883,"RA":214.0961,"AM":4.1800,"t":"S"},{"DE":-35.2553,"RA":249.0936,"AM":4.1800,"t":"S"},{"DE":57.0436,"RA":333.7582,"AM":4.1800,"t":"S"},{"DE":-27.0436,"RA":340.1639,"AM":4.1800,"t":"S"},{"DE":-34.4508,"RA":207.3614,"AM":4.1900,"t":"S"},{"DE":20.5463,"RA":281.4155,"AM":4.1900,"t":"S"},{"DE":5.9481,"RA":82.6960,"AM":4.2000,"t":"S"},{"DE":-22.8801,"RA":119.2148,"AM":4.2000,"t":"S"},{"DE":36.7072,"RA":156.9709,"AM":4.2000,"t":"S"},{"DE":42.4370,"RA":248.5258,"AM":4.2000,"t":"S"},{"DE":12.1729,"RA":341.6732,"AM":4.2000,"t":"S"},{"DE":-32.5396,"RA":343.9871,"AM":4.2000,"t":"S"},{"DE":59.9403,"RA":52.2672,"AM":4.2100,"t":"S"},{"DE":22.2939,"RA":66.3423,"AM":4.2100,"t":"S"},{"DE":82.0373,"RA":251.4924,"AM":4.2100,"t":"S"},{"DE":62.9941,"RA":307.3952,"AM":4.2100,"t":"S"},{"DE":-65.3662,"RA":321.6106,"AM":4.2100,"t":"S"},{"DE":38.3186,"RA":42.6459,"AM":4.2200,"t":"S"},{"DE":-23.2497,"RA":56.7121,"AM":4.2200,"t":"S"},{"DE":-48.1029,"RA":118.3257,"AM":4.2200,"t":"S"},{"DE":-36.8023,"RA":241.6481,"AM":4.2200,"t":"S"},{"DE":-18.4563,"RA":246.7560,"AM":4.2200,"t":"S"},{"DE":71.3378,"RA":275.1893,"AM":4.2200,"t":"S"},{"DE":-4.7479,"RA":281.7936,"AM":4.2200,"t":"S"},{"DE":-62.1876,"RA":283.0543,"AM":4.2200,"t":"S"},{"DE":36.8986,"RA":283.6262,"AM":4.2200,"t":"S"},{"DE":30.7197,"RA":311.4156,"AM":4.2200,"t":"S"},{"DE":39.3947,"RA":319.3540,"AM":4.2200,"t":"S"},{"DE":-6.0490,"RA":348.5807,"AM":4.2200,"t":"S"},{"DE":-64.8748,"RA":5.0121,"AM":4.2300,"t":"S"},{"DE":28.8835,"RA":115.8280,"AM":4.2300,"t":"S"},{"DE":27.8782,"RA":197.9686,"AM":4.2300,"t":"S"},{"DE":-33.0437,"RA":206.4221,"AM":4.2300,"t":"S"},{"DE":1.5445,"RA":210.4116,"AM":4.2300,"t":"S"},{"DE":44.9349,"RA":242.1924,"AM":4.2300,"t":"S"},{"DE":-77.5174,"RA":250.7719,"AM":4.2300,"t":"S"},{"DE":-37.0634,"RA":286.6046,"AM":4.2300,"t":"S"},{"DE":58.7800,"RA":325.8769,"AM":4.2300,"t":"S"},{"DE":49.3096,"RA":326.6984,"AM":4.2300,"t":"S"},{"DE":86.2571,"RA":17.1842,"AM":4.2400,"t":"S"},{"DE":-47.7038,"RA":36.7463,"AM":4.2400,"t":"S"},{"DE":-13.8587,"RA":41.0306,"AM":4.2400,"t":"S"},{"DE":-79.3122,"RA":184.5872,"AM":4.2400,"t":"S"},{"DE":41.3575,"RA":188.4362,"AM":4.2400,"t":"S"},{"DE":-34.7044,"RA":247.8456,"AM":4.2400,"t":"S"},{"DE":-12.8753,"RA":265.3536,"AM":4.2400,"t":"S"},{"DE":-9.0877,"RA":348.9729,"AM":4.2400,"t":"S"},{"DE":-68.8759,"RA":18.9406,"AM":4.2500,"t":"S"},{"DE":50.3513,"RA":61.6460,"AM":4.2500,"t":"S"},{"DE":10.1608,"RA":68.9136,"AM":4.2500,"t":"S"},{"DE":41.2648,"RA":69.1726,"AM":4.2500,"t":"S"},{"DE":-8.7541,"RA":77.2866,"AM":4.2500,"t":"S"},{"DE":43.1881,"RA":125.7088,"AM":4.2500,"t":"S"},{"DE":-40.1789,"RA":193.3591,"AM":4.2500,"t":"S"},{"DE":75.6960,"RA":216.8814,"AM":4.2500,"t":"S"},{"DE":61.1208,"RA":326.3622,"AM":4.2500,"t":"S"},{"DE":47.2418,"RA":17.3755,"AM":4.2600,"t":"S"},{"DE":9.1577,"RA":26.3485,"AM":4.2600,"t":"S"},{"DE":-43.0698,"RA":49.9792,"AM":4.2600,"t":"S","name":"82 G. Eri"},{"DE":-21.6329,"RA":53.4470,"AM":4.2600,"t":"S"},{"DE":-51.4866,"RA":64.0065,"AM":4.2600,"t":"S"},{"DE":66.3427,"RA":73.5125,"AM":4.2600,"t":"S"},{"DE":11.8577,"RA":134.6218,"AM":4.2600,"t":"S"},{"DE":-38.6353,"RA":264.1368,"AM":4.2600,"t":"S"},{"DE":21.5958,"RA":270.3767,"AM":4.2600,"t":"S"},{"DE":64.6280,"RA":330.9470,"AM":4.2600,"t":"S"},{"DE":7.8901,"RA":15.7359,"AM":4.2700,"t":"S"},{"DE":10.1141,"RA":41.2356,"AM":4.2700,"t":"S"},{"DE":8.8924,"RA":63.8836,"AM":4.2700,"t":"S"},{"DE":12.5108,"RA":69.5394,"AM":4.2700,"t":"S"},{"DE":22.9569,"RA":70.5613,"AM":4.2700,"t":"S"},{"DE":-49.9062,"RA":196.7277,"AM":4.2700,"t":"S"},{"DE":-47.8753,"RA":229.6335,"AM":4.2700,"t":"S"},{"DE":-44.7998,"RA":290.8046,"AM":4.2700,"t":"S"},{"DE":16.1243,"RA":311.6646,"AM":4.2700,"t":"S"},{"DE":6.3790,"RA":351.9921,"AM":4.2700,"t":"S"},{"DE":22.8136,"RA":66.5769,"AM":4.2800,"t":"S"},{"DE":81.3264,"RA":144.2723,"AM":4.2800,"t":"S"},{"DE":-31.0678,"RA":156.7879,"AM":4.2800,"t":"S"},{"DE":-29.8670,"RA":261.8386,"AM":4.2800,"t":"S"},{"DE":56.5677,"RA":303.3493,"AM":4.2800,"t":"S"},{"DE":-16.8345,"RA":320.5616,"AM":4.2800,"t":"S"},{"DE":33.1782,"RA":332.4969,"AM":4.2800,"t":"S"},{"DE":-43.5204,"RA":346.7198,"AM":4.2800,"t":"S"},{"DE":0.4017,"RA":54.2183,"AM":4.2900,"t":"S"},{"DE":-13.1768,"RA":79.8939,"AM":4.2900,"t":"S"},{"DE":-55.6033,"RA":159.8267,"AM":4.2900,"t":"S"},{"DE":-33.9081,"RA":178.2272,"AM":4.2900,"t":"S"},{"DE":77.7945,"RA":236.0145,"AM":4.2900,"t":"S"},{"DE":-16.6127,"RA":247.7849,"AM":4.2900,"t":"S"},{"DE":-13.8697,"RA":331.6093,"AM":4.2900,"t":"S"},{"DE":-32.3461,"RA":337.8764,"AM":4.2900,"t":"S"},{"DE":43.2681,"RA":354.5342,"AM":4.2900,"t":"S"},{"DE":-29.3574,"RA":14.6515,"AM":4.3000,"t":"S"},{"DE":8.4601,"RA":37.0398,"AM":4.3000,"t":"S"},{"DE":24.4673,"RA":56.3021,"AM":4.3000,"t":"S"},{"DE":-37.6202,"RA":57.1494,"AM":4.3000,"t":"S"},{"DE":17.9279,"RA":66.3724,"AM":4.3000,"t":"S"},{"DE":45.9367,"RA":89.9838,"AM":4.3000,"t":"S"},{"DE":3.3987,"RA":130.8062,"AM":4.3000,"t":"S"},{"DE":24.7497,"RA":163.9033,"AM":4.3000,"t":"S"},{"DE":-0.8237,"RA":174.2372,"AM":4.3000,"t":"S"},{"DE":-63.7885,"RA":177.4212,"AM":4.3000,"t":"S"},{"DE":-16.1960,"RA":188.0176,"AM":4.3000,"t":"S"},{"DE":-56.3865,"RA":215.0814,"AM":4.3000,"t":"S"},{"DE":-12.5082,"RA":304.4119,"AM":4.3000,"t":"S"},{"DE":-59.7610,"RA":130.1543,"AM":4.3100,"t":"S"},{"DE":-83.6679,"RA":216.7320,"AM":4.3100,"t":"S"},{"DE":37.3772,"RA":231.1227,"AM":4.3100,"t":"S"},{"DE":-20.8688,"RA":241.8514,"AM":4.3100,"t":"S"},{"DE":-1.1051,"RA":309.5845,"AM":4.3100,"t":"S"},{"DE":48.1926,"RA":54.1224,"AM":4.3200,"t":"S"},{"DE":-19.6715,"RA":70.1105,"AM":4.3200,"t":"S"},{"DE":18.5942,"RA":83.0531,"AM":4.3200,"t":"S"},{"DE":29.4981,"RA":93.8446,"AM":4.3200,"t":"S"},{"DE":-13.5477,"RA":131.5939,"AM":4.3200,"t":"S"},{"DE":22.9680,"RA":142.9301,"AM":4.3200,"t":"S"},{"DE":-63.3129,"RA":180.7567,"AM":4.3200,"t":"S"},{"DE":17.5294,"RA":197.4970,"AM":4.3200,"t":"S"},{"DE":-32.9941,"RA":207.9567,"AM":4.3200,"t":"S"},{"DE":-43.5754,"RA":222.9096,"AM":4.3200,"t":"S"},{"DE":-12.8469,"RA":260.2069,"AM":4.3200,"t":"S"},{"DE":8.9255,"RA":112.0408,"AM":4.3300,"t":"S"},{"DE":-48.9433,"RA":193.2789,"AM":4.3300,"t":"S"},{"DE":-45.3793,"RA":216.5450,"AM":4.3300,"t":"S"},{"DE":-26.6028,"RA":258.8375,"AM":4.3300,"t":"S"},{"DE":-63.6686,"RA":272.1450,"AM":4.3300,"t":"S"},{"DE":36.0645,"RA":274.9655,"AM":4.3300,"t":"S"},{"DE":31.5288,"RA":169.5468,"AM":4.3300,"t":"S"},{"DE":33.7193,"RA":9.2202,"AM":4.3400,"t":"S"},{"DE":29.3118,"RA":9.6390,"AM":4.3400,"t":"S"},{"DE":55.1499,"RA":17.7753,"AM":4.3400,"t":"S"},{"DE":-65.7355,"RA":86.1933,"AM":4.3400,"t":"S"},{"DE":-23.4184,"RA":97.9640,"AM":4.3400,"t":"S"},{"DE":-77.4845,"RA":125.1617,"AM":4.3400,"t":"S"},{"DE":-57.5415,"RA":139.0504,"AM":4.3400,"t":"S"},{"DE":-49.3550,"RA":144.2066,"AM":4.3400,"t":"S"},{"DE":-45.6034,"RA":210.4312,"AM":4.3400,"t":"S"},{"DE":-42.5673,"RA":234.5135,"AM":4.3400,"t":"S"},{"DE":4.1404,"RA":261.6287,"AM":4.3400,"t":"S"},{"DE":37.6051,"RA":281.1931,"AM":4.3400,"t":"S"},{"DE":18.1815,"RA":281.7553,"AM":4.3400,"t":"S"},{"DE":17.3500,"RA":326.1279,"AM":4.3400,"t":"S"},{"DE":47.7069,"RA":337.3826,"AM":4.3400,"t":"S"},{"DE":19.7267,"RA":47.9073,"AM":4.3500,"t":"S"},{"DE":8.9002,"RA":72.6530,"AM":4.3500,"t":"S"},{"DE":-52.9756,"RA":98.7441,"AM":4.3500,"t":"S"},{"DE":58.4228,"RA":104.3192,"AM":4.3500,"t":"S"},{"DE":-68.6171,"RA":121.9826,"AM":4.3500,"t":"S"},{"DE":5.8378,"RA":132.1082,"AM":4.3500,"t":"S"},{"DE":28.2684,"RA":186.7345,"AM":4.3500,"t":"S"},{"DE":-30.1487,"RA":229.4577,"AM":4.3500,"t":"S"},{"DE":86.5865,"RA":263.0538,"AM":4.3500,"t":"S"},{"DE":-61.4939,"RA":275.8068,"AM":4.3500,"t":"S"},{"DE":38.1337,"RA":289.0921,"AM":4.3500,"t":"S"},{"DE":-33.0258,"RA":326.2367,"AM":4.3500,"t":"S"},{"DE":-62.9582,"RA":7.8859,"AM":4.3600,"t":"S"},{"DE":-57.4631,"RA":10.8385,"AM":4.3600,"t":"S"},{"DE":8.8467,"RA":33.2500,"AM":4.3600,"t":"S"},{"DE":47.9952,"RA":52.6437,"AM":4.3600,"t":"S"},{"DE":22.0819,"RA":61.1738,"AM":4.3600,"t":"S"},{"DE":-5.4527,"RA":73.2236,"AM":4.3600,"t":"S"},{"DE":-12.9413,"RA":78.3078,"AM":4.3600,"t":"S"},{"DE":-35.2833,"RA":89.3842,"AM":4.3600,"t":"S"},{"DE":-17.0542,"RA":104.0343,"AM":4.3600,"t":"S"},{"DE":-2.9838,"RA":122.1485,"AM":4.3600,"t":"S"},{"DE":-41.1796,"RA":211.5115,"AM":4.3600,"t":"S"},{"DE":-1.2866,"RA":294.1803,"AM":4.3600,"t":"S"},{"DE":-6.0141,"RA":0.4901,"AM":4.3700,"t":"S"},{"DE":-35.1405,"RA":94.1381,"AM":4.3700,"t":"S"},{"DE":-24.9544,"RA":109.6770,"AM":4.3700,"t":"S"},{"DE":-42.2259,"RA":165.0386,"AM":4.3700,"t":"S"},{"DE":20.8146,"RA":272.1895,"AM":4.3700,"t":"S"},{"DE":-35.2763,"RA":299.9341,"AM":4.3700,"t":"S"},{"DE":-5.5390,"RA":197.4875,"AM":4.3800,"t":"S"},{"DE":77.7114,"RA":302.2222,"AM":4.3800,"t":"S"},{"DE":-20.6420,"RA":351.5116,"AM":4.3800,"t":"S"},{"DE":-37.8183,"RA":353.2427,"AM":4.3800,"t":"S"},{"DE":-46.3027,"RA":28.4115,"AM":4.3900,"t":"S"},{"DE":65.5260,"RA":57.3804,"AM":4.3900,"t":"S"},{"DE":9.4896,"RA":83.7052,"AM":4.3900,"t":"S"},{"DE":20.2762,"RA":88.5958,"AM":4.3900,"t":"S"},{"DE":4.5929,"RA":95.9420,"AM":4.3900,"t":"S"},{"DE":2.3346,"RA":120.5664,"AM":4.3900,"t":"S"},{"DE":9.9975,"RA":151.9761,"AM":4.3900,"t":"S"},{"DE":2.0913,"RA":225.7252,"AM":4.3900,"t":"S"},{"DE":10.1654,"RA":253.5020,"AM":4.3900,"t":"S"},{"DE":-21.1129,"RA":260.2515,"AM":4.3900,"t":"S"},{"DE":18.0139,"RA":295.0241,"AM":4.3900,"t":"S"},{"DE":17.4760,"RA":295.2622,"AM":4.3900,"t":"S"},{"DE":-53.4494,"RA":319.9664,"AM":4.3900,"t":"S"},{"DE":23.4176,"RA":14.3017,"AM":4.4000,"t":"S"},{"DE":-25.9372,"RA":117.0215,"AM":4.4000,"t":"S"},{"DE":-19.2450,"RA":122.2568,"AM":4.4000,"t":"S"},{"DE":-67.2335,"RA":284.2377,"AM":4.4000,"t":"S"},{"DE":-54.9926,"RA":329.4794,"AM":4.4000,"t":"S"},{"DE":-53.6224,"RA":102.4638,"AM":4.4100,"t":"S"},{"DE":30.2452,"RA":107.7849,"AM":4.4100,"t":"S"},{"DE":-39.5118,"RA":215.7593,"AM":4.4100,"t":"S"},{"DE":26.1106,"RA":262.6846,"AM":4.4100,"t":"S"},{"DE":30.1893,"RA":269.6256,"AM":4.4100,"t":"S"},{"DE":34.8969,"RA":319.4795,"AM":4.4100,"t":"S"},{"DE":75.3875,"RA":346.9743,"AM":4.4100,"t":"S"},{"DE":-9.1825,"RA":349.4759,"AM":4.4100,"t":"S"},{"DE":-32.5320,"RA":349.7060,"AM":4.4100,"t":"S"},{"DE":14.7685,"RA":91.8930,"AM":4.4200,"t":"S"},{"DE":-18.2375,"RA":99.4726,"AM":4.4200,"t":"S"},{"DE":-44.6397,"RA":108.3846,"AM":4.4200,"t":"S"},{"DE":-26.3525,"RA":108.5634,"AM":4.4200,"t":"S"},{"DE":-40.3479,"RA":123.5121,"AM":4.4200,"t":"S"},{"DE":20.1798,"RA":165.5824,"AM":4.4200,"t":"S"},{"DE":-27.9604,"RA":222.5722,"AM":4.4200,"t":"S"},{"DE":7.3531,"RA":236.6109,"AM":4.4200,"t":"S"},{"DE":1.3051,"RA":270.4383,"AM":4.4200,"t":"S"},{"DE":52.2290,"RA":335.8901,"AM":4.4200,"t":"S"},{"DE":23.4041,"RA":351.3449,"AM":4.4200,"t":"S"},{"DE":-12.1016,"RA":56.5356,"AM":4.4300,"t":"S"},{"DE":-7.6529,"RA":63.8181,"AM":4.4300,"t":"S"},{"DE":53.7521,"RA":74.3217,"AM":4.4300,"t":"S"},{"DE":39.1460,"RA":288.4395,"AM":4.4300,"t":"S"},{"DE":-27.7098,"RA":300.6645,"AM":4.4300,"t":"S"},{"DE":32.1902,"RA":305.9651,"AM":4.4300,"t":"S"},{"DE":15.0746,"RA":310.8647,"AM":4.4300,"t":"S"},{"DE":-5.0277,"RA":311.9343,"AM":4.4300,"t":"S"},{"DE":-18.9329,"RA":3.6601,"AM":4.4400,"t":"S"},{"DE":7.5851,"RA":12.1706,"AM":4.4400,"t":"S"},{"DE":-59.3022,"RA":64.1211,"AM":4.4400,"t":"S"},{"DE":-41.8638,"RA":70.1406,"AM":4.4400,"t":"S"},{"DE":59.0110,"RA":94.9058,"AM":4.4400,"t":"S"},{"DE":-22.2961,"RA":113.5133,"AM":4.4400,"t":"S"},{"DE":-39.6185,"RA":122.8396,"AM":4.4400,"t":"S"},{"DE":-36.6593,"RA":124.6389,"AM":4.4400,"t":"S"},{"DE":-50.4572,"RA":218.1544,"AM":4.4400,"t":"S"},{"DE":24.6649,"RA":292.1764,"AM":4.4400,"t":"S"},{"DE":5.4876,"RA":25.3579,"AM":4.4500,"t":"S"},{"DE":-32.4059,"RA":42.2725,"AM":4.4500,"t":"S"},{"DE":-11.8692,"RA":78.0746,"AM":4.4500,"t":"S"},{"DE":14.2088,"RA":92.9850,"AM":4.4500,"t":"S"},{"DE":3.3414,"RA":129.6893,"AM":4.4500,"t":"S"},{"DE":-41.2536,"RA":135.0226,"AM":4.4500,"t":"S"},{"DE":-57.5576,"RA":158.8971,"AM":4.4500,"t":"S"},{"DE":-80.5402,"RA":161.4463,"AM":4.4500,"t":"S"},{"DE":-3.6516,"RA":169.1654,"AM":4.4500,"t":"S"},{"DE":-21.4664,"RA":248.0342,"AM":4.4500,"t":"S"},{"DE":73.3555,"RA":288.8884,"AM":4.4500,"t":"S"},{"DE":7.3789,"RA":293.5223,"AM":4.4500,"t":"S"},{"DE":67.4025,"RA":37.2666,"AM":4.4600,"t":"S"},{"DE":-2.9547,"RA":58.5729,"AM":4.4600,"t":"S"},{"DE":2.8613,"RA":78.3228,"AM":4.4600,"t":"S"},{"DE":51.6046,"RA":137.2179,"AM":4.4600,"t":"S"},{"DE":-22.8258,"RA":167.9145,"AM":4.4600,"t":"S"},{"DE":-50.6613,"RA":182.0218,"AM":4.4600,"t":"S"},{"DE":-47.5548,"RA":246.7960,"AM":4.4600,"t":"S"},{"DE":-32.8755,"RA":343.1314,"AM":4.4600,"t":"S"},{"DE":-18.5726,"RA":41.2757,"AM":4.4700,"t":"S"},{"DE":29.0485,"RA":50.0848,"AM":4.4700,"t":"S"},{"DE":1.7140,"RA":74.6371,"AM":4.4700,"t":"S"},{"DE":-32.5801,"RA":97.0425,"AM":4.4700,"t":"S"},{"DE":7.3330,"RA":98.2259,"AM":4.4700,"t":"S"},{"DE":-49.2449,"RA":119.5602,"AM":4.4700,"t":"S"},{"DE":-72.6027,"RA":136.2868,"AM":4.4700,"t":"S"},{"DE":26.1823,"RA":141.1636,"AM":4.4700,"t":"S"},{"DE":52.0515,"RA":143.7061,"AM":4.4700,"t":"S"},{"DE":-45.1735,"RA":177.7863,"AM":4.4700,"t":"S"},{"DE":29.7451,"RA":218.6700,"AM":4.4700,"t":"S"},{"DE":-4.3465,"RA":224.2958,"AM":4.4700,"t":"S"},{"DE":10.0070,"RA":318.6201,"AM":4.4700,"t":"S"},{"DE":-39.5434,"RA":331.5287,"AM":4.4700,"t":"S"},{"DE":48.2844,"RA":11.1813,"AM":4.4800,"t":"S"},{"DE":-62.1593,"RA":60.2242,"AM":4.4800,"t":"S"},{"DE":15.6183,"RA":66.5864,"AM":4.4800,"t":"S"},{"DE":2.4122,"RA":101.9652,"AM":4.4800,"t":"S"},{"DE":-0.3716,"RA":151.9845,"AM":4.4800,"t":"S"},{"DE":-59.3208,"RA":230.8444,"AM":4.4800,"t":"S"},{"DE":-20.0373,"RA":246.0258,"AM":4.4800,"t":"S"},{"DE":3.8200,"RA":345.9692,"AM":4.4800,"t":"S"},{"DE":-23.7431,"RA":346.6702,"AM":4.4800,"t":"S"},{"DE":70.9070,"RA":30.4897,"AM":4.4900,"t":"S"},{"DE":-29.7665,"RA":68.3773,"AM":4.4900,"t":"S"},{"DE":13.2280,"RA":100.9971,"AM":4.4900,"t":"S"},{"DE":-46.7593,"RA":108.1402,"AM":4.4900,"t":"S"},{"DE":-38.8628,"RA":118.1610,"AM":4.4900,"t":"S"},{"DE":35.2447,"RA":151.8573,"AM":4.4900,"t":"S"},{"DE":16.4183,"RA":220.1815,"AM":4.4900,"t":"S"},{"DE":50.2211,"RA":294.1106,"AM":4.4900,"t":"S"},{"DE":-25.0059,"RA":316.7820,"AM":4.4900,"t":"S"},{"DE":28.7426,"RA":326.0357,"AM":4.4900,"t":"S"},{"DE":1.7800,"RA":355.5117,"AM":4.4900,"t":"S"},{"DE":-14.5449,"RA":355.6806,"AM":4.4900,"t":"S"},{"DE":-65.5771,"RA":359.9789,"AM":4.4900,"t":"S"},{"DE":4.1215,"RA":84.7964,"AM":4.5000,"t":"S"},{"DE":-56.1667,"RA":87.4568,"AM":4.5000,"t":"S"},{"DE":-56.7698,"RA":131.6773,"AM":4.5000,"t":"S"},{"DE":-56.0432,"RA":155.2284,"AM":4.5000,"t":"S"},{"DE":20.2189,"RA":176.9964,"AM":4.5000,"t":"S"},{"DE":17.4569,"RA":206.8157,"AM":4.5000,"t":"S"},{"DE":27.8142,"RA":303.9422,"AM":4.5000,"t":"S"},{"DE":-11.3717,"RA":317.3985,"AM":4.5000,"t":"S"},{"DE":-21.8072,"RA":322.1808,"AM":4.5000,"t":"S"},{"DE":-32.9885,"RA":332.0958,"AM":4.5000,"t":"S"},{"DE":39.7149,"RA":333.4697,"AM":4.5000,"t":"S"},{"DE":44.2763,"RA":340.1285,"AM":4.5000,"t":"S"},{"DE":36.7852,"RA":4.5819,"AM":4.5100,"t":"S"},{"DE":30.0896,"RA":17.9151,"AM":4.5100,"t":"S"},{"DE":39.1811,"RA":87.2935,"AM":4.5100,"t":"S"},{"DE":-35.9513,"RA":142.3113,"AM":4.5100,"t":"S"},{"DE":-61.3281,"RA":144.8376,"AM":4.5100,"t":"S"},{"DE":19.6704,"RA":235.3877,"AM":4.5100,"t":"S"},{"DE":67.8736,"RA":300.7044,"AM":4.5100,"t":"S"},{"DE":-51.9210,"RA":311.0095,"AM":4.5100,"t":"S"},{"DE":-19.4660,"RA":324.2701,"AM":4.5100,"t":"S"},{"DE":-64.9664,"RA":336.8330,"AM":4.5100,"t":"S"},{"DE":57.4994,"RA":358.5960,"AM":4.5100,"t":"S"},{"DE":29.2471,"RA":41.9772,"AM":4.5200,"t":"S"},{"DE":-60.9884,"RA":200.6582,"AM":4.5200,"t":"S"},{"DE":-64.5357,"RA":201.0019,"AM":4.5200,"t":"S"},{"DE":-13.3711,"RA":214.7775,"AM":4.5200,"t":"S"},{"DE":26.9476,"RA":226.1115,"AM":4.5200,"t":"S"},{"DE":-45.9544,"RA":272.8074,"AM":4.5200,"t":"S"},{"DE":-15.9550,"RA":290.4318,"AM":4.5200,"t":"S"},{"DE":57.5797,"RA":311.3382,"AM":4.5200,"t":"S"},{"DE":23.6388,"RA":322.4871,"AM":4.5200,"t":"S"},{"DE":43.1234,"RA":337.6219,"AM":4.5200,"t":"S"},{"DE":-62.9656,"RA":7.8892,"AM":4.5300,"t":"S"},{"DE":41.0789,"RA":12.4535,"AM":4.5300,"t":"S"},{"DE":-3.0743,"RA":90.0140,"AM":4.5300,"t":"S"},{"DE":-34.9685,"RA":114.3421,"AM":4.5300,"t":"S"},{"DE":51.7900,"RA":213.3708,"AM":4.5300,"t":"S"},{"DE":-5.0866,"RA":261.6578,"AM":4.5300,"t":"S"},{"DE":-27.8308,"RA":266.8901,"AM":4.5300,"t":"S"},{"DE":36.4907,"RA":311.8522,"AM":4.5300,"t":"S"},{"DE":49.4062,"RA":348.1374,"AM":4.5300,"t":"S"},{"DE":33.3716,"RA":79.5440,"AM":4.5400,"t":"S"},{"DE":-22.9648,"RA":98.7641,"AM":4.5400,"t":"S"},{"DE":-1.1847,"RA":142.9955,"AM":4.5400,"t":"S"},{"DE":36.3976,"RA":143.5558,"AM":4.5400,"t":"S"},{"DE":69.8303,"RA":143.6205,"AM":4.5400,"t":"S"},{"DE":19.1005,"RA":222.8474,"AM":4.5400,"t":"S"},{"DE":-19.7917,"RA":228.0554,"AM":4.5400,"t":"S"},{"DE":-36.8585,"RA":230.7890,"AM":4.5400,"t":"S"},{"DE":-27.1699,"RA":299.2368,"AM":4.5400,"t":"S"},{"DE":9.4095,"RA":346.7511,"AM":4.5400,"t":"S"},{"DE":12.7606,"RA":352.2887,"AM":4.5400,"t":"S"},{"DE":-17.3360,"RA":0.9350,"AM":4.5500,"t":"S"},{"DE":58.8787,"RA":52.4781,"AM":4.5500,"t":"S"},{"DE":-35.4830,"RA":76.1016,"AM":4.5500,"t":"S"},{"DE":76.9774,"RA":105.0162,"AM":4.5500,"t":"S"},{"DE":12.0066,"RA":112.4491,"AM":4.5500,"t":"S"},{"DE":54.0643,"RA":148.0265,"AM":4.5500,"t":"S"},{"DE":-44.9584,"RA":233.9719,"AM":4.5500,"t":"S"},{"DE":-24.1693,"RA":245.1591,"AM":4.5500,"t":"S"},{"DE":-28.4571,"RA":272.0207,"AM":4.5500,"t":"S"},{"DE":71.3114,"RA":325.4798,"AM":4.5500,"t":"S"},{"DE":46.5366,"RA":335.2564,"AM":4.5500,"t":"S"},{"DE":49.4764,"RA":336.1291,"AM":4.5500,"t":"S"},{"DE":35.0597,"RA":42.8785,"AM":4.5600,"t":"S"},{"DE":-61.4002,"RA":59.6864,"AM":4.5600,"t":"S"},{"DE":27.6123,"RA":88.3319,"AM":4.5600,"t":"S"},{"DE":38.4522,"RA":136.6324,"AM":4.5600,"t":"S"},{"DE":23.0955,"RA":168.8010,"AM":4.5600,"t":"S"},{"DE":-45.2214,"RA":216.5343,"AM":4.5600,"t":"S"},{"DE":-46.5057,"RA":263.9150,"AM":4.5600,"t":"S"},{"DE":27.0970,"RA":313.0320,"AM":4.5600,"t":"S"},{"DE":47.6484,"RA":316.6504,"AM":4.5600,"t":"S"},{"DE":-40.2745,"RA":54.2737,"AM":4.5700,"t":"S"},{"DE":14.0333,"RA":246.3540,"AM":4.5700,"t":"S"},{"DE":-23.4472,"RA":246.3963,"AM":4.5700,"t":"S"},{"DE":72.1488,"RA":265.4847,"AM":4.5700,"t":"S"},{"DE":22.6451,"RA":283.6870,"AM":4.5700,"t":"S"},{"DE":-40.4967,"RA":287.0873,"AM":4.5700,"t":"S"},{"DE":24.0796,"RA":298.3654,"AM":4.5700,"t":"S"},{"DE":-4.8384,"RA":83.8465,"AM":4.5800,"t":"S"},{"DE":-46.5476,"RA":147.9195,"AM":4.5800,"t":"S"},{"DE":-60.5666,"RA":160.8846,"AM":4.5800,"t":"S"},{"DE":-59.9206,"RA":198.0734,"AM":4.5800,"t":"S"},{"DE":64.7233,"RA":207.8581,"AM":4.5800,"t":"S"},{"DE":-27.9264,"RA":243.0759,"AM":4.5800,"t":"S"},{"DE":-8.1188,"RA":264.4613,"AM":4.5800,"t":"S"},{"DE":23.7403,"RA":350.1593,"AM":4.5800,"t":"S"},{"DE":-46.0850,"RA":10.3315,"AM":4.5900,"t":"S"},{"DE":-37.3135,"RA":55.7086,"AM":4.5900,"t":"S"},{"DE":71.3323,"RA":57.5895,"AM":4.5900,"t":"S"},{"DE":3.0957,"RA":81.7093,"AM":4.5900,"t":"S"},{"DE":64.3279,"RA":130.0536,"AM":4.5900,"t":"S"},{"DE":-2.7690,"RA":142.2871,"AM":4.5900,"t":"S"},{"DE":-55.0293,"RA":154.9032,"AM":4.5900,"t":"S"},{"DE":-60.3176,"RA":168.1501,"AM":4.5900,"t":"S"},{"DE":26.0684,"RA":237.3986,"AM":4.5900,"t":"S"},{"DE":-25.3271,"RA":238.4030,"AM":4.5900,"t":"S"},{"DE":39.6127,"RA":281.0949,"AM":4.5900,"t":"S"},{"DE":-24.8836,"RA":294.1768,"AM":4.5900,"t":"S"},{"DE":-28.1303,"RA":357.2314,"AM":4.5900,"t":"S"},{"DE":50.2955,"RA":64.5608,"AM":4.6000,"t":"S"},{"DE":-13.0646,"RA":151.2811,"AM":4.6000,"t":"S"},{"DE":-37.1378,"RA":164.1793,"AM":4.6000,"t":"S"},{"DE":16.9643,"RA":221.3103,"AM":4.6000,"t":"S"},{"DE":-38.7336,"RA":231.3343,"AM":4.6000,"t":"S"},{"DE":42.4515,"RA":238.1685,"AM":4.6000,"t":"S"},{"DE":65.7145,"RA":290.1670,"AM":4.6000,"t":"S"},{"DE":-5.7076,"RA":1.3339,"AM":4.6100,"t":"S"},{"DE":38.6816,"RA":4.2729,"AM":4.6100,"t":"S"},{"DE":3.1875,"RA":28.3890,"AM":4.6100,"t":"S"},{"DE":39.6116,"RA":47.8224,"AM":4.6100,"t":"S"},{"DE":49.2115,"RA":111.6786,"AM":4.6100,"t":"S"},{"DE":-18.3992,"RA":119.9669,"AM":4.6100,"t":"S"},{"DE":-10.0645,"RA":233.5446,"AM":4.6100,"t":"S"},{"DE":35.2509,"RA":308.4758,"AM":4.6100,"t":"S"},{"DE":59.1811,"RA":14.1665,"AM":4.6200,"t":"S"},{"DE":-24.0162,"RA":59.9812,"AM":4.6200,"t":"S"},{"DE":21.5900,"RA":75.7739,"AM":4.6200,"t":"S"},{"DE":-7.3015,"RA":82.9827,"AM":4.6200,"t":"S"},{"DE":-25.8585,"RA":137.0120,"AM":4.6200,"t":"S"},{"DE":7.3360,"RA":166.2543,"AM":4.6200,"t":"S"},{"DE":-62.4241,"RA":166.6352,"AM":4.6200,"t":"S"},{"DE":-54.2641,"RA":173.6903,"AM":4.6200,"t":"S"},{"DE":-56.4888,"RA":191.5947,"AM":4.6200,"t":"S"},{"DE":-59.1467,"RA":193.6633,"AM":4.6200,"t":"S"},{"DE":-8.3717,"RA":246.9508,"AM":4.6200,"t":"S"},{"DE":-3.6903,"RA":270.1209,"AM":4.6200,"t":"S"},{"DE":-42.3125,"RA":278.3757,"AM":4.6200,"t":"S"},{"DE":4.2036,"RA":284.0549,"AM":4.6200,"t":"S"},{"DE":21.3404,"RA":44.8030,"AM":4.6300,"t":"S"},{"DE":-28.4109,"RA":115.8849,"AM":4.6300,"t":"S"},{"DE":-49.6130,"RA":118.2652,"AM":4.6300,"t":"S"},{"DE":-7.2337,"RA":130.9182,"AM":4.6300,"t":"S"},{"DE":-37.4131,"RA":138.9378,"AM":4.6300,"t":"S"},{"DE":-39.9873,"RA":189.9689,"AM":4.6300,"t":"S"},{"DE":54.6816,"RA":205.1845,"AM":4.6300,"t":"S"},{"DE":65.9325,"RA":224.3961,"AM":4.6300,"t":"S"},{"DE":-25.7513,"RA":237.7448,"AM":4.6300,"t":"S"},{"DE":-57.7751,"RA":240.8840,"AM":4.6300,"t":"S"},{"DE":-62.2783,"RA":277.8434,"AM":4.6300,"t":"S"},{"DE":59.3884,"RA":282.8002,"AM":4.6300,"t":"S"},{"DE":25.1414,"RA":359.4397,"AM":4.6300,"t":"S"},{"DE":-24.6122,"RA":58.4279,"AM":4.6400,"t":"S"},{"DE":10.1508,"RA":73.7239,"AM":4.6400,"t":"S"},{"DE":20.1385,"RA":90.9799,"AM":4.6400,"t":"S"},{"DE":-51.4328,"RA":206.6641,"AM":4.6400,"t":"S"},{"DE":36.6358,"RA":234.8445,"AM":4.6400,"t":"S"},{"DE":-44.6612,"RA":235.2976,"AM":4.6400,"t":"S"},{"DE":-10.7830,"RA":252.4584,"AM":4.6400,"t":"S"},{"DE":37.2915,"RA":259.4178,"AM":4.6400,"t":"S"},{"DE":8.7339,"RA":271.8265,"AM":4.6400,"t":"S"},{"DE":0.3386,"RA":291.6295,"AM":4.6400,"t":"S"},{"DE":14.6742,"RA":308.8272,"AM":4.6400,"t":"S"},{"DE":51.5451,"RA":339.3435,"AM":4.6400,"t":"S"},{"DE":50.0521,"RA":346.0455,"AM":4.6400,"t":"S"},{"DE":27.7071,"RA":40.8630,"AM":4.6500,"t":"S"},{"DE":14.8444,"RA":68.4621,"AM":4.6500,"t":"S"},{"DE":15.4041,"RA":76.1423,"AM":4.6500,"t":"S"},{"DE":-63.0896,"RA":88.5249,"AM":4.6500,"t":"S"},{"DE":-36.7340,"RA":109.5767,"AM":4.6500,"t":"S"},{"DE":-30.9623,"RA":112.6775,"AM":4.6500,"t":"S"},{"DE":-28.3693,"RA":113.8454,"AM":4.6500,"t":"S"},{"DE":-57.6388,"RA":156.8520,"AM":4.6500,"t":"S"},{"DE":6.6143,"RA":180.2183,"AM":4.6500,"t":"S"},{"DE":-49.2297,"RA":240.8037,"AM":4.6500,"t":"S"},{"DE":-40.4656,"RA":142.6765,"AM":4.6500,"t":"S"},{"DE":21.0346,"RA":17.8634,"AM":4.6600,"t":"S"},{"DE":-10.6864,"RA":27.3963,"AM":4.6600,"t":"S"},{"DE":9.8958,"RA":100.2444,"AM":4.6600,"t":"S"},{"DE":-20.1365,"RA":103.9060,"AM":4.6600,"t":"S"},{"DE":-27.8812,"RA":109.1458,"AM":4.6600,"t":"S"},{"DE":21.4685,"RA":130.8215,"AM":4.6600,"t":"S"},{"DE":-70.5385,"RA":136.4099,"AM":4.6600,"t":"S"},{"DE":43.1900,"RA":163.4947,"AM":4.6600,"t":"S"},{"DE":-7.9956,"RA":189.8115,"AM":4.6600,"t":"S"},{"DE":-48.8131,"RA":190.6479,"AM":4.6600,"t":"S"},{"DE":-34.4119,"RA":234.9416,"AM":4.6600,"t":"S"},{"DE":-29.5801,"RA":271.2551,"AM":4.6600,"t":"S"},{"DE":-27.0426,"RA":274.5133,"AM":4.6600,"t":"S"},{"DE":-8.9344,"RA":275.9149,"AM":4.6600,"t":"S"},{"DE":27.7536,"RA":300.2752,"AM":4.6600,"t":"S"},{"DE":24.5837,"RA":18.4373,"AM":4.6700,"t":"S"},{"DE":49.5089,"RA":52.3418,"AM":4.6700,"t":"S"},{"DE":40.4837,"RA":63.7221,"AM":4.6700,"t":"S"},{"DE":15.9180,"RA":69.8187,"AM":4.6700,"t":"S"},{"DE":-14.9353,"RA":91.5388,"AM":4.6700,"t":"S"},{"DE":17.6478,"RA":123.0530,"AM":4.6700,"t":"S"},{"DE":63.5136,"RA":137.7291,"AM":4.6700,"t":"S"},{"DE":16.7509,"RA":270.0142,"AM":4.6700,"t":"S"},{"DE":-14.5658,"RA":277.2994,"AM":4.6700,"t":"S"},{"DE":39.6701,"RA":281.0848,"AM":4.6700,"t":"S"},{"DE":69.6612,"RA":293.0872,"AM":4.6700,"t":"S"},{"DE":-32.2578,"RA":315.3228,"AM":4.6700,"t":"S"},{"DE":59.2320,"RA":23.4829,"AM":4.6800,"t":"S"},{"DE":-67.6473,"RA":28.7336,"AM":4.6800,"t":"S"},{"DE":-29.2968,"RA":31.1227,"AM":4.6800,"t":"S"},{"DE":39.6627,"RA":44.6903,"AM":4.6800,"t":"S"},{"DE":-52.7235,"RA":134.0803,"AM":4.6800,"t":"S"},{"DE":4.6493,"RA":144.6137,"AM":4.6800,"t":"S"},{"DE":8.0442,"RA":150.0534,"AM":4.6800,"t":"S"},{"DE":31.9762,"RA":159.6801,"AM":4.6800,"t":"S"},{"DE":-6.2558,"RA":202.9912,"AM":4.6800,"t":"S"},{"DE":49.0160,"RA":203.6137,"AM":4.6800,"t":"S"},{"DE":-78.6957,"RA":245.0868,"AM":4.6800,"t":"S"},{"DE":30.1533,"RA":294.8442,"AM":4.6800,"t":"S"},{"DE":-7.8542,"RA":324.4380,"AM":4.6800,"t":"S"},{"DE":-18.8304,"RA":340.8968,"AM":4.6800,"t":"S"},{"DE":14.7138,"RA":66.6516,"AM":4.6900,"t":"S"},{"DE":40.0991,"RA":79.7849,"AM":4.6900,"t":"S"},{"DE":-25.3648,"RA":114.5752,"AM":4.6900,"t":"S"},{"DE":-47.0777,"RA":117.0841,"AM":4.6900,"t":"S"},{"DE":-1.3926,"RA":120.3056,"AM":4.6900,"t":"S"},{"DE":-59.1830,"RA":159.6875,"AM":4.6900,"t":"S"},{"DE":-60.9813,"RA":191.4083,"AM":4.6900,"t":"S"},{"DE":51.1896,"RA":325.5236,"AM":4.6900,"t":"S"},{"DE":-56.7860,"RA":330.8323,"AM":4.6900,"t":"S"},{"DE":-42.6151,"RA":353.7690,"AM":4.6900,"t":"S"},{"DE":-21.2398,"RA":80.1122,"AM":4.7000,"t":"S"},{"DE":-9.8022,"RA":174.1705,"AM":4.7000,"t":"S"},{"DE":-34.7447,"RA":175.0533,"AM":4.7000,"t":"S"},{"DE":-42.3620,"RA":253.4989,"AM":4.7000,"t":"S"},{"DE":-9.0525,"RA":280.5684,"AM":4.7000,"t":"S"},{"DE":-26.2995,"RA":298.9598,"AM":4.7000,"t":"S"},{"DE":10.1316,"RA":317.5854,"AM":4.7000,"t":"S"},{"DE":84.3462,"RA":343.6018,"AM":4.7000,"t":"S"},{"DE":-20.9145,"RA":353.3193,"AM":4.7000,"t":"S"},{"DE":8.9074,"RA":44.9288,"AM":4.7100,"t":"S"},{"DE":-62.9375,"RA":52.3434,"AM":4.7100,"t":"S"},{"DE":14.2506,"RA":73.1332,"AM":4.7100,"t":"S"},{"DE":-57.4727,"RA":76.3778,"AM":4.7100,"t":"S"},{"DE":-1.0922,"RA":82.4333,"AM":4.7100,"t":"S"},{"DE":32.1920,"RA":83.1820,"AM":4.7100,"t":"S"},{"DE":-25.9654,"RA":140.3733,"AM":4.7100,"t":"S"},{"DE":-28.8339,"RA":140.8011,"AM":4.7100,"t":"S"},{"DE":-18.3507,"RA":176.1907,"AM":4.7100,"t":"S"},{"DE":-48.4633,"RA":196.5696,"AM":4.7100,"t":"S"},{"DE":-63.6867,"RA":209.4121,"AM":4.7100,"t":"S"},{"DE":8.4615,"RA":298.5620,"AM":4.7100,"t":"S"},{"DE":-32.1725,"RA":319.4845,"AM":4.7100,"t":"S"},{"DE":-22.4576,"RA":347.4787,"AM":4.7100,"t":"S"},{"DE":68.1300,"RA":21.4831,"AM":4.7200,"t":"S"},{"DE":-0.3825,"RA":80.4406,"AM":4.7200,"t":"S"},{"DE":37.3056,"RA":87.7601,"AM":4.7200,"t":"S"},{"DE":-54.9686,"RA":92.5746,"AM":4.7200,"t":"S"},{"DE":-12.9270,"RA":122.8179,"AM":4.7200,"t":"S"},{"DE":-22.3438,"RA":141.8267,"AM":4.7200,"t":"S"},{"DE":33.7961,"RA":156.4784,"AM":4.7200,"t":"S"},{"DE":-71.9928,"RA":157.5837,"AM":4.7200,"t":"S"},{"DE":40.4256,"RA":158.3080,"AM":4.7200,"t":"S"},{"DE":-63.1657,"RA":181.0801,"AM":4.7200,"t":"S"},{"DE":17.7929,"RA":185.1793,"AM":4.7200,"t":"S"},{"DE":40.5726,"RA":199.3857,"AM":4.7200,"t":"S"},{"DE":46.0367,"RA":240.6995,"AM":4.7200,"t":"S"},{"DE":-0.4453,"RA":259.1529,"AM":4.7200,"t":"S"},{"DE":-18.8663,"RA":325.6646,"AM":4.7200,"t":"S"},{"DE":50.2786,"RA":36.4059,"AM":4.7300,"t":"S"},{"DE":13.1778,"RA":103.6610,"AM":4.7300,"t":"S"},{"DE":-42.9873,"RA":122.8579,"AM":4.7300,"t":"S"},{"DE":-2.4846,"RA":165.4570,"AM":4.7300,"t":"S"},{"DE":-45.1732,"RA":241.6226,"AM":4.7300,"t":"S"},{"DE":36.4909,"RA":242.2429,"AM":4.7300,"t":"S"},{"DE":-8.9833,"RA":313.1635,"AM":4.7300,"t":"S"},{"DE":54.5223,"RA":7.9431,"AM":4.7400,"t":"S"},{"DE":27.2641,"RA":19.8666,"AM":4.7400,"t":"S"},{"DE":-15.2447,"RA":38.0218,"AM":4.7400,"t":"S"},{"DE":-42.8917,"RA":39.9499,"AM":4.7400,"t":"S"},{"DE":65.6523,"RA":49.9969,"AM":4.7400,"t":"S"},{"DE":-5.0751,"RA":52.6544,"AM":4.7400,"t":"S"},{"DE":-61.3024,"RA":122.2532,"AM":4.7400,"t":"S"},{"DE":-47.3171,"RA":130.3047,"AM":4.7400,"t":"S"},{"DE":67.6296,"RA":135.6363,"AM":4.7400,"t":"S"},{"DE":-18.3112,"RA":199.6014,"AM":4.7400,"t":"S"},{"DE":-53.4389,"RA":212.4786,"AM":4.7400,"t":"S"},{"DE":20.9779,"RA":237.8163,"AM":4.7400,"t":"S"},{"DE":-23.8161,"RA":269.9481,"AM":4.7400,"t":"S"},{"DE":-42.0951,"RA":285.7786,"AM":4.7400,"t":"S"},{"DE":34.4530,"RA":292.9430,"AM":4.7400,"t":"S"},{"DE":47.5210,"RA":314.9565,"AM":4.7400,"t":"S"},{"DE":-2.1554,"RA":330.8285,"AM":4.7400,"t":"S"},{"DE":-45.4924,"RA":354.4624,"AM":4.7400,"t":"S"},{"DE":-48.2719,"RA":108.6589,"AM":4.7500,"t":"S"},{"DE":-66.8149,"RA":177.0604,"AM":4.7500,"t":"S"},{"DE":-31.9276,"RA":208.3023,"AM":4.7500,"t":"S"},{"DE":51.3672,"RA":214.0416,"AM":4.7500,"t":"S"},{"DE":-19.6788,"RA":235.4867,"AM":4.7500,"t":"S"},{"DE":-34.7104,"RA":235.6709,"AM":4.7500,"t":"S"},{"DE":-60.5817,"RA":308.8950,"AM":4.7500,"t":"S"},{"DE":68.1114,"RA":349.6560,"AM":4.7500,"t":"S"},{"DE":-48.8035,"RA":7.8539,"AM":4.7600,"t":"S"},{"DE":-75.0669,"RA":42.6188,"AM":4.7600,"t":"S"},{"DE":-21.0040,"RA":42.7597,"AM":4.7600,"t":"S"},{"DE":1.8551,"RA":88.1102,"AM":4.7600,"t":"S"},{"DE":69.3198,"RA":94.7116,"AM":4.7600,"t":"S"},{"DE":-30.3346,"RA":119.4171,"AM":4.7600,"t":"S"},{"DE":-23.5915,"RA":145.3209,"AM":4.7600,"t":"S"},{"DE":-64.4664,"RA":160.5589,"AM":4.7600,"t":"S"},{"DE":38.1856,"RA":169.7830,"AM":4.7600,"t":"S"},{"DE":51.5623,"RA":186.0062,"AM":4.7600,"t":"S"},{"DE":17.4094,"RA":194.7310,"AM":4.7600,"t":"S"},{"DE":-15.9736,"RA":201.8632,"AM":4.7600,"t":"S"},{"DE":34.4442,"RA":207.9478,"AM":4.7600,"t":"S"},{"DE":-58.4591,"RA":215.6546,"AM":4.7600,"t":"S"},{"DE":-67.7707,"RA":260.4980,"AM":4.7600,"t":"S"},{"DE":-49.4156,"RA":265.0991,"AM":4.7600,"t":"S"},{"DE":21.3904,"RA":289.0543,"AM":4.7600,"t":"S"},{"DE":62.0819,"RA":324.4801,"AM":4.7600,"t":"S"},{"DE":25.4683,"RA":346.7781,"AM":4.7600,"t":"S"},{"DE":-10.6096,"RA":11.0475,"AM":4.7700,"t":"S"},{"DE":56.7057,"RA":46.3851,"AM":4.7700,"t":"S"},{"DE":-7.2128,"RA":84.7212,"AM":4.7700,"t":"S"},{"DE":8.0373,"RA":101.8326,"AM":4.7700,"t":"S"},{"DE":-11.9749,"RA":139.9433,"AM":4.7700,"t":"S"},{"DE":-3.0035,"RA":172.5787,"AM":4.7700,"t":"S"},{"DE":-9.5390,"RA":193.5882,"AM":4.7700,"t":"S"},{"DE":68.7580,"RA":264.2379,"AM":4.7700,"t":"S"},{"DE":-8.1803,"RA":270.7705,"AM":4.7700,"t":"S"},{"DE":57.0456,"RA":278.1438,"AM":4.7700,"t":"S"},{"DE":-37.9407,"RA":300.8894,"AM":4.7700,"t":"S"},{"DE":38.0329,"RA":304.4467,"AM":4.7700,"t":"S"},{"DE":-12.7591,"RA":305.1659,"AM":4.7700,"t":"S"},{"DE":-17.8137,"RA":307.2151,"AM":4.7700,"t":"S"},{"DE":83.1538,"RA":341.8707,"AM":4.7700,"t":"S"},{"DE":-77.0657,"RA":0.3992,"AM":4.7800,"t":"S"},{"DE":-1.1443,"RA":13.2521,"AM":4.7800,"t":"S"},{"DE":37.8591,"RA":32.1218,"AM":4.7800,"t":"S"},{"DE":63.3450,"RA":56.5097,"AM":4.7800,"t":"S"},{"DE":16.1940,"RA":67.6401,"AM":4.7800,"t":"S"},{"DE":-12.5374,"RA":74.9822,"AM":4.7800,"t":"S"},{"DE":-6.0020,"RA":83.7612,"AM":4.7800,"t":"S"},{"DE":51.5067,"RA":122.1144,"AM":4.7800,"t":"S"},{"DE":-35.8995,"RA":123.3730,"AM":4.7800,"t":"S"},{"DE":-27.7695,"RA":146.0504,"AM":4.7800,"t":"S"},{"DE":19.4709,"RA":154.9341,"AM":4.7800,"t":"S"},{"DE":25.8462,"RA":185.6263,"AM":4.7800,"t":"S"},{"DE":5.4699,"RA":199.4012,"AM":4.7800,"t":"S"},{"DE":-45.1871,"RA":215.1774,"AM":4.7800,"t":"S"},{"DE":-27.7540,"RA":215.7741,"AM":4.7800,"t":"S"},{"DE":-23.9626,"RA":262.8540,"AM":4.7800,"t":"S"},{"DE":-40.0904,"RA":267.5463,"AM":4.7800,"t":"S"},{"DE":-64.8713,"RA":281.3620,"AM":4.7800,"t":"S"},{"DE":28.3305,"RA":335.3306,"AM":4.7800,"t":"S"},{"DE":4.6957,"RA":336.9647,"AM":4.7800,"t":"S"},{"DE":20.2067,"RA":3.6507,"AM":4.7900,"t":"S"},{"DE":23.5961,"RA":29.4822,"AM":4.7900,"t":"S"},{"DE":36.7032,"RA":73.1583,"AM":4.7900,"t":"S"},{"DE":-48.4904,"RA":125.6321,"AM":4.7900,"t":"S"},{"DE":-62.4046,"RA":140.2368,"AM":4.7900,"t":"S"},{"DE":-67.8946,"RA":198.8124,"AM":4.7900,"t":"S"},{"DE":35.6574,"RA":237.8081,"AM":4.7900,"t":"S"},{"DE":-25.1152,"RA":247.5520,"AM":4.7900,"t":"S"},{"DE":-31.7032,"RA":267.2937,"AM":4.7900,"t":"S"},{"DE":4.3686,"RA":270.0658,"AM":4.7900,"t":"S"},{"DE":25.5920,"RA":303.8162,"AM":4.7900,"t":"S"},{"DE":72.3412,"RA":332.4516,"AM":4.7900,"t":"S"},{"DE":-41.3467,"RA":333.9038,"AM":4.7900,"t":"S"},{"DE":50.5125,"RA":10.5162,"AM":4.8000,"t":"S"},{"DE":61.1240,"RA":13.2677,"AM":4.8000,"t":"S"},{"DE":-8.8197,"RA":48.9584,"AM":4.8000,"t":"S"},{"DE":46.4989,"RA":65.3882,"AM":4.8000,"t":"S"},{"DE":17.4441,"RA":66.0240,"AM":4.8000,"t":"S"},{"DE":-7.1740,"RA":75.3598,"AM":4.8000,"t":"S"},{"DE":42.4889,"RA":99.8326,"AM":4.8000,"t":"S"},{"DE":67.1340,"RA":137.5981,"AM":4.8000,"t":"S"},{"DE":54.0219,"RA":139.0471,"AM":4.8000,"t":"S"},{"DE":-9.5557,"RA":140.1209,"AM":4.8000,"t":"S"},{"DE":-63.9611,"RA":161.0289,"AM":4.8000,"t":"S"},{"DE":22.6293,"RA":188.7129,"AM":4.8000,"t":"S"},{"DE":27.6247,"RA":196.7947,"AM":4.8000,"t":"S"},{"DE":77.5475,"RA":212.2125,"AM":4.8000,"t":"S"},{"DE":35.5095,"RA":214.4993,"AM":4.8000,"t":"S"},{"DE":26.5279,"RA":220.8557,"AM":4.8000,"t":"S"},{"DE":25.0081,"RA":225.5271,"AM":4.8000,"t":"S"},{"DE":-28.6140,"RA":244.5746,"AM":4.8000,"t":"S"},{"DE":33.1001,"RA":259.3315,"AM":4.8000,"t":"S"},{"DE":46.8157,"RA":303.3252,"AM":4.8000,"t":"S"},{"DE":44.3873,"RA":313.3115,"AM":4.8000,"t":"S"},{"DE":-40.8095,"RA":320.1901,"AM":4.8000,"t":"S"},{"DE":1.3774,"RA":336.3193,"AM":4.8000,"t":"S"},{"DE":29.3076,"RA":340.4392,"AM":4.8000,"t":"S"},{"DE":31.5288,"RA":169.5468,"AM":4.8000,"t":"S"},{"DE":15.5972,"RA":77.4248,"AM":4.8100,"t":"S"},{"DE":-67.1853,"RA":78.4393,"AM":4.8100,"t":"S"},{"DE":-34.8952,"RA":79.3712,"AM":4.8100,"t":"S"},{"DE":25.9539,"RA":89.4986,"AM":4.8100,"t":"S"},{"DE":-63.5675,"RA":120.0832,"AM":4.8100,"t":"S"},{"DE":39.6215,"RA":143.7660,"AM":4.8100,"t":"S"},{"DE":-10.8593,"RA":171.1525,"AM":4.8100,"t":"S"},{"DE":-2.2280,"RA":217.0506,"AM":4.8100,"t":"S"},{"DE":-20.5417,"RA":276.3377,"AM":4.8100,"t":"S"},{"DE":21.2012,"RA":309.6306,"AM":4.8100,"t":"S"},{"DE":46.1141,"RA":312.2346,"AM":4.8100,"t":"S"},{"DE":-47.3853,"RA":29.2919,"AM":4.8200,"t":"S"},{"DE":38.4845,"RA":78.3572,"AM":4.8200,"t":"S"},{"DE":-14.1458,"RA":99.8197,"AM":4.8200,"t":"S"},{"DE":-20.2243,"RA":103.3871,"AM":4.8200,"t":"S"},{"DE":-14.5239,"RA":113.4498,"AM":4.8200,"t":"S"},{"DE":-41.6500,"RA":155.5816,"AM":4.8200,"t":"S"},{"DE":55.9805,"RA":157.6569,"AM":4.8200,"t":"S"},{"DE":-51.4506,"RA":186.6324,"AM":4.8200,"t":"S"},{"DE":36.2949,"RA":204.3652,"AM":4.8200,"t":"S"},{"DE":25.0917,"RA":212.5997,"AM":4.8200,"t":"S"},{"DE":22.8045,"RA":240.5737,"AM":4.8200,"t":"S"},{"DE":1.0290,"RA":245.5181,"AM":4.8200,"t":"S"},{"DE":45.9833,"RA":252.3092,"AM":4.8200,"t":"S"},{"DE":-4.2226,"RA":255.2650,"AM":4.8200,"t":"S"},{"DE":65.5635,"RA":276.4960,"AM":4.8200,"t":"S"},{"DE":71.2972,"RA":283.5992,"AM":4.8200,"t":"S"},{"DE":-19.8550,"RA":316.1013,"AM":4.8200,"t":"S"},{"DE":12.2052,"RA":335.3795,"AM":4.8200,"t":"S"},{"DE":-10.6779,"RA":337.6617,"AM":4.8200,"t":"S"},{"DE":49.0153,"RA":349.4360,"AM":4.8200,"t":"S"},{"DE":-17.8165,"RA":355.4409,"AM":4.8200,"t":"S"},{"DE":58.9727,"RA":13.7507,"AM":4.8300,"t":"S"},{"DE":45.4067,"RA":21.9137,"AM":4.8300,"t":"S"},{"DE":-11.8722,"RA":39.8910,"AM":4.8300,"t":"S"},{"DE":-67.6166,"RA":41.3857,"AM":4.8300,"t":"S"},{"DE":-39.6557,"RA":107.2128,"AM":4.8300,"t":"S"},{"DE":-23.3156,"RA":109.1535,"AM":4.8300,"t":"S"},{"DE":-33.0544,"RA":125.3460,"AM":4.8300,"t":"S"},{"DE":-53.1140,"RA":130.6058,"AM":4.8300,"t":"S"},{"DE":-49.5273,"RA":195.8888,"AM":4.8300,"t":"S"},{"DE":47.6541,"RA":225.9476,"AM":4.8300,"t":"S"},{"DE":-44.5004,"RA":228.2066,"AM":4.8300,"t":"S"},{"DE":41.8817,"RA":247.1606,"AM":4.8300,"t":"S"},{"DE":-34.1229,"RA":256.2056,"AM":4.8300,"t":"S"},{"DE":26.6621,"RA":281.5187,"AM":4.8300,"t":"S"},{"DE":-5.8463,"RA":284.2653,"AM":4.8300,"t":"S"},{"DE":-37.1074,"RA":284.6808,"AM":4.8300,"t":"S"},{"DE":6.1438,"RA":22.5463,"AM":4.8400,"t":"S"},{"DE":44.2317,"RA":33.3055,"AM":4.8400,"t":"S"},{"DE":34.2242,"RA":34.2629,"AM":4.8400,"t":"S"},{"DE":3.3702,"RA":49.8404,"AM":4.8400,"t":"S"},{"DE":9.2638,"RA":63.4849,"AM":4.8400,"t":"S"},{"DE":16.5341,"RA":85.3238,"AM":4.8400,"t":"S"},{"DE":-38.3080,"RA":114.8639,"AM":4.8400,"t":"S"},{"DE":-58.0092,"RA":128.8320,"AM":4.8400,"t":"S"},{"DE":3.6175,"RA":165.1402,"AM":4.8400,"t":"S"},{"DE":8.2581,"RA":176.3210,"AM":4.8400,"t":"S"},{"DE":16.3069,"RA":214.9385,"AM":4.8400,"t":"S"},{"DE":11.4880,"RA":248.1512,"AM":4.8400,"t":"S"},{"DE":64.5890,"RA":250.2297,"AM":4.8400,"t":"S"},{"DE":56.7819,"RA":251.3242,"AM":4.8400,"t":"S"},{"DE":-26.1958,"RA":299.7383,"AM":4.8400,"t":"S"},{"DE":-41.4143,"RA":340.8749,"AM":4.8400,"t":"S"},{"DE":-53.5001,"RA":341.4078,"AM":4.8400,"t":"S"},{"DE":59.4198,"RA":346.6534,"AM":4.8400,"t":"S"},{"DE":-11.3746,"RA":241.0916,"AM":4.8400,"t":"S"},{"DE":74.3937,"RA":47.9844,"AM":4.8500,"t":"S"},{"DE":34.2227,"RA":49.6826,"AM":4.8500,"t":"S"},{"DE":-23.0243,"RA":112.4642,"AM":4.8500,"t":"S"},{"DE":-51.8113,"RA":152.2344,"AM":4.8500,"t":"S"},{"DE":-37.8030,"RA":198.0135,"AM":4.8500,"t":"S"},{"DE":-63.6105,"RA":229.4120,"AM":4.8500,"t":"S"},{"DE":-44.3422,"RA":269.1976,"AM":4.8500,"t":"S"},{"DE":3.3772,"RA":275.2169,"AM":4.8500,"t":"S"},{"DE":-52.9386,"RA":284.6157,"AM":4.8500,"t":"S"},{"DE":-33.0072,"RA":6.9821,"AM":4.8600,"t":"S"},{"DE":-22.5111,"RA":49.5921,"AM":4.8600,"t":"S"},{"DE":59.4417,"RA":101.5589,"AM":4.8600,"t":"S"},{"DE":-29.5611,"RA":129.9270,"AM":4.8600,"t":"S"},{"DE":75.7129,"RA":158.7732,"AM":4.8600,"t":"S"},{"DE":-66.7834,"RA":199.3043,"AM":4.8600,"t":"S"},{"DE":8.4466,"RA":215.8446,"AM":4.8600,"t":"S"},{"DE":8.1618,"RA":220.4115,"AM":4.8600,"t":"S"},{"DE":30.8920,"RA":245.5243,"AM":4.8600,"t":"S"},{"DE":-44.0453,"RA":248.5209,"AM":4.8600,"t":"S"},{"DE":48.9283,"RA":249.6869,"AM":4.8600,"t":"S"},{"DE":55.1730,"RA":263.0665,"AM":4.8600,"t":"S"},{"DE":-21.6832,"RA":265.8575,"AM":4.8600,"t":"S"},{"DE":-35.6420,"RA":281.0807,"AM":4.8600,"t":"S"},{"DE":-22.7448,"RA":283.5424,"AM":4.8600,"t":"S"},{"DE":-25.2567,"RA":288.8851,"AM":4.8600,"t":"S"},{"DE":-61.5299,"RA":309.3970,"AM":4.8600,"t":"S"},{"DE":5.0585,"RA":331.4198,"AM":4.8600,"t":"S"},{"DE":45.5288,"RA":20.5851,"AM":4.8700,"t":"S"},{"DE":5.5932,"RA":38.9686,"AM":4.8700,"t":"S"},{"DE":21.0444,"RA":48.7254,"AM":4.8700,"t":"S"},{"DE":-10.2563,"RA":63.5987,"AM":4.8700,"t":"S"},{"DE":-45.1827,"RA":108.3057,"AM":4.8700,"t":"S"},{"DE":-15.9434,"RA":130.4306,"AM":4.8700,"t":"S"},{"DE":-27.6819,"RA":133.8815,"AM":4.8700,"t":"S"},{"DE":-25.9323,"RA":148.5514,"AM":4.8700,"t":"S"},{"DE":-27.4126,"RA":159.3072,"AM":4.8700,"t":"S"},{"DE":-64.3835,"RA":161.7135,"AM":4.8700,"t":"S"},{"DE":-19.7611,"RA":296.5906,"AM":4.8700,"t":"S"},{"DE":38.5341,"RA":323.6939,"AM":4.8700,"t":"S"},{"DE":-12.2905,"RA":36.4875,"AM":4.8800,"t":"S"},{"DE":21.9370,"RA":81.9087,"AM":4.8800,"t":"S"},{"DE":24.5675,"RA":87.2540,"AM":4.8800,"t":"S"},{"DE":-33.8014,"RA":88.2787,"AM":4.8800,"t":"S"},{"DE":-24.5587,"RA":109.6682,"AM":4.8800,"t":"S"},{"DE":-78.2218,"RA":179.9069,"AM":4.8800,"t":"S"},{"DE":10.2356,"RA":190.4711,"AM":4.8800,"t":"S"},{"DE":30.7850,"RA":195.0686,"AM":4.8800,"t":"S"},{"DE":65.1348,"RA":254.0062,"AM":4.8800,"t":"S"},{"DE":-41.7163,"RA":269.4492,"AM":4.8800,"t":"S"},{"DE":-8.2752,"RA":280.8802,"AM":4.8800,"t":"S"},{"DE":-18.9529,"RA":289.4087,"AM":4.8800,"t":"S"},{"DE":-48.0992,"RA":293.8041,"AM":4.8800,"t":"S"},{"DE":58.6520,"RA":356.7643,"AM":4.8800,"t":"S"},{"DE":-3.5560,"RA":359.6682,"AM":4.8800,"t":"S"},{"DE":55.7549,"RA":359.7522,"AM":4.8800,"t":"S"},{"DE":-15.4680,"RA":2.8161,"AM":4.8900,"t":"S"},{"DE":37.4883,"RA":72.4777,"AM":4.8900,"t":"S"},{"DE":1.8464,"RA":81.1868,"AM":4.8900,"t":"S"},{"DE":12.6513,"RA":87.3872,"AM":4.8900,"t":"S"},{"DE":34.5843,"RA":114.7914,"AM":4.8900,"t":"S"},{"DE":18.5100,"RA":116.5310,"AM":4.8900,"t":"S"},{"DE":-53.7155,"RA":157.8416,"AM":4.8900,"t":"S"},{"DE":-13.3845,"RA":159.3886,"AM":4.8900,"t":"S"},{"DE":-40.5004,"RA":176.6306,"AM":4.8900,"t":"S"},{"DE":-65.2059,"RA":177.9636,"AM":4.8900,"t":"S"},{"DE":21.2449,"RA":193.3239,"AM":4.8900,"t":"S"},{"DE":-81.0078,"RA":214.5582,"AM":4.8900,"t":"S"},{"DE":12.7408,"RA":256.3445,"AM":4.8900,"t":"S"},{"DE":55.1842,"RA":263.0438,"AM":4.8900,"t":"S"},{"DE":37.3544,"RA":296.0691,"AM":4.8900,"t":"S"},{"DE":-33.7797,"RA":312.4920,"AM":4.8900,"t":"S"},{"DE":39.0503,"RA":339.8153,"AM":4.8900,"t":"S"},{"DE":58.5489,"RA":352.5080,"AM":4.8900,"t":"S"},{"DE":50.9682,"RA":12.2084,"AM":4.9000,"t":"S"},{"DE":-14.5988,"RA":21.4051,"AM":4.9000,"t":"S"},{"DE":1.4746,"RA":85.6193,"AM":4.9000,"t":"S"},{"DE":45.0941,"RA":104.4046,"AM":4.9000,"t":"S"},{"DE":-33.9993,"RA":192.6715,"AM":4.9000,"t":"S"},{"DE":-59.1032,"RA":198.5637,"AM":4.9000,"t":"S"},{"DE":-38.6025,"RA":240.8508,"AM":4.9000,"t":"S"},{"DE":-19.8019,"RA":241.3607,"AM":4.9000,"t":"S"},{"DE":-70.0844,"RA":247.1163,"AM":4.9000,"t":"S"},{"DE":22.6100,"RA":297.7671,"AM":4.9000,"t":"S"},{"DE":-46.2268,"RA":312.3706,"AM":4.9000,"t":"S"},{"DE":40.1939,"RA":40.5622,"AM":4.9100,"t":"S"},{"DE":-0.0440,"RA":67.9694,"AM":4.9100,"t":"S"},{"DE":-20.0519,"RA":75.3566,"AM":4.9100,"t":"S"},{"DE":18.6451,"RA":76.8625,"AM":4.9100,"t":"S"},{"DE":-2.9445,"RA":94.9983,"AM":4.9100,"t":"S"},{"DE":-4.2371,"RA":107.5570,"AM":4.9100,"t":"S"},{"DE":39.3205,"RA":107.9138,"AM":4.9100,"t":"S"},{"DE":-16.8766,"RA":159.6456,"AM":4.9100,"t":"S"},{"DE":-59.6858,"RA":190.4858,"AM":4.9100,"t":"S"},{"DE":37.1824,"RA":203.6991,"AM":4.9100,"t":"S"},{"DE":-8.5189,"RA":225.2431,"AM":4.9100,"t":"S"},{"DE":-31.5191,"RA":228.6555,"AM":4.9100,"t":"S"},{"DE":-17.7422,"RA":250.3933,"AM":4.9100,"t":"S"},{"DE":54.4700,"RA":256.3339,"AM":4.9100,"t":"S"},{"DE":52.4389,"RA":298.9075,"AM":4.9100,"t":"S"},{"DE":-2.8855,"RA":307.4125,"AM":4.9100,"t":"S"},{"DE":-2.5500,"RA":309.1818,"AM":4.9100,"t":"S"},{"DE":-61.9821,"RA":338.2502,"AM":4.9100,"t":"S"},{"DE":8.8162,"RA":343.8070,"AM":4.9100,"t":"S"},{"DE":-22.5268,"RA":29.1675,"AM":4.9200,"t":"S"},{"DE":-10.5979,"RA":90.4601,"AM":4.9200,"t":"S"},{"DE":-16.4844,"RA":91.2464,"AM":4.9200,"t":"S"},{"DE":49.2879,"RA":96.2246,"AM":4.9200,"t":"S"},{"DE":-49.5839,"RA":105.9734,"AM":4.9200,"t":"S"},{"DE":82.4115,"RA":112.7687,"AM":4.9200,"t":"S"},{"DE":-38.5699,"RA":138.9030,"AM":4.9200,"t":"S"},{"DE":-27.2936,"RA":166.3330,"AM":4.9200,"t":"S"},{"DE":27.2682,"RA":186.6003,"AM":4.9200,"t":"S"},{"DE":3.6590,"RA":203.5331,"AM":4.9200,"t":"S"},{"DE":21.2641,"RA":207.4285,"AM":4.9200,"t":"S"},{"DE":-35.1918,"RA":221.2467,"AM":4.9200,"t":"S"},{"DE":-10.3223,"RA":231.0495,"AM":4.9200,"t":"S"},{"DE":-43.4252,"RA":271.7079,"AM":4.9200,"t":"S"},{"DE":21.9613,"RA":275.0746,"AM":4.9200,"t":"S"},{"DE":-45.9148,"RA":277.9393,"AM":4.9200,"t":"S"},{"DE":50.7082,"RA":283.3064,"AM":4.9200,"t":"S"},{"DE":25.2706,"RA":311.2188,"AM":4.9200,"t":"S"},{"DE":-41.9936,"RA":62.7106,"AM":4.9300,"t":"S"},{"DE":20.5786,"RA":64.3153,"AM":4.9300,"t":"S"},{"DE":34.5667,"RA":65.1027,"AM":4.9300,"t":"S"},{"DE":37.8902,"RA":74.8142,"AM":4.9300,"t":"S"},{"DE":-52.5338,"RA":113.9155,"AM":4.9300,"t":"S"},{"DE":58.7104,"RA":115.7518,"AM":4.9300,"t":"S"},{"DE":-3.6796,"RA":119.9340,"AM":4.9300,"t":"S"},{"DE":-59.2293,"RA":134.2434,"AM":4.9300,"t":"S"},{"DE":-23.9156,"RA":145.5602,"AM":4.9300,"t":"S"},{"DE":-29.2610,"RA":173.0684,"AM":4.9300,"t":"S"},{"DE":-62.0901,"RA":175.2235,"AM":4.9300,"t":"S"},{"DE":23.9454,"RA":184.0856,"AM":4.9300,"t":"S"},{"DE":27.5407,"RA":192.9247,"AM":4.9300,"t":"S"},{"DE":56.3663,"RA":195.1819,"AM":4.9300,"t":"S"},{"DE":-16.3020,"RA":212.7104,"AM":4.9300,"t":"S"},{"DE":-2.2992,"RA":222.7545,"AM":4.9300,"t":"S"},{"DE":24.8692,"RA":226.8252,"AM":4.9300,"t":"S"},{"DE":-10.0643,"RA":243.0000,"AM":4.9300,"t":"S"},{"DE":-7.0275,"RA":294.2227,"AM":4.9300,"t":"S"},{"DE":-52.8808,"RA":301.8465,"AM":4.9300,"t":"S"},{"DE":36.8396,"RA":302.3567,"AM":4.9300,"t":"S"},{"DE":36.8063,"RA":303.6334,"AM":4.9300,"t":"S"},{"DE":34.3741,"RA":311.7948,"AM":4.9300,"t":"S"},{"DE":-7.7265,"RA":349.2123,"AM":4.9300,"t":"S"},{"DE":29.3615,"RA":355.9978,"AM":4.9300,"t":"S"},{"DE":30.3031,"RA":33.0929,"AM":4.9400,"t":"S"},{"DE":35.1831,"RA":44.7653,"AM":4.9400,"t":"S"},{"DE":-48.7211,"RA":104.0666,"AM":4.9400,"t":"S"},{"DE":-19.0166,"RA":110.5564,"AM":4.9400,"t":"S"},{"DE":27.7943,"RA":120.8795,"AM":4.9400,"t":"S"},{"DE":-45.3079,"RA":132.4485,"AM":4.9400,"t":"S"},{"DE":-19.0094,"RA":148.7175,"AM":4.9400,"t":"S"},{"DE":65.5664,"RA":156.0327,"AM":4.9400,"t":"S"},{"DE":-73.2215,"RA":157.7586,"AM":4.9400,"t":"S"},{"DE":-23.1181,"RA":197.2636,"AM":4.9400,"t":"S"},{"DE":40.1529,"RA":198.4290,"AM":4.9400,"t":"S"},{"DE":68.7681,"RA":246.9960,"AM":4.9400,"t":"S"},{"DE":32.1455,"RA":285.0034,"AM":4.9400,"t":"S"},{"DE":15.1976,"RA":303.5692,"AM":4.9400,"t":"S"},{"DE":48.9516,"RA":307.5147,"AM":4.9400,"t":"S"},{"DE":-32.5484,"RA":332.5364,"AM":4.9400,"t":"S"},{"DE":47.0245,"RA":10.8670,"AM":4.9500,"t":"S"},{"DE":58.2316,"RA":20.0205,"AM":4.9500,"t":"S"},{"DE":63.0723,"RA":59.3560,"AM":4.9500,"t":"S"},{"DE":-1.1288,"RA":85.2113,"AM":4.9500,"t":"S"},{"DE":16.1304,"RA":93.0137,"AM":4.9500,"t":"S"},{"DE":2.8563,"RA":171.9843,"AM":4.9500,"t":"S"},{"DE":70.0218,"RA":188.6835,"AM":4.9500,"t":"S"},{"DE":-14.2794,"RA":239.5474,"AM":4.9500,"t":"S"},{"DE":-54.6305,"RA":243.3697,"AM":4.9500,"t":"S"},{"DE":75.7553,"RA":244.3769,"AM":4.9500,"t":"S"},{"DE":38.4867,"RA":298.9657,"AM":4.9500,"t":"S"},{"DE":-59.3759,"RA":300.4364,"AM":4.9500,"t":"S"},{"DE":43.3124,"RA":343.0084,"AM":4.9500,"t":"S"},{"DE":1.2556,"RA":351.7331,"AM":4.9500,"t":"S"},{"DE":3.4868,"RA":356.5980,"AM":4.9500,"t":"S"},{"DE":40.5770,"RA":25.1451,"AM":4.9600,"t":"S"},{"DE":42.6134,"RA":25.4457,"AM":4.9600,"t":"S"},{"DE":-28.2323,"RA":38.4613,"AM":4.9600,"t":"S"},{"DE":43.3297,"RA":50.3607,"AM":4.9600,"t":"S"},{"DE":16.3597,"RA":67.1099,"AM":4.9600,"t":"S"},{"DE":22.0965,"RA":79.8192,"AM":4.9600,"t":"S"},{"DE":55.7069,"RA":88.7116,"AM":4.9600,"t":"S"},{"DE":-18.1342,"RA":207.4679,"AM":4.9600,"t":"S"},{"DE":54.7498,"RA":239.4479,"AM":4.9600,"t":"S"},{"DE":-25.8652,"RA":240.8359,"AM":4.9600,"t":"S"},{"DE":22.2189,"RA":271.5079,"AM":4.9600,"t":"S"},{"DE":-23.7012,"RA":272.9305,"AM":4.9600,"t":"S"},{"DE":31.4053,"RA":272.9757,"AM":4.9600,"t":"S"},{"DE":62.2828,"RA":351.2094,"AM":4.9600,"t":"S"},{"DE":-45.5317,"RA":18.7956,"AM":4.9700,"t":"S"},{"DE":68.6852,"RA":29.0001,"AM":4.9700,"t":"S"},{"DE":33.9650,"RA":55.5944,"AM":4.9700,"t":"S"},{"DE":-61.0788,"RA":60.3255,"AM":4.9700,"t":"S"},{"DE":27.3508,"RA":65.0884,"AM":4.9700,"t":"S"},{"DE":-37.1207,"RA":88.8746,"AM":4.9700,"t":"S"},{"DE":26.7658,"RA":118.3742,"AM":4.9700,"t":"S"},{"DE":-66.9015,"RA":155.7424,"AM":4.9700,"t":"S"},{"DE":3.3126,"RA":185.0874,"AM":4.9700,"t":"S"},{"DE":13.7788,"RA":202.1076,"AM":4.9700,"t":"S"},{"DE":-29.4916,"RA":217.0435,"AM":4.9700,"t":"S"},{"DE":-23.8181,"RA":235.0704,"AM":4.9700,"t":"S"},{"DE":-50.0681,"RA":244.2539,"AM":4.9700,"t":"S"},{"DE":14.0919,"RA":255.7828,"AM":4.9700,"t":"S"},{"DE":31.3253,"RA":353.4883,"AM":4.9700,"t":"S"},{"DE":-14.2222,"RA":354.9461,"AM":4.9700,"t":"S"},{"DE":46.4203,"RA":356.5085,"AM":4.9700,"t":"S"},{"DE":-3.6902,"RA":25.6813,"AM":4.9800,"t":"S"},{"DE":25.9399,"RA":32.3555,"AM":4.9800,"t":"S"},{"DE":-64.0713,"RA":44.6991,"AM":4.9800,"t":"S"},{"DE":51.5977,"RA":76.6693,"AM":4.9800,"t":"S"},{"DE":-5.3873,"RA":83.8159,"AM":4.9800,"t":"S"},{"DE":-5.4161,"RA":83.8454,"AM":4.9800,"t":"S"},{"DE":-15.2639,"RA":115.0967,"AM":4.9800,"t":"S"},{"DE":-12.4754,"RA":130.0061,"AM":4.9800,"t":"S"},{"DE":6.1014,"RA":165.1867,"AM":4.9800,"t":"S"},{"DE":-70.2258,"RA":177.4859,"AM":4.9800,"t":"S"},{"DE":26.8257,"RA":186.7471,"AM":4.9800,"t":"S"},{"DE":40.8993,"RA":232.9458,"AM":4.9800,"t":"S"},{"DE":29.8511,"RA":240.3607,"AM":4.9800,"t":"S"},{"DE":58.8007,"RA":275.9776,"AM":4.9800,"t":"S"},{"DE":4.2021,"RA":284.0610,"AM":4.9800,"t":"S"},{"DE":-5.4158,"RA":290.1371,"AM":4.9800,"t":"S"},{"DE":58.8460,"RA":298.9808,"AM":4.9800,"t":"S"},{"DE":-10.5095,"RA":1.1255,"AM":4.9900,"t":"S"},{"DE":54.4875,"RA":30.5754,"AM":4.9900,"t":"S"},{"DE":49.0629,"RA":52.0128,"AM":4.9900,"t":"S"},{"DE":-31.9384,"RA":55.5621,"AM":4.9900,"t":"S"},{"DE":61.1089,"RA":59.2845,"AM":4.9900,"t":"S"},{"DE":-12.1231,"RA":69.7231,"AM":4.9900,"t":"S"},{"DE":3.5445,"RA":80.7083,"AM":4.9900,"t":"S"},{"DE":41.7812,"RA":102.6915,"AM":4.9900,"t":"S"},{"DE":-34.3673,"RA":102.7181,"AM":4.9900,"t":"S"},{"DE":-4.2392,"RA":105.7282,"AM":4.9900,"t":"S"},{"DE":9.2761,"RA":111.4121,"AM":4.9900,"t":"S"},{"DE":-15.7882,"RA":123.3332,"AM":4.9900,"t":"S"},{"DE":5.0923,"RA":136.4932,"AM":4.9900,"t":"S"},{"DE":-44.8679,"RA":137.7683,"AM":4.9900,"t":"S"},{"DE":11.2998,"RA":142.9864,"AM":4.9900,"t":"S"},{"DE":43.4827,"RA":170.7066,"AM":4.9900,"t":"S"},{"DE":33.0615,"RA":184.1256,"AM":4.9900,"t":"S"},{"DE":-54.5594,"RA":205.4366,"AM":4.9900,"t":"S"},{"DE":2.4094,"RA":213.0659,"AM":4.9900,"t":"S"},{"DE":-47.9278,"RA":230.5346,"AM":4.9900,"t":"S"},{"DE":30.2878,"RA":230.8012,"AM":4.9900,"t":"S"},{"DE":-41.7444,"RA":239.8761,"AM":4.9900,"t":"S"},{"DE":64.3973,"RA":273.4732,"AM":4.9900,"t":"S"},{"DE":29.6213,"RA":291.0316,"AM":4.9900,"t":"S"},{"DE":-32.0563,"RA":301.0816,"AM":4.9900,"t":"S"},{"DE":-34.0438,"RA":332.1081,"AM":4.9900,"t":"S"},{"DE":49.7335,"RA":344.1083,"AM":4.9900,"t":"S"},{"DE":-9.6107,"RA":349.7403,"AM":4.9900,"t":"S"},{"DE":59.1555,"RA":61.1132,"AM":5.0000,"t":"S"},{"DE":17.3835,"RA":81.1061,"AM":5.0000,"t":"S"},{"DE":-37.2529,"RA":91.8818,"AM":5.0000,"t":"S"},{"DE":-13.7184,"RA":93.9370,"AM":5.0000,"t":"S"},{"DE":-14.0434,"RA":104.0277,"AM":5.0000,"t":"S"},{"DE":49.4648,"RA":109.6332,"AM":5.0000,"t":"S"},{"DE":6.8358,"RA":144.3028,"AM":5.0000,"t":"S"},{"DE":-36.1648,"RA":170.8029,"AM":5.0000,"t":"S"},{"DE":-62.4894,"RA":175.8800,"AM":5.0000,"t":"S"},{"DE":77.3494,"RA":232.8543,"AM":5.0000,"t":"S"},{"DE":17.0470,"RA":242.0189,"AM":5.0000,"t":"S"},{"DE":-30.2530,"RA":269.7720,"AM":5.0000,"t":"S"},{"DE":43.4619,"RA":271.8698,"AM":5.0000,"t":"S"},{"DE":-22.6713,"RA":283.7797,"AM":5.0000,"t":"S"},{"DE":46.9348,"RA":285.3599,"AM":5.0000,"t":"S"},{"DE":57.7051,"RA":288.4798,"AM":5.0000,"t":"S"},{"DE":19.7734,"RA":293.6454,"AM":5.0000,"t":"S"},{"DE":33.7276,"RA":296.6067,"AM":5.0000,"t":"S"},{"DE":-64.2982,"RA":359.3959,"AM":5.0000,"t":"S"},{"DE":-54.7081,"RA":131.1741,"AM":5.0000,"t":"S"},{"DE":-11.3746,"RA":241.0916,"AM":5.0000,"t":"S"},{"DE":-37.0647,"RA":286.6027,"AM":5.0000,"t":"S"},{"DE":46.0723,"RA":2.5802,"AM":5.0100,"t":"S"},{"DE":17.8931,"RA":7.0121,"AM":5.0100,"t":"S"},{"DE":44.3862,"RA":24.8375,"AM":5.0100,"t":"S"},{"DE":-26.2750,"RA":75.5409,"AM":5.0100,"t":"S"},{"DE":32.6876,"RA":78.8517,"AM":5.0100,"t":"S"},{"DE":-65.5894,"RA":92.8125,"AM":5.0100,"t":"S"},{"DE":61.5153,"RA":94.4784,"AM":5.0100,"t":"S"},{"DE":27.9161,"RA":112.4532,"AM":5.0100,"t":"S"},{"DE":-34.7054,"RA":118.0654,"AM":5.0100,"t":"S"},{"DE":-49.9442,"RA":128.6817,"AM":5.0100,"t":"S"},{"DE":-51.2553,"RA":143.5367,"AM":5.0100,"t":"S"},{"DE":69.0762,"RA":160.7668,"AM":5.0100,"t":"S"},{"DE":-65.3978,"RA":174.8734,"AM":5.0100,"t":"S"},{"DE":-55.1430,"RA":184.7491,"AM":5.0100,"t":"S"},{"DE":39.0186,"RA":186.4623,"AM":5.0100,"t":"S"},{"DE":69.2011,"RA":187.5280,"AM":5.0100,"t":"S"},{"DE":18.0571,"RA":260.0786,"AM":5.0100,"t":"S"},{"DE":19.1420,"RA":297.2444,"AM":5.0100,"t":"S"},{"DE":-15.4915,"RA":299.4876,"AM":5.0100,"t":"S"},{"DE":13.0476,"RA":67.2090,"AM":5.0200,"t":"S"},{"DE":37.3853,"RA":81.1631,"AM":5.0200,"t":"S"},{"DE":-21.1157,"RA":143.3019,"AM":5.0200,"t":"S"},{"DE":-47.0034,"RA":158.2370,"AM":5.0200,"t":"S"},{"DE":33.5069,"RA":163.9350,"AM":5.0200,"t":"S"},{"DE":27.4921,"RA":209.1424,"AM":5.0200,"t":"S"},{"DE":-37.8032,"RA":223.2128,"AM":5.0200,"t":"S"},{"DE":71.8239,"RA":229.2745,"AM":5.0200,"t":"S"},{"DE":50.7811,"RA":267.2679,"AM":5.0200,"t":"S"},{"DE":76.9629,"RA":267.3623,"AM":5.0200,"t":"S"},{"DE":49.1216,"RA":275.3861,"AM":5.0200,"t":"S"},{"DE":2.0600,"RA":281.2081,"AM":5.0200,"t":"S"},{"DE":-20.6563,"RA":284.3353,"AM":5.0200,"t":"S"},{"DE":-24.5086,"RA":291.3187,"AM":5.0200,"t":"S"},{"DE":-30.8983,"RA":326.9340,"AM":5.0200,"t":"S"},{"DE":22.6483,"RA":31.6413,"AM":5.0300,"t":"S"},{"DE":-16.2172,"RA":72.5484,"AM":5.0300,"t":"S"},{"DE":-26.2845,"RA":90.8150,"AM":5.0300,"t":"S"},{"DE":-36.5926,"RA":109.2059,"AM":5.0300,"t":"S"},{"DE":-14.5638,"RA":116.4870,"AM":5.0300,"t":"S"},{"DE":-44.7248,"RA":127.3645,"AM":5.0300,"t":"S"},{"DE":40.4303,"RA":164.8668,"AM":5.0300,"t":"S"},{"DE":18.3771,"RA":188.7823,"AM":5.0300,"t":"S"},{"DE":-8.7030,"RA":205.4032,"AM":5.0300,"t":"S"},{"DE":-57.0861,"RA":213.7381,"AM":5.0300,"t":"S"},{"DE":24.6564,"RA":252.9386,"AM":5.0300,"t":"S"},{"DE":-32.1435,"RA":255.4693,"AM":5.0300,"t":"S"},{"DE":10.8645,"RA":259.6541,"AM":5.0300,"t":"S"},{"DE":55.5395,"RA":280.6581,"AM":5.0300,"t":"S"},{"DE":-54.4239,"RA":290.7133,"AM":5.0300,"t":"S"},{"DE":-2.7889,"RA":292.6660,"AM":5.0300,"t":"S"},{"DE":52.9880,"RA":297.6572,"AM":5.0300,"t":"S"},{"DE":28.0576,"RA":313.6402,"AM":5.0300,"t":"S"},{"DE":-29.7204,"RA":0.5830,"AM":5.0400,"t":"S"},{"DE":43.9421,"RA":17.0034,"AM":5.0400,"t":"S"},{"DE":-53.5220,"RA":26.5259,"AM":5.0400,"t":"S"},{"DE":50.9377,"RA":49.0509,"AM":5.0400,"t":"S"},{"DE":-37.1443,"RA":70.5145,"AM":5.0400,"t":"S"},{"DE":-9.5582,"RA":89.7680,"AM":5.0400,"t":"S"},{"DE":-62.1546,"RA":91.7641,"AM":5.0400,"t":"S"},{"DE":12.2722,"RA":94.1109,"AM":5.0400,"t":"S"},{"DE":44.5245,"RA":100.7708,"AM":5.0400,"t":"S"},{"DE":25.0505,"RA":110.8688,"AM":5.0400,"t":"S"},{"DE":17.6745,"RA":114.8691,"AM":5.0400,"t":"S"},{"DE":-45.1731,"RA":115.7380,"AM":5.0400,"t":"S"},{"DE":-45.2660,"RA":121.6681,"AM":5.0400,"t":"S"},{"DE":-76.5191,"RA":181.1942,"AM":5.0400,"t":"S"},{"DE":-16.1986,"RA":198.0148,"AM":5.0400,"t":"S"},{"DE":-74.8878,"RA":201.2804,"AM":5.0400,"t":"S"},{"DE":-51.1651,"RA":202.3552,"AM":5.0400,"t":"S"},{"DE":-60.9573,"RA":229.2371,"AM":5.0400,"t":"S"},{"DE":1.7654,"RA":229.8283,"AM":5.0400,"t":"S"},{"DE":40.8330,"RA":232.7323,"AM":5.0400,"t":"S"},{"DE":-20.1670,"RA":238.3336,"AM":5.0400,"t":"S"},{"DE":43.9459,"RA":319.6133,"AM":5.0400,"t":"S"},{"DE":40.4135,"RA":324.2374,"AM":5.0400,"t":"S"},{"DE":73.1799,"RA":329.8128,"AM":5.0400,"t":"S"},{"DE":-4.2281,"RA":339.4391,"AM":5.0400,"t":"S"},{"DE":50.0950,"RA":49.7818,"AM":5.0500,"t":"S"},{"DE":24.1367,"RA":57.2967,"AM":5.0500,"t":"S"},{"DE":-49.5778,"RA":76.2416,"AM":5.0500,"t":"S"},{"DE":33.9581,"RA":80.0038,"AM":5.0500,"t":"S"},{"DE":-48.2202,"RA":99.6568,"AM":5.0500,"t":"S"},{"DE":87.0201,"RA":115.1294,"AM":5.0500,"t":"S"},{"DE":-22.6619,"RA":129.7830,"AM":5.0500,"t":"S"},{"DE":30.5621,"RA":271.7565,"AM":5.0500,"t":"S"},{"DE":59.4145,"RA":332.8774,"AM":5.0500,"t":"S"},{"DE":8.6772,"RA":347.3811,"AM":5.0500,"t":"S"},{"DE":5.3813,"RA":350.0858,"AM":5.0500,"t":"S"},{"DE":67.8068,"RA":356.9781,"AM":5.0500,"t":"S"},{"DE":63.2168,"RA":55.5389,"AM":5.0600,"t":"S"},{"DE":-26.9435,"RA":78.8516,"AM":5.0600,"t":"S"},{"DE":-24.7730,"RA":80.4427,"AM":5.0600,"t":"S"},{"DE":-68.8434,"RA":92.1846,"AM":5.0600,"t":"S"},{"DE":-6.5503,"RA":92.9659,"AM":5.0600,"t":"S"},{"DE":-4.7622,"RA":96.9899,"AM":5.0600,"t":"S"},{"DE":-23.4737,"RA":113.5776,"AM":5.0600,"t":"S"},{"DE":-65.6132,"RA":124.5783,"AM":5.0600,"t":"S"},{"DE":-47.3700,"RA":151.5467,"AM":5.0600,"t":"S"},{"DE":39.2121,"RA":165.2101,"AM":5.0600,"t":"S"},{"DE":-80.1089,"RA":215.5966,"AM":5.0600,"t":"S"},{"DE":-44.5577,"RA":257.6764,"AM":5.0600,"t":"S"},{"DE":45.5249,"RA":295.2090,"AM":5.0600,"t":"S"},{"DE":-16.1240,"RA":295.6297,"AM":5.0600,"t":"S"},{"DE":50.1047,"RA":300.3398,"AM":5.0600,"t":"S"},{"DE":24.1160,"RA":309.6330,"AM":5.0600,"t":"S"},{"DE":44.0593,"RA":312.5204,"AM":5.0600,"t":"S"},{"DE":-51.6082,"RA":312.8752,"AM":5.0600,"t":"S"},{"DE":-70.1263,"RA":318.3353,"AM":5.0600,"t":"S"},{"DE":19.1203,"RA":358.1220,"AM":5.0600,"t":"S"},{"DE":-63.0315,"RA":8.1827,"AM":5.0700,"t":"S"},{"DE":16.9406,"RA":12.2446,"AM":5.0700,"t":"S"},{"DE":-1.1961,"RA":48.1935,"AM":5.0700,"t":"S"},{"DE":-44.9537,"RA":67.7087,"AM":5.0700,"t":"S"},{"DE":53.0795,"RA":69.9779,"AM":5.0700,"t":"S"},{"DE":-0.8913,"RA":81.1205,"AM":5.0700,"t":"S"},{"DE":-34.1117,"RA":104.6046,"AM":5.0700,"t":"S"},{"DE":16.1590,"RA":108.3428,"AM":5.0700,"t":"S"},{"DE":28.1183,"RA":112.3352,"AM":5.0700,"t":"S"},{"DE":-38.5111,"RA":116.8541,"AM":5.0700,"t":"S"},{"DE":9.7158,"RA":142.9899,"AM":5.0700,"t":"S"},{"DE":-80.9413,"RA":143.4729,"AM":5.0700,"t":"S"},{"DE":-14.3323,"RA":145.0765,"AM":5.0700,"t":"S"},{"DE":-8.1050,"RA":148.1268,"AM":5.0700,"t":"S"},{"DE":6.9537,"RA":158.7001,"AM":5.0700,"t":"S"},{"DE":-59.4421,"RA":172.9420,"AM":5.0700,"t":"S"},{"DE":-27.2612,"RA":213.1918,"AM":5.0700,"t":"S"},{"DE":52.9244,"RA":249.0572,"AM":5.0700,"t":"S"},{"DE":40.7770,"RA":257.3886,"AM":5.0700,"t":"S"},{"DE":68.1350,"RA":262.9912,"AM":5.0700,"t":"S"},{"DE":-45.7574,"RA":278.0081,"AM":5.0700,"t":"S"},{"DE":11.0712,"RA":286.7442,"AM":5.0700,"t":"S"},{"DE":10.0862,"RA":309.7824,"AM":5.0700,"t":"S"},{"DE":30.1742,"RA":327.4612,"AM":5.0700,"t":"S"},{"DE":62.2798,"RA":331.2866,"AM":5.0700,"t":"S"},{"DE":-26.6032,"RA":258.8360,"AM":5.0700,"t":"S"},{"DE":54.1684,"RA":9.0346,"AM":5.0800,"t":"S"},{"DE":11.1433,"RA":57.0678,"AM":5.0800,"t":"S"},{"DE":15.7998,"RA":69.7884,"AM":5.0800,"t":"S"},{"DE":18.8399,"RA":72.8436,"AM":5.0800,"t":"S"},{"DE":79.2311,"RA":80.6405,"AM":5.0800,"t":"S"},{"DE":34.4759,"RA":81.9120,"AM":5.0800,"t":"S"},{"DE":-74.7530,"RA":92.5595,"AM":5.0800,"t":"S"},{"DE":-8.9985,"RA":101.9051,"AM":5.0800,"t":"S"},{"DE":-44.1099,"RA":119.3268,"AM":5.0800,"t":"S"},{"DE":-53.0885,"RA":126.9025,"AM":5.0800,"t":"S"},{"DE":46.0210,"RA":147.1472,"AM":5.0800,"t":"S"},{"DE":-0.6370,"RA":157.5728,"AM":5.0800,"t":"S"},{"DE":-23.7452,"RA":158.5037,"AM":5.0800,"t":"S"},{"DE":-59.5644,"RA":159.0856,"AM":5.0800,"t":"S"},{"DE":23.1884,"RA":160.8540,"AM":5.0800,"t":"S"},{"DE":-18.7800,"RA":170.8412,"AM":5.0800,"t":"S"},{"DE":-57.1687,"RA":193.6538,"AM":5.0800,"t":"S"},{"DE":-62.7810,"RA":224.1833,"AM":5.0800,"t":"S"},{"DE":-15.6030,"RA":283.6796,"AM":5.0800,"t":"S"},{"DE":23.6144,"RA":301.7225,"AM":5.0800,"t":"S"},{"DE":-18.2117,"RA":306.8300,"AM":5.0800,"t":"S"},{"DE":-13.5518,"RA":328.3240,"AM":5.0800,"t":"S"},{"DE":73.6432,"RA":338.9412,"AM":5.0800,"t":"S"},{"DE":-74.9234,"RA":12.1467,"AM":5.0900,"t":"S"},{"DE":17.8175,"RA":29.3377,"AM":5.0900,"t":"S"},{"DE":55.4518,"RA":52.5009,"AM":5.0900,"t":"S"},{"DE":81.1941,"RA":75.0863,"AM":5.0900,"t":"S"},{"DE":-1.2202,"RA":98.4080,"AM":5.0900,"t":"S"},{"DE":20.4437,"RA":110.4869,"AM":5.0900,"t":"S"},{"DE":-51.0185,"RA":111.5910,"AM":5.0900,"t":"S"},{"DE":-23.3104,"RA":119.7738,"AM":5.0900,"t":"S"},{"DE":-36.3223,"RA":123.4930,"AM":5.0900,"t":"S"},{"DE":-46.5292,"RA":132.6394,"AM":5.0900,"t":"S"},{"DE":-53.3789,"RA":141.5749,"AM":5.0900,"t":"S"},{"DE":57.1281,"RA":146.6319,"AM":5.0900,"t":"S"},{"DE":-45.7327,"RA":147.4881,"AM":5.0900,"t":"S"},{"DE":-64.9547,"RA":170.8392,"AM":5.0900,"t":"S"},{"DE":14.8991,"RA":184.0008,"AM":5.0900,"t":"S"},{"DE":-3.0905,"RA":237.8150,"AM":5.0900,"t":"S"},{"DE":-29.4162,"RA":242.7587,"AM":5.0900,"t":"S"},{"DE":25.6229,"RA":267.2048,"AM":5.0900,"t":"S"},{"DE":-38.6569,"RA":275.5774,"AM":5.0900,"t":"S"},{"DE":19.9911,"RA":301.2896,"AM":5.0900,"t":"S"},{"DE":43.2738,"RA":325.0462,"AM":5.0900,"t":"S"},{"DE":25.9251,"RA":328.2657,"AM":5.0900,"t":"S"},{"DE":45.0143,"RA":331.5081,"AM":5.0900,"t":"S"},{"DE":-80.4397,"RA":335.0063,"AM":5.0900,"t":"S"},{"DE":42.7578,"RA":345.6515,"AM":5.0900,"t":"S"},{"DE":12.3139,"RA":350.7690,"AM":5.0900,"t":"S"},{"DE":10.3315,"RA":355.8432,"AM":5.0900,"t":"S"},{"DE":31.9342,"RA":44.3220,"AM":5.1000,"t":"S"},{"DE":20.7421,"RA":50.6885,"AM":5.1000,"t":"S"},{"DE":80.6987,"RA":62.5116,"AM":5.1000,"t":"S"},{"DE":9.4610,"RA":65.9659,"AM":5.1000,"t":"S"},{"DE":-66.9012,"RA":87.4731,"AM":5.1000,"t":"S"},{"DE":-26.7498,"RA":177.1879,"AM":5.1000,"t":"S"},{"DE":-31.5062,"RA":199.2214,"AM":5.1000,"t":"S"},{"DE":5.8201,"RA":216.0473,"AM":5.1000,"t":"S"},{"DE":17.8184,"RA":240.3097,"AM":5.1000,"t":"S"},{"DE":-67.1097,"RA":251.6667,"AM":5.1000,"t":"S"},{"DE":-44.1626,"RA":261.0545,"AM":5.1000,"t":"S"},{"DE":20.0452,"RA":272.2203,"AM":5.1000,"t":"S"},{"DE":1.0851,"RA":289.6354,"AM":5.1000,"t":"S"},{"DE":2.2436,"RA":324.8886,"AM":5.1000,"t":"S"},{"DE":-9.0824,"RA":326.2511,"AM":5.1000,"t":"S"},{"DE":56.9454,"RA":345.0213,"AM":5.1000,"t":"S"},{"DE":-82.0188,"RA":358.0278,"AM":5.1000,"t":"S"},{"DE":-21.6293,"RA":22.4006,"AM":5.1100,"t":"S"},{"DE":-34.7323,"RA":58.4123,"AM":5.1100,"t":"S"},{"DE":-4.4562,"RA":77.1821,"AM":5.1100,"t":"S"},{"DE":68.8883,"RA":103.4260,"AM":5.1100,"t":"S"},{"DE":-36.7427,"RA":109.6591,"AM":5.1100,"t":"S"},{"DE":41.0556,"RA":149.4212,"AM":5.1100,"t":"S"},{"DE":-61.9472,"RA":167.1417,"AM":5.1100,"t":"S"},{"DE":-39.7551,"RA":201.5322,"AM":5.1100,"t":"S"},{"DE":-68.6030,"RA":238.8734,"AM":5.1100,"t":"S"},{"DE":39.5072,"RA":276.0575,"AM":5.1100,"t":"S"},{"DE":-38.3234,"RA":280.9456,"AM":5.1100,"t":"S"},{"DE":76.5605,"RA":287.2907,"AM":5.1100,"t":"S"},{"DE":-60.5489,"RA":310.0102,"AM":5.1100,"t":"S"},{"DE":-43.9885,"RA":312.1213,"AM":5.1100,"t":"S"},{"DE":63.6256,"RA":329.1631,"AM":5.1100,"t":"S"},{"DE":-41.6272,"RA":334.1107,"AM":5.1100,"t":"S"},{"DE":56.7956,"RA":339.6579,"AM":5.1100,"t":"S"},{"DE":41.8192,"RA":341.0228,"AM":5.1100,"t":"S"},{"DE":-42.4969,"RA":28.5918,"AM":5.1200,"t":"S"},{"DE":-59.7378,"RA":45.9036,"AM":5.1200,"t":"S"},{"DE":-4.6552,"RA":76.6902,"AM":5.1200,"t":"S"},{"DE":-48.9321,"RA":107.6979,"AM":5.1200,"t":"S"},{"DE":36.7606,"RA":110.5110,"AM":5.1200,"t":"S"},{"DE":-40.9337,"RA":115.9246,"AM":5.1200,"t":"S"},{"DE":1.7669,"RA":117.9249,"AM":5.1200,"t":"S"},{"DE":-44.2657,"RA":139.0960,"AM":5.1200,"t":"S"},{"DE":-49.0051,"RA":143.4356,"AM":5.1200,"t":"S"},{"DE":65.7163,"RA":160.4862,"AM":5.1200,"t":"S"},{"DE":54.5851,"RA":163.3937,"AM":5.1200,"t":"S"},{"DE":-59.5156,"RA":172.9533,"AM":5.1200,"t":"S"},{"DE":-41.0219,"RA":188.9398,"AM":5.1200,"t":"S"},{"DE":16.5777,"RA":191.6615,"AM":5.1200,"t":"S"},{"DE":-51.8341,"RA":266.0363,"AM":5.1200,"t":"S"},{"DE":28.8700,"RA":275.2542,"AM":5.1200,"t":"S"},{"DE":-18.4027,"RA":277.8596,"AM":5.1200,"t":"S"},{"DE":-10.9772,"RA":278.7600,"AM":5.1200,"t":"S"},{"DE":27.9653,"RA":292.6891,"AM":5.1200,"t":"S"},{"DE":-10.5604,"RA":293.7802,"AM":5.1200,"t":"S"},{"DE":10.4157,"RA":297.7568,"AM":5.1200,"t":"S"},{"DE":-44.5160,"RA":308.4795,"AM":5.1200,"t":"S"},{"DE":-21.5982,"RA":335.3982,"AM":5.1200,"t":"S"},{"DE":-34.7494,"RA":345.8742,"AM":5.1200,"t":"S"},{"DE":-3.0275,"RA":0.4560,"AM":5.1300,"t":"S"},{"DE":-7.7805,"RA":3.6151,"AM":5.1300,"t":"S"},{"DE":3.6145,"RA":19.4498,"AM":5.1300,"t":"S"},{"DE":-33.8110,"RA":37.0071,"AM":5.1300,"t":"S"},{"DE":64.5860,"RA":51.1690,"AM":5.1300,"t":"S"},{"DE":-5.3897,"RA":83.8186,"AM":5.1300,"t":"S"},{"DE":27.2177,"RA":125.0161,"AM":5.1300,"t":"S"},{"DE":7.5645,"RA":126.4782,"AM":5.1300,"t":"S"},{"DE":-31.0872,"RA":173.2255,"AM":5.1300,"t":"S"},{"DE":43.8545,"RA":211.9823,"AM":5.1300,"t":"S"},{"DE":-41.0672,"RA":226.3298,"AM":5.1300,"t":"S"},{"DE":-28.0470,"RA":233.6555,"AM":5.1300,"t":"S"},{"DE":-47.3720,"RA":243.8139,"AM":5.1300,"t":"S"},{"DE":24.4994,"RA":260.2259,"AM":5.1300,"t":"S"},{"DE":56.8592,"RA":287.9190,"AM":5.1300,"t":"S"},{"DE":-77.0238,"RA":316.1793,"AM":5.1300,"t":"S"},{"DE":-52.7458,"RA":359.7323,"AM":5.1300,"t":"S"},{"DE":44.4886,"RA":9.1935,"AM":5.1400,"t":"S"},{"DE":-7.9228,"RA":18.6002,"AM":5.1400,"t":"S"},{"DE":11.3364,"RA":52.6020,"AM":5.1400,"t":"S"},{"DE":33.0914,"RA":57.3862,"AM":5.1400,"t":"S"},{"DE":-58.9125,"RA":81.5803,"AM":5.1400,"t":"S"},{"DE":19.6906,"RA":90.8640,"AM":5.1400,"t":"S"},{"DE":-46.6146,"RA":102.4776,"AM":5.1400,"t":"S"},{"DE":67.5719,"RA":102.7379,"AM":5.1400,"t":"S"},{"DE":-51.4026,"RA":105.2145,"AM":5.1400,"t":"S"},{"DE":10.9518,"RA":105.9086,"AM":5.1400,"t":"S"},{"DE":-56.7497,"RA":106.0764,"AM":5.1400,"t":"S"},{"DE":-4.1110,"RA":114.3195,"AM":5.1400,"t":"S"},{"DE":33.4157,"RA":116.8764,"AM":5.1400,"t":"S"},{"DE":-45.5777,"RA":119.4655,"AM":5.1400,"t":"S"},{"DE":13.1182,"RA":121.2687,"AM":5.1400,"t":"S"},{"DE":-46.9916,"RA":123.4007,"AM":5.1400,"t":"S"},{"DE":-56.7572,"RA":161.7395,"AM":5.1400,"t":"S"},{"DE":-42.6742,"RA":172.1462,"AM":5.1400,"t":"S"},{"DE":-61.2834,"RA":174.2528,"AM":5.1400,"t":"S"},{"DE":77.6162,"RA":183.0497,"AM":5.1400,"t":"S"},{"DE":-13.5657,"RA":185.2321,"AM":5.1400,"t":"S"},{"DE":49.6821,"RA":199.5605,"AM":5.1400,"t":"S"},{"DE":-2.2655,"RA":214.8853,"AM":5.1400,"t":"S"},{"DE":39.0101,"RA":233.8121,"AM":5.1400,"t":"S"},{"DE":-33.9661,"RA":239.2229,"AM":5.1400,"t":"S"},{"DE":-24.2869,"RA":259.5028,"AM":5.1400,"t":"S"},{"DE":-60.2005,"RA":284.6522,"AM":5.1400,"t":"S"},{"DE":2.2937,"RA":288.4279,"AM":5.1400,"t":"S"},{"DE":19.7984,"RA":291.3692,"AM":5.1400,"t":"S"},{"DE":57.5235,"RA":298.3224,"AM":5.1400,"t":"S"},{"DE":34.9828,"RA":304.6628,"AM":5.1400,"t":"S"},{"DE":-66.7607,"RA":310.4878,"AM":5.1400,"t":"S"},{"DE":31.4247,"RA":17.7782,"AM":5.1500,"t":"S"},{"DE":-44.7135,"RA":30.4266,"AM":5.1500,"t":"S"},{"DE":36.1473,"RA":38.0257,"AM":5.1500,"t":"S"},{"DE":-16.8159,"RA":94.4238,"AM":5.1500,"t":"S"},{"DE":37.5174,"RA":116.6637,"AM":5.1500,"t":"S"},{"DE":-49.8228,"RA":130.9178,"AM":5.1500,"t":"S"},{"DE":43.7266,"RA":132.9868,"AM":5.1500,"t":"S"},{"DE":66.8732,"RA":137.0980,"AM":5.1500,"t":"S"},{"DE":72.2526,"RA":145.7384,"AM":5.1500,"t":"S"},{"DE":-66.3728,"RA":153.3778,"AM":5.1500,"t":"S"},{"DE":-42.6387,"RA":166.8196,"AM":5.1500,"t":"S"},{"DE":-61.8266,"RA":174.5306,"AM":5.1500,"t":"S"},{"DE":-42.4341,"RA":180.9146,"AM":5.1500,"t":"S"},{"DE":-67.5221,"RA":185.5307,"AM":5.1500,"t":"S"},{"DE":-10.7404,"RA":196.9742,"AM":5.1500,"t":"S"},{"DE":-36.2519,"RA":206.7348,"AM":5.1500,"t":"S"},{"DE":-25.4432,"RA":221.5004,"AM":5.1500,"t":"S"},{"DE":-15.9972,"RA":222.6716,"AM":5.1500,"t":"S"},{"DE":67.3467,"RA":228.6589,"AM":5.1500,"t":"S"},{"DE":-41.4912,"RA":229.0168,"AM":5.1500,"t":"S"},{"DE":1.8421,"RA":232.1593,"AM":5.1500,"t":"S"},{"DE":8.5826,"RA":251.4579,"AM":5.1500,"t":"S"},{"DE":37.0429,"RA":299.9800,"AM":5.1500,"t":"S"},{"DE":0.4864,"RA":309.8537,"AM":5.1500,"t":"S"},{"DE":-18.1387,"RA":310.0123,"AM":5.1500,"t":"S"},{"DE":16.1241,"RA":311.6619,"AM":5.1500,"t":"S"},{"DE":8.7201,"RA":347.9341,"AM":5.1500,"t":"S"},{"DE":37.9686,"RA":5.2803,"AM":5.1600,"t":"S"},{"DE":55.8457,"RA":35.5893,"AM":5.1600,"t":"S"},{"DE":-3.7123,"RA":44.1559,"AM":5.1600,"t":"S"},{"DE":50.2222,"RA":49.6572,"AM":5.1600,"t":"S"},{"DE":-52.1089,"RA":87.7218,"AM":5.1600,"t":"S"},{"DE":-12.3920,"RA":97.8460,"AM":5.1600,"t":"S"},{"DE":-13.8980,"RA":117.9429,"AM":5.1600,"t":"S"},{"DE":-62.9156,"RA":123.8164,"AM":5.1600,"t":"S"},{"DE":22.0454,"RA":137.3397,"AM":5.1600,"t":"S"},{"DE":57.0826,"RA":158.7903,"AM":5.1600,"t":"S"},{"DE":-1.5031,"RA":208.6756,"AM":5.1600,"t":"S"},{"DE":-64.0314,"RA":226.2005,"AM":5.1600,"t":"S"},{"DE":15.4280,"RA":231.4475,"AM":5.1600,"t":"S"},{"DE":-9.1834,"RA":233.6105,"AM":5.1600,"t":"S"},{"DE":-39.7040,"RA":278.0889,"AM":5.1600,"t":"S"},{"DE":6.8111,"RA":320.7234,"AM":5.1600,"t":"S"},{"DE":-14.0476,"RA":325.3869,"AM":5.1600,"t":"S"},{"DE":9.8357,"RA":343.1003,"AM":5.1600,"t":"S"},{"DE":-23.7877,"RA":7.5944,"AM":5.1700,"t":"S"},{"DE":-10.6443,"RA":12.5316,"AM":5.1700,"t":"S"},{"DE":54.9203,"RA":17.0622,"AM":5.1700,"t":"S"},{"DE":72.8183,"RA":39.5086,"AM":5.1700,"t":"S"},{"DE":12.4458,"RA":41.2399,"AM":5.1700,"t":"S"},{"DE":-3.7455,"RA":65.9202,"AM":5.1700,"t":"S"},{"DE":-17.2284,"RA":117.4217,"AM":5.1700,"t":"S"},{"DE":-47.2347,"RA":134.7182,"AM":5.1700,"t":"S"},{"DE":-59.0837,"RA":134.8512,"AM":5.1700,"t":"S"},{"DE":-17.1508,"RA":179.0040,"AM":5.1700,"t":"S"},{"DE":-75.3670,"RA":181.9585,"AM":5.1700,"t":"S"},{"DE":26.0986,"RA":186.0772,"AM":5.1700,"t":"S"},{"DE":-13.0139,"RA":190.3165,"AM":5.1700,"t":"S"},{"DE":-51.1988,"RA":194.2682,"AM":5.1700,"t":"S"},{"DE":40.0080,"RA":268.3251,"AM":5.1700,"t":"S"},{"DE":-52.3409,"RA":286.5831,"AM":5.1700,"t":"S"},{"DE":11.9444,"RA":291.2425,"AM":5.1700,"t":"S"},{"DE":36.3179,"RA":291.5380,"AM":5.1700,"t":"S"},{"DE":44.6949,"RA":294.1583,"AM":5.1700,"t":"S"},{"DE":-54.7270,"RA":316.3093,"AM":5.1700,"t":"S"},{"DE":-20.6517,"RA":318.9079,"AM":5.1700,"t":"S"},{"DE":-18.9092,"RA":357.8389,"AM":5.1700,"t":"S"},{"DE":17.5290,"RA":197.4958,"AM":5.1700,"t":"S"},{"DE":-28.9815,"RA":5.3800,"AM":5.1800,"t":"S"},{"DE":44.3945,"RA":7.0568,"AM":5.1800,"t":"S"},{"DE":70.6225,"RA":25.7324,"AM":5.1800,"t":"S"},{"DE":27.5999,"RA":61.6517,"AM":5.1800,"t":"S"},{"DE":11.4260,"RA":73.6954,"AM":5.1800,"t":"S"},{"DE":16.0457,"RA":77.9232,"AM":5.1800,"t":"S"},{"DE":-76.3410,"RA":82.9698,"AM":5.1800,"t":"S"},{"DE":25.8971,"RA":84.9342,"AM":5.1800,"t":"S"},{"DE":-32.3064,"RA":86.4996,"AM":5.1800,"t":"S"},{"DE":-67.9164,"RA":104.9607,"AM":5.1800,"t":"S"},{"DE":-16.2015,"RA":111.1674,"AM":5.1800,"t":"S"},{"DE":-36.4842,"RA":125.3377,"AM":5.1800,"t":"S"},{"DE":-51.7274,"RA":126.3805,"AM":5.1800,"t":"S"},{"DE":-53.0547,"RA":129.9900,"AM":5.1800,"t":"S"},{"DE":61.4233,"RA":138.5856,"AM":5.1800,"t":"S"},{"DE":46.2039,"RA":160.8873,"AM":5.1800,"t":"S"},{"DE":2.0106,"RA":169.3225,"AM":5.1800,"t":"S"},{"DE":-63.9725,"RA":171.4308,"AM":5.1800,"t":"S"},{"DE":69.4325,"RA":213.0168,"AM":5.1800,"t":"S"},{"DE":-60.1142,"RA":223.8943,"AM":5.1800,"t":"S"},{"DE":-52.1074,"RA":283.1651,"AM":5.1800,"t":"S"},{"DE":5.3978,"RA":294.7985,"AM":5.1800,"t":"S"},{"DE":38.7224,"RA":297.6416,"AM":5.1800,"t":"S"},{"DE":23.5089,"RA":303.8760,"AM":5.1800,"t":"S"},{"DE":74.9546,"RA":307.8767,"AM":5.1800,"t":"S"},{"DE":72.3201,"RA":325.7671,"AM":5.1800,"t":"S"},{"DE":-50.2265,"RA":356.8166,"AM":5.1800,"t":"S"},{"DE":-23.8163,"RA":35.6356,"AM":5.1900,"t":"S"},{"DE":50.0065,"RA":36.1038,"AM":5.1900,"t":"S"},{"DE":-63.3997,"RA":76.8917,"AM":5.1900,"t":"S"},{"DE":-6.7089,"RA":91.0563,"AM":5.1900,"t":"S"},{"DE":0.2992,"RA":96.8073,"AM":5.1900,"t":"S"},{"DE":-60.5871,"RA":119.9064,"AM":5.1900,"t":"S"},{"DE":-70.3867,"RA":129.7714,"AM":5.1900,"t":"S"},{"DE":-32.7805,"RA":132.4646,"AM":5.1900,"t":"S"},{"DE":-2.7391,"RA":157.3696,"AM":5.1900,"t":"S"},{"DE":69.3230,"RA":174.0112,"AM":5.1900,"t":"S"},{"DE":9.4242,"RA":199.1938,"AM":5.1900,"t":"S"},{"DE":-16.2568,"RA":226.6567,"AM":5.1900,"t":"S"},{"DE":62.5996,"RA":236.6666,"AM":5.1900,"t":"S"},{"DE":-61.6335,"RA":247.7057,"AM":5.1900,"t":"S"},{"DE":-50.6335,"RA":261.5002,"AM":5.1900,"t":"S"},{"DE":28.6948,"RA":303.5605,"AM":5.1900,"t":"S"},{"DE":13.7215,"RA":313.9029,"AM":5.1900,"t":"S"},{"DE":64.8719,"RA":319.8426,"AM":5.1900,"t":"S"},{"DE":63.5845,"RA":339.6627,"AM":5.1900,"t":"S"},{"DE":-15.0393,"RA":350.6632,"AM":5.1900,"t":"S"},{"DE":29.7516,"RA":7.5307,"AM":5.2000,"t":"S"},{"DE":-3.5928,"RA":8.8120,"AM":5.2000,"t":"S"},{"DE":53.6118,"RA":64.1796,"AM":5.2000,"t":"S"},{"DE":-8.2314,"RA":68.5485,"AM":5.2000,"t":"S"},{"DE":59.8884,"RA":88.7409,"AM":5.2000,"t":"S"},{"DE":19.1564,"RA":93.7120,"AM":5.2000,"t":"S"},{"DE":-56.8528,"RA":97.3688,"AM":5.2000,"t":"S"},{"DE":17.6453,"RA":100.6014,"AM":5.2000,"t":"S"},{"DE":24.2154,"RA":105.6033,"AM":5.2000,"t":"S"},{"DE":-42.3373,"RA":106.0117,"AM":5.2000,"t":"S"},{"DE":59.6375,"RA":108.9790,"AM":5.2000,"t":"S"},{"DE":21.4452,"RA":111.9349,"AM":5.2000,"t":"S"},{"DE":-44.1228,"RA":122.3997,"AM":5.2000,"t":"S"},{"DE":-40.2639,"RA":130.0799,"AM":5.2000,"t":"S"},{"DE":-45.4107,"RA":130.4871,"AM":5.2000,"t":"S"},{"DE":-32.4994,"RA":175.4331,"AM":5.2000,"t":"S"},{"DE":-22.2159,"RA":185.1402,"AM":5.2000,"t":"S"},{"DE":35.7989,"RA":196.4352,"AM":5.2000,"t":"S"},{"DE":-24.9722,"RA":209.6298,"AM":5.2000,"t":"S"},{"DE":33.7991,"RA":245.5893,"AM":5.2000,"t":"S"},{"DE":0.1961,"RA":276.8021,"AM":5.2000,"t":"S"},{"DE":-40.4062,"RA":281.9359,"AM":5.2000,"t":"S"},{"DE":32.9013,"RA":284.2566,"AM":5.2000,"t":"S"},{"DE":32.5017,"RA":286.8565,"AM":5.2000,"t":"S"},{"DE":-32.3416,"RA":316.6028,"AM":5.2000,"t":"S"},{"DE":38.7494,"RA":316.7219,"AM":5.2000,"t":"S"},{"DE":-13.4586,"RA":349.7778,"AM":5.2000,"t":"S"},{"DE":-41.4869,"RA":16.9494,"AM":5.2100,"t":"S"},{"DE":7.5754,"RA":18.4329,"AM":5.2100,"t":"S"},{"DE":-54.5499,"RA":40.1650,"AM":5.2100,"t":"S"},{"DE":29.0013,"RA":61.7519,"AM":5.2100,"t":"S"},{"DE":0.5530,"RA":89.7066,"AM":5.2100,"t":"S"},{"DE":-11.5301,"RA":96.0430,"AM":5.2100,"t":"S"},{"DE":58.4174,"RA":96.7036,"AM":5.2100,"t":"S"},{"DE":-9.1675,"RA":100.4849,"AM":5.2100,"t":"S"},{"DE":-36.0631,"RA":171.3728,"AM":5.2100,"t":"S"},{"DE":-19.9431,"RA":198.9948,"AM":5.2100,"t":"S"},{"DE":-10.1650,"RA":203.2420,"AM":5.2100,"t":"S"},{"DE":2.1965,"RA":237.5731,"AM":5.2100,"t":"S"},{"DE":-47.4682,"RA":260.8170,"AM":5.2100,"t":"S"},{"DE":-20.7082,"RA":338.6735,"AM":5.2100,"t":"S"},{"DE":-22.0061,"RA":11.1850,"AM":5.2200,"t":"S"},{"DE":76.1151,"RA":31.3815,"AM":5.2200,"t":"S"},{"DE":-2.7829,"RA":44.6753,"AM":5.2200,"t":"S"},{"DE":10.0114,"RA":63.6510,"AM":5.2200,"t":"S"},{"DE":-2.4735,"RA":69.4005,"AM":5.2200,"t":"S"},{"DE":58.9724,"RA":76.5352,"AM":5.2200,"t":"S"},{"DE":41.8046,"RA":80.4517,"AM":5.2200,"t":"S"},{"DE":11.5444,"RA":97.9512,"AM":5.2200,"t":"S"},{"DE":48.7895,"RA":101.9149,"AM":5.2200,"t":"S"},{"DE":-5.7221,"RA":105.4849,"AM":5.2200,"t":"S"},{"DE":6.9420,"RA":112.0086,"AM":5.2200,"t":"S"},{"DE":-46.6085,"RA":116.8813,"AM":5.2200,"t":"S"},{"DE":-39.2969,"RA":119.8683,"AM":5.2200,"t":"S"},{"DE":15.3228,"RA":134.3123,"AM":5.2200,"t":"S"},{"DE":-64.1698,"RA":168.1885,"AM":5.2200,"t":"S"},{"DE":-61.1152,"RA":171.6476,"AM":5.2200,"t":"S"},{"DE":43.0456,"RA":180.5286,"AM":5.2200,"t":"S"},{"DE":7.6733,"RA":191.4044,"AM":5.2200,"t":"S"},{"DE":-61.2730,"RA":214.9650,"AM":5.2200,"t":"S"},{"DE":-52.3835,"RA":221.7554,"AM":5.2200,"t":"S"},{"DE":5.2467,"RA":251.9434,"AM":5.2200,"t":"S"},{"DE":-20.3247,"RA":282.4171,"AM":5.2200,"t":"S"},{"DE":32.5511,"RA":282.4705,"AM":5.2200,"t":"S"},{"DE":26.2624,"RA":290.7120,"AM":5.2200,"t":"S"},{"DE":64.8210,"RA":300.3689,"AM":5.2200,"t":"S"},{"DE":46.5406,"RA":322.3622,"AM":5.2200,"t":"S"},{"DE":39.2362,"RA":352.8224,"AM":5.2200,"t":"S"},{"DE":28.7382,"RA":20.2807,"AM":5.2300,"t":"S"},{"DE":21.2110,"RA":33.2003,"AM":5.2300,"t":"S"},{"DE":-6.0886,"RA":46.6395,"AM":5.2300,"t":"S"},{"DE":-31.0705,"RA":101.1186,"AM":5.2300,"t":"S"},{"DE":40.6724,"RA":111.0353,"AM":5.2300,"t":"S"},{"DE":-47.9372,"RA":122.4298,"AM":5.2300,"t":"S"},{"DE":27.9275,"RA":133.9153,"AM":5.2300,"t":"S"},{"DE":32.4186,"RA":134.8861,"AM":5.2300,"t":"S"},{"DE":-52.1887,"RA":135.4357,"AM":5.2300,"t":"S"},{"DE":10.6682,"RA":136.9367,"AM":5.2300,"t":"S"},{"DE":-35.8910,"RA":149.7179,"AM":5.2300,"t":"S"},{"DE":-64.2632,"RA":161.6233,"AM":5.2300,"t":"S"},{"DE":-20.1387,"RA":163.3730,"AM":5.2300,"t":"S"},{"DE":65.4385,"RA":193.8690,"AM":5.2300,"t":"S"},{"DE":-26.0875,"RA":221.9367,"AM":5.2300,"t":"S"},{"DE":-37.4249,"RA":235.6597,"AM":5.2300,"t":"S"},{"DE":33.8586,"RA":243.6703,"AM":5.2300,"t":"S"},{"DE":-41.2305,"RA":252.8905,"AM":5.2300,"t":"S"},{"DE":-6.1540,"RA":253.6487,"AM":5.2300,"t":"S"},{"DE":61.8746,"RA":263.7475,"AM":5.2300,"t":"S"},{"DE":6.0732,"RA":287.2496,"AM":5.2300,"t":"S"},{"DE":24.9380,"RA":300.5059,"AM":5.2300,"t":"S"},{"DE":-35.1331,"RA":2.9333,"AM":5.2400,"t":"S"},{"DE":-50.9868,"RA":12.6715,"AM":5.2400,"t":"S"},{"DE":20.2685,"RA":25.6241,"AM":5.2400,"t":"S"},{"DE":52.3517,"RA":45.2175,"AM":5.2400,"t":"S"},{"DE":-62.5064,"RA":49.5496,"AM":5.2400,"t":"S"},{"DE":-17.4671,"RA":54.0726,"AM":5.2400,"t":"S"},{"DE":-1.1631,"RA":56.1271,"AM":5.2400,"t":"S"},{"DE":-23.8747,"RA":56.9152,"AM":5.2400,"t":"S"},{"DE":25.5794,"RA":57.5789,"AM":5.2400,"t":"S"},{"DE":-63.3864,"RA":65.4719,"AM":5.2400,"t":"S"},{"DE":-8.9703,"RA":68.5490,"AM":5.2400,"t":"S"},{"DE":57.5444,"RA":80.8660,"AM":5.2400,"t":"S"},{"DE":-4.8561,"RA":83.9145,"AM":5.2400,"t":"S"},{"DE":43.5774,"RA":101.6847,"AM":5.2400,"t":"S"},{"DE":-39.2103,"RA":109.6396,"AM":5.2400,"t":"S"},{"DE":1.9145,"RA":113.0248,"AM":5.2400,"t":"S"},{"DE":-26.2550,"RA":129.4673,"AM":5.2400,"t":"S"},{"DE":-43.2275,"RA":138.6020,"AM":5.2400,"t":"S"},{"DE":-6.3531,"RA":139.1739,"AM":5.2400,"t":"S"},{"DE":8.1343,"RA":174.6150,"AM":5.2400,"t":"S"},{"DE":-43.3686,"RA":197.8468,"AM":5.2400,"t":"S"},{"DE":54.5563,"RA":226.5696,"AM":5.2400,"t":"S"},{"DE":-11.8377,"RA":243.4621,"AM":5.2400,"t":"S"},{"DE":-7.5979,"RA":246.9311,"AM":5.2400,"t":"S"},{"DE":20.4792,"RA":247.6398,"AM":5.2400,"t":"S"},{"DE":-44.1103,"RA":276.0760,"AM":5.2400,"t":"S"},{"DE":-58.9014,"RA":299.2762,"AM":5.2400,"t":"S"},{"DE":-14.9548,"RA":309.8180,"AM":5.2400,"t":"S"},{"DE":4.2946,"RA":314.7713,"AM":5.2400,"t":"S"},{"DE":-23.2629,"RA":325.5029,"AM":5.2400,"t":"S"},{"DE":56.8394,"RA":332.9527,"AM":5.2400,"t":"S"},{"DE":-19.6134,"RA":341.8880,"AM":5.2400,"t":"S"},{"DE":-18.2769,"RA":356.0503,"AM":5.2400,"t":"S"},{"DE":-8.1817,"RA":270.7680,"AM":5.2400,"t":"S"},{"DE":-32.3270,"RA":25.5358,"AM":5.2500,"t":"S"},{"DE":33.3589,"RA":33.9845,"AM":5.2500,"t":"S"},{"DE":-62.8065,"RA":42.2559,"AM":5.2500,"t":"S"},{"DE":-13.9274,"RA":80.8756,"AM":5.2500,"t":"S"},{"DE":-37.6967,"RA":98.0891,"AM":5.2500,"t":"S"},{"DE":-32.3397,"RA":99.4484,"AM":5.2500,"t":"S"},{"DE":10.7683,"RA":116.5675,"AM":5.2500,"t":"S"},{"DE":-32.6748,"RA":121.0675,"AM":5.2500,"t":"S"},{"DE":-8.0689,"RA":154.4075,"AM":5.2500,"t":"S"},{"DE":82.5586,"RA":157.7707,"AM":5.2500,"t":"S"},{"DE":40.3534,"RA":234.4566,"AM":5.2500,"t":"S"},{"DE":-54.5004,"RA":264.5231,"AM":5.2500,"t":"S"},{"DE":20.8336,"RA":270.5960,"AM":5.2500,"t":"S"},{"DE":17.8266,"RA":275.7043,"AM":5.2500,"t":"S"},{"DE":74.0856,"RA":281.4448,"AM":5.2500,"t":"S"},{"DE":36.1002,"RA":286.8255,"AM":5.2500,"t":"S"},{"DE":-39.4249,"RA":318.2627,"AM":5.2500,"t":"S"},{"DE":40.2254,"RA":340.3694,"AM":5.2500,"t":"S"},{"DE":67.2092,"RA":345.8869,"AM":5.2500,"t":"S"},{"DE":17.4643,"RA":42.3232,"AM":5.2600,"t":"S"},{"DE":-7.6009,"RA":46.0688,"AM":5.2600,"t":"S"},{"DE":15.0955,"RA":65.1513,"AM":5.2600,"t":"S"},{"DE":65.1404,"RA":65.1681,"AM":5.2600,"t":"S"},{"DE":6.4542,"RA":87.0010,"AM":5.2600,"t":"S"},{"DE":28.0223,"RA":98.8003,"AM":5.2600,"t":"S"},{"DE":-55.5696,"RA":138.5750,"AM":5.2600,"t":"S"},{"DE":-51.0509,"RA":139.5245,"AM":5.2600,"t":"S"},{"DE":12.4448,"RA":149.5557,"AM":5.2600,"t":"S"},{"DE":-65.8154,"RA":152.1783,"AM":5.2600,"t":"S"},{"DE":-57.2404,"RA":163.1285,"AM":5.2600,"t":"S"},{"DE":-47.6416,"RA":173.9816,"AM":5.2600,"t":"S"},{"DE":21.3527,"RA":175.1961,"AM":5.2600,"t":"S"},{"DE":-25.7139,"RA":178.6772,"AM":5.2600,"t":"S"},{"DE":-52.8115,"RA":208.0203,"AM":5.2600,"t":"S"},{"DE":49.4582,"RA":212.0722,"AM":5.2600,"t":"S"},{"DE":-46.7327,"RA":232.3511,"AM":5.2600,"t":"S"},{"DE":10.0102,"RA":234.1232,"AM":5.2600,"t":"S"},{"DE":69.1094,"RA":245.4530,"AM":5.2600,"t":"S"},{"DE":26.2304,"RA":284.9395,"AM":5.2600,"t":"S"},{"DE":63.1199,"RA":330.9706,"AM":5.2600,"t":"S"},{"DE":47.0073,"RA":22.5254,"AM":5.2700,"t":"S"},{"DE":77.2813,"RA":31.2797,"AM":5.2700,"t":"S"},{"DE":-30.7238,"RA":33.2269,"AM":5.2700,"t":"S"},{"DE":2.2672,"RA":37.8754,"AM":5.2700,"t":"S"},{"DE":-79.1094,"RA":37.9175,"AM":5.2700,"t":"S"},{"DE":21.1471,"RA":50.3068,"AM":5.2700,"t":"S"},{"DE":22.2000,"RA":66.3542,"AM":5.2700,"t":"S"},{"DE":-7.8229,"RA":94.9283,"AM":5.2700,"t":"S"},{"DE":-37.9297,"RA":101.8392,"AM":5.2700,"t":"S"},{"DE":15.8267,"RA":113.4020,"AM":5.2700,"t":"S"},{"DE":-58.2247,"RA":128.8149,"AM":5.2700,"t":"S"},{"DE":49.8198,"RA":148.9292,"AM":5.2700,"t":"S"},{"DE":-51.2330,"RA":153.3452,"AM":5.2700,"t":"S"},{"DE":-64.1723,"RA":157.2191,"AM":5.2700,"t":"S"},{"DE":55.6282,"RA":176.7317,"AM":5.2700,"t":"S"},{"DE":-63.0586,"RA":190.7095,"AM":5.2700,"t":"S"},{"DE":-12.7077,"RA":201.6799,"AM":5.2700,"t":"S"},{"DE":-24.6422,"RA":223.5839,"AM":5.2700,"t":"S"},{"DE":-78.6675,"RA":245.1119,"AM":5.2700,"t":"S"},{"DE":33.5683,"RA":255.4015,"AM":5.2700,"t":"S"},{"DE":-53.2370,"RA":255.7863,"AM":5.2700,"t":"S"},{"DE":13.6222,"RA":284.7739,"AM":5.2700,"t":"S"},{"DE":40.3651,"RA":304.2304,"AM":5.2700,"t":"S"},{"DE":-82.7189,"RA":327.7262,"AM":5.2700,"t":"S"},{"DE":62.7857,"RA":331.2520,"AM":5.2700,"t":"S"},{"DE":86.1080,"RA":333.2925,"AM":5.2700,"t":"S"},{"DE":-15.4480,"RA":355.6159,"AM":5.2700,"t":"S"},{"DE":73.0400,"RA":24.6289,"AM":5.2800,"t":"S"},{"DE":50.6954,"RA":59.1521,"AM":5.2800,"t":"S"},{"DE":-1.5497,"RA":60.3835,"AM":5.2800,"t":"S"},{"DE":-59.7327,"RA":71.0881,"AM":5.2800,"t":"S"},{"DE":20.4184,"RA":76.9517,"AM":5.2800,"t":"S"},{"DE":-28.6897,"RA":84.4359,"AM":5.2800,"t":"S"},{"DE":13.8996,"RA":86.9288,"AM":5.2800,"t":"S"},{"DE":-19.1659,"RA":91.9235,"AM":5.2800,"t":"S"},{"DE":-50.2391,"RA":97.4545,"AM":5.2800,"t":"S"},{"DE":-14.4260,"RA":101.7129,"AM":5.2800,"t":"S"},{"DE":21.7611,"RA":102.8877,"AM":5.2800,"t":"S"},{"DE":-73.4000,"RA":125.5188,"AM":5.2800,"t":"S"},{"DE":-1.8970,"RA":131.8124,"AM":5.2800,"t":"S"},{"DE":56.7414,"RA":138.9575,"AM":5.2800,"t":"S"},{"DE":-74.8943,"RA":139.3550,"AM":5.2800,"t":"S"},{"DE":40.2398,"RA":144.5907,"AM":5.2800,"t":"S"},{"DE":-45.6901,"RA":176.4332,"AM":5.2800,"t":"S"},{"DE":-19.6590,"RA":180.2132,"AM":5.2800,"t":"S"},{"DE":48.9841,"RA":184.9530,"AM":5.2800,"t":"S"},{"DE":29.1643,"RA":228.6215,"AM":5.2800,"t":"S"},{"DE":-64.0579,"RA":246.9888,"AM":5.2800,"t":"S"},{"DE":56.0155,"RA":249.5019,"AM":5.2800,"t":"S"},{"DE":-45.8430,"RA":261.7166,"AM":5.2800,"t":"S"},{"DE":-33.0166,"RA":278.4907,"AM":5.2800,"t":"S"},{"DE":11.5954,"RA":289.4542,"AM":5.2800,"t":"S"},{"DE":11.8266,"RA":295.6417,"AM":5.2800,"t":"S"},{"DE":11.4237,"RA":299.0594,"AM":5.2800,"t":"S"},{"DE":-19.1185,"RA":304.8483,"AM":5.2800,"t":"S"},{"DE":-72.2554,"RA":336.1465,"AM":5.2800,"t":"S"},{"DE":-18.6783,"RA":356.5038,"AM":5.2800,"t":"S"},{"DE":-82.2240,"RA":2.5094,"AM":5.2900,"t":"S"},{"DE":-17.9383,"RA":3.0416,"AM":5.2900,"t":"S"},{"DE":-25.0526,"RA":26.4114,"AM":5.2900,"t":"S"},{"DE":64.6216,"RA":29.9084,"AM":5.2900,"t":"S"},{"DE":28.6427,"RA":34.7375,"AM":5.2900,"t":"S"},{"DE":0.3957,"RA":35.4860,"AM":5.2900,"t":"S"},{"DE":29.6693,"RA":37.0416,"AM":5.2900,"t":"S"},{"DE":7.7160,"RA":63.3879,"AM":5.2900,"t":"S"},{"DE":31.4389,"RA":66.5263,"AM":5.2900,"t":"S"},{"DE":56.7572,"RA":72.0010,"AM":5.2900,"t":"S"},{"DE":-12.3156,"RA":79.9959,"AM":5.2900,"t":"S"},{"DE":-34.6678,"RA":85.5633,"AM":5.2900,"t":"S"},{"DE":-52.6355,"RA":88.7087,"AM":5.2900,"t":"S"},{"DE":-22.9414,"RA":103.9455,"AM":5.2900,"t":"S"},{"DE":-26.5859,"RA":109.7136,"AM":5.2900,"t":"S"},{"DE":24.3954,"RA":147.9710,"AM":5.2900,"t":"S"},{"DE":25.9129,"RA":187.2279,"AM":5.2900,"t":"S"},{"DE":10.1006,"RA":213.7119,"AM":5.2900,"t":"S"},{"DE":-20.7283,"RA":273.8038,"AM":5.2900,"t":"S"},{"DE":-87.6058,"RA":283.6984,"AM":5.2900,"t":"S"},{"DE":48.8352,"RA":321.7150,"AM":5.2900,"t":"S"},{"DE":-41.1793,"RA":323.0245,"AM":5.2900,"t":"S"},{"DE":22.9489,"RA":326.5182,"AM":5.2900,"t":"S"},{"DE":-0.9063,"RA":331.1976,"AM":5.2900,"t":"S"},{"DE":39.4587,"RA":10.2799,"AM":5.3000,"t":"S"},{"DE":-52.5431,"RA":39.3514,"AM":5.3000,"t":"S"},{"DE":27.0609,"RA":40.1711,"AM":5.3000,"t":"S"},{"DE":46.0569,"RA":53.1095,"AM":5.3000,"t":"S"},{"DE":-50.4813,"RA":70.6935,"AM":5.3000,"t":"S"},{"DE":43.3651,"RA":70.7263,"AM":5.3000,"t":"S"},{"DE":-71.3143,"RA":75.6792,"AM":5.3000,"t":"S"},{"DE":-14.7961,"RA":101.4975,"AM":5.3000,"t":"S"},{"DE":-40.4988,"RA":108.0659,"AM":5.3000,"t":"S"},{"DE":25.7842,"RA":116.0288,"AM":5.3000,"t":"S"},{"DE":2.2248,"RA":119.5861,"AM":5.3000,"t":"S"},{"DE":21.5818,"RA":121.9411,"AM":5.3000,"t":"S"},{"DE":-3.4430,"RA":132.3405,"AM":5.3000,"t":"S"},{"DE":43.2178,"RA":138.4509,"AM":5.3000,"t":"S"},{"DE":-57.9836,"RA":145.1774,"AM":5.3000,"t":"S"},{"DE":-12.8159,"RA":152.5245,"AM":5.3000,"t":"S"},{"DE":39.3370,"RA":172.2672,"AM":5.3000,"t":"S"},{"DE":-28.1428,"RA":260.8400,"AM":5.3000,"t":"S"},{"DE":24.4461,"RA":274.7945,"AM":5.3000,"t":"S"},{"DE":-16.2933,"RA":295.1808,"AM":5.3000,"t":"S"},{"DE":-34.6978,"RA":299.9639,"AM":5.3000,"t":"S"},{"DE":24.6711,"RA":304.1962,"AM":5.3000,"t":"S"},{"DE":5.3430,"RA":305.7946,"AM":5.3000,"t":"S"},{"DE":22.3259,"RA":314.5681,"AM":5.3000,"t":"S"},{"DE":4.2935,"RA":314.7687,"AM":5.3000,"t":"S"},{"DE":-21.1937,"RA":317.1401,"AM":5.3000,"t":"S"},{"DE":37.1168,"RA":321.8390,"AM":5.3000,"t":"S"},{"DE":5.6801,"RA":325.5644,"AM":5.3000,"t":"S"},{"DE":46.3872,"RA":346.9136,"AM":5.3000,"t":"S"},{"DE":-32.0731,"RA":355.1590,"AM":5.3000,"t":"S"},{"DE":10.9473,"RA":358.1546,"AM":5.3000,"t":"S"},{"DE":51.0658,"RA":33.4009,"AM":5.3100,"t":"S"},{"DE":47.3800,"RA":34.8201,"AM":5.3100,"t":"S"},{"DE":-46.5972,"RA":86.6140,"AM":5.3100,"t":"S"},{"DE":50.4338,"RA":116.0174,"AM":5.3100,"t":"S"},{"DE":-47.5208,"RA":133.4608,"AM":5.3100,"t":"S"},{"DE":-39.4015,"RA":139.2378,"AM":5.3100,"t":"S"},{"DE":13.3076,"RA":168.9663,"AM":5.3100,"t":"S"},{"DE":34.2016,"RA":175.2626,"AM":5.3100,"t":"S"},{"DE":8.2459,"RA":176.9788,"AM":5.3100,"t":"S"},{"DE":-45.7239,"RA":183.5113,"AM":5.3100,"t":"S"},{"DE":-19.9309,"RA":198.5454,"AM":5.3100,"t":"S"},{"DE":-41.8171,"RA":247.9240,"AM":5.3100,"t":"S"},{"DE":-1.0629,"RA":262.5991,"AM":5.3100,"t":"S"},{"DE":-68.4244,"RA":287.4696,"AM":5.3100,"t":"S"},{"DE":-15.1715,"RA":318.9368,"AM":5.3100,"t":"S"},{"DE":-57.7974,"RA":336.2346,"AM":5.3100,"t":"S"},{"DE":68.7786,"RA":17.6637,"AM":5.3200,"t":"S"},{"DE":-7.6855,"RA":45.6761,"AM":5.3200,"t":"S"},{"DE":49.2133,"RA":50.8050,"AM":5.3200,"t":"S"},{"DE":5.4356,"RA":60.9358,"AM":5.3200,"t":"S"},{"DE":0.9983,"RA":69.3070,"AM":5.3200,"t":"S"},{"DE":3.7669,"RA":83.5699,"AM":5.3200,"t":"S"},{"DE":-24.9122,"RA":117.2570,"AM":5.3200,"t":"S"},{"DE":-24.0462,"RA":126.2656,"AM":5.3200,"t":"S"},{"DE":10.5452,"RA":162.3143,"AM":5.3200,"t":"S"},{"DE":66.7449,"RA":175.6183,"AM":5.3200,"t":"S"},{"DE":-35.4127,"RA":185.8976,"AM":5.3200,"t":"S"},{"DE":-64.4851,"RA":201.3085,"AM":5.3200,"t":"S"},{"DE":-14.1490,"RA":222.3294,"AM":5.3200,"t":"S"},{"DE":-33.8558,"RA":223.9363,"AM":5.3200,"t":"S"},{"DE":4.9394,"RA":228.7973,"AM":5.3200,"t":"S"},{"DE":-49.5724,"RA":245.6167,"AM":5.3200,"t":"S"},{"DE":10.5852,"RA":258.1159,"AM":5.3200,"t":"S"},{"DE":-39.8744,"RA":297.9608,"AM":5.3200,"t":"S"},{"DE":-66.9440,"RA":300.4685,"AM":5.3200,"t":"S"},{"DE":-36.1012,"RA":302.7995,"AM":5.3200,"t":"S"},{"DE":-38.6314,"RA":315.7415,"AM":5.3200,"t":"S"},{"DE":-80.1238,"RA":342.5948,"AM":5.3200,"t":"S"},{"DE":21.4732,"RA":16.4206,"AM":5.3300,"t":"S"},{"DE":-44.2679,"RA":64.8195,"AM":5.3300,"t":"S"},{"DE":2.5082,"RA":73.3449,"AM":5.3300,"t":"S"},{"DE":7.7791,"RA":73.6991,"AM":5.3300,"t":"S"},{"DE":8.4984,"RA":76.9704,"AM":5.3300,"t":"S"},{"DE":-20.5543,"RA":121.8252,"AM":5.3300,"t":"S"},{"DE":-71.5149,"RA":124.9541,"AM":5.3300,"t":"S"},{"DE":-47.9289,"RA":127.2698,"AM":5.3300,"t":"S"},{"DE":18.0944,"RA":127.8989,"AM":5.3300,"t":"S"},{"DE":20.4412,"RA":128.1771,"AM":5.3300,"t":"S"},{"DE":-64.5146,"RA":161.5690,"AM":5.3300,"t":"S"},{"DE":13.6758,"RA":199.3151,"AM":5.3300,"t":"S"},{"DE":-36.6696,"RA":275.7211,"AM":5.3300,"t":"S"},{"DE":17.3609,"RA":284.5614,"AM":5.3300,"t":"S"},{"DE":-56.3626,"RA":297.0048,"AM":5.3300,"t":"S"},{"DE":17.5165,"RA":300.0138,"AM":5.3300,"t":"S"},{"DE":-21.0746,"RA":333.5751,"AM":5.3300,"t":"S"},{"DE":22.4988,"RA":353.3671,"AM":5.3300,"t":"S"},{"DE":-30.0018,"RA":30.3114,"AM":5.3400,"t":"S"},{"DE":38.3375,"RA":43.4275,"AM":5.3400,"t":"S"},{"DE":6.0500,"RA":56.4185,"AM":5.3400,"t":"S"},{"DE":21.7735,"RA":64.9029,"AM":5.3400,"t":"S"},{"DE":2.5958,"RA":79.7967,"AM":5.3400,"t":"S"},{"DE":-1.5918,"RA":83.1723,"AM":5.3400,"t":"S"},{"DE":-64.2275,"RA":83.2481,"AM":5.3400,"t":"S"},{"DE":16.1432,"RA":93.8547,"AM":5.3400,"t":"S"},{"DE":53.4522,"RA":95.4422,"AM":5.3400,"t":"S"},{"DE":39.9026,"RA":99.7049,"AM":5.3400,"t":"S"},{"DE":57.1692,"RA":101.7063,"AM":5.3400,"t":"S"},{"DE":59.4485,"RA":103.2711,"AM":5.3400,"t":"S"},{"DE":30.9609,"RA":113.7867,"AM":5.3400,"t":"S"},{"DE":68.4741,"RA":123.2033,"AM":5.3400,"t":"S"},{"DE":-66.7930,"RA":132.6447,"AM":5.3400,"t":"S"},{"DE":-80.7869,"RA":141.0402,"AM":5.3400,"t":"S"},{"DE":-38.0098,"RA":155.8722,"AM":5.3400,"t":"S"},{"DE":-68.3289,"RA":181.1622,"AM":5.3400,"t":"S"},{"DE":-48.6925,"RA":182.0613,"AM":5.3400,"t":"S"},{"DE":-56.8358,"RA":193.9881,"AM":5.3400,"t":"S"},{"DE":-24.8063,"RA":216.2026,"AM":5.3400,"t":"S"},{"DE":12.8475,"RA":235.4476,"AM":5.3400,"t":"S"},{"DE":31.7017,"RA":253.2419,"AM":5.3400,"t":"S"},{"DE":42.4125,"RA":293.6719,"AM":5.3400,"t":"S"},{"DE":-39.8099,"RA":313.4174,"AM":5.3400,"t":"S"},{"DE":17.2859,"RA":327.5362,"AM":5.3400,"t":"S"},{"DE":34.6046,"RA":333.1993,"AM":5.3400,"t":"S"},{"DE":-12.8314,"RA":334.2002,"AM":5.3400,"t":"S"},{"DE":48.6841,"RA":344.2688,"AM":5.3400,"t":"S"},{"DE":64.2475,"RA":12.6816,"AM":5.3500,"t":"S"},{"DE":-11.2665,"RA":14.0062,"AM":5.3500,"t":"S"},{"DE":19.1723,"RA":21.5636,"AM":5.3500,"t":"S"},{"DE":11.7056,"RA":71.5072,"AM":5.3500,"t":"S"},{"DE":38.4826,"RA":91.6462,"AM":5.3500,"t":"S"},{"DE":58.9357,"RA":92.4958,"AM":5.3500,"t":"S"},{"DE":-31.8089,"RA":111.1827,"AM":5.3500,"t":"S"},{"DE":49.6725,"RA":112.4830,"AM":5.3500,"t":"S"},{"DE":45.8340,"RA":130.2544,"AM":5.3500,"t":"S"},{"DE":-40.6493,"RA":143.0803,"AM":5.3500,"t":"S"},{"DE":3.5379,"RA":205.7655,"AM":5.3500,"t":"S"},{"DE":0.7153,"RA":230.2583,"AM":5.3500,"t":"S"},{"DE":43.1386,"RA":238.6577,"AM":5.3500,"t":"S"},{"DE":-26.3267,"RA":242.0316,"AM":5.3500,"t":"S"},{"DE":-46.2432,"RA":247.4264,"AM":5.3500,"t":"S"},{"DE":18.4332,"RA":253.8424,"AM":5.3500,"t":"S"},{"DE":48.5856,"RA":264.1569,"AM":5.3500,"t":"S"},{"DE":-42.7107,"RA":284.0707,"AM":5.3500,"t":"S"},{"DE":-7.9395,"RA":288.1696,"AM":5.3500,"t":"S"},{"DE":-7.8211,"RA":335.0496,"AM":5.3500,"t":"S"},{"DE":31.8125,"RA":350.4789,"AM":5.3500,"t":"S"},{"DE":50.4717,"RA":354.7847,"AM":5.3500,"t":"S"},{"DE":21.4385,"RA":9.9815,"AM":5.3600,"t":"S"},{"DE":15.4755,"RA":11.6373,"AM":5.3600,"t":"S"},{"DE":-61.7753,"RA":16.8276,"AM":5.3600,"t":"S"},{"DE":-60.3119,"RA":36.2248,"AM":5.3600,"t":"S"},{"DE":-1.0349,"RA":38.0393,"AM":5.3600,"t":"S"},{"DE":2.8269,"RA":61.0412,"AM":5.3600,"t":"S"},{"DE":53.4730,"RA":69.9919,"AM":5.3600,"t":"S"},{"DE":-1.1561,"RA":83.3810,"AM":5.3600,"t":"S"},{"DE":-7.5180,"RA":87.8416,"AM":5.3600,"t":"S"},{"DE":65.7184,"RA":93.2127,"AM":5.3600,"t":"S"},{"DE":-9.3900,"RA":94.7108,"AM":5.3600,"t":"S"},{"DE":3.1114,"RA":108.5836,"AM":5.3600,"t":"S"},{"DE":-30.6864,"RA":108.8378,"AM":5.3600,"t":"S"},{"DE":-34.1724,"RA":116.3960,"AM":5.3600,"t":"S"},{"DE":-43.5004,"RA":119.2409,"AM":5.3600,"t":"S"},{"DE":-7.7725,"RA":122.8875,"AM":5.3600,"t":"S"},{"DE":14.9415,"RA":138.8077,"AM":5.3600,"t":"S"},{"DE":14.0217,"RA":145.9329,"AM":5.3600,"t":"S"},{"DE":-59.2158,"RA":160.6690,"AM":5.3600,"t":"S"},{"DE":30.6823,"RA":161.4662,"AM":5.3600,"t":"S"},{"DE":3.6552,"RA":179.9871,"AM":5.3600,"t":"S"},{"DE":-17.7353,"RA":200.7546,"AM":5.3600,"t":"S"},{"DE":-62.8756,"RA":221.3220,"AM":5.3600,"t":"S"},{"DE":-39.7103,"RA":231.1876,"AM":5.3600,"t":"S"},{"DE":-19.3019,"RA":234.7273,"AM":5.3600,"t":"S"},{"DE":25.5376,"RA":260.0410,"AM":5.3600,"t":"S"},{"DE":-56.0234,"RA":274.2814,"AM":5.3600,"t":"S"},{"DE":-37.3432,"RA":284.1687,"AM":5.3600,"t":"S"},{"DE":80.5523,"RA":311.8897,"AM":5.3600,"t":"S"},{"DE":-53.6271,"RA":334.5643,"AM":5.3600,"t":"S"},{"DE":-18.0271,"RA":355.3937,"AM":5.3600,"t":"S"},{"DE":-5.7333,"RA":26.4969,"AM":5.3700,"t":"S"},{"DE":-49.1514,"RA":75.7029,"AM":5.3700,"t":"S"},{"DE":24.0396,"RA":83.8630,"AM":5.3700,"t":"S"},{"DE":-4.1938,"RA":91.6614,"AM":5.3700,"t":"S"},{"DE":59.9990,"RA":93.9189,"AM":5.3700,"t":"S"},{"DE":-69.6903,"RA":96.3693,"AM":5.3700,"t":"S"},{"DE":-27.8343,"RA":110.8708,"AM":5.3700,"t":"S"},{"DE":11.6695,"RA":111.2424,"AM":5.3700,"t":"S"},{"DE":73.9179,"RA":120.0490,"AM":5.3700,"t":"S"},{"DE":31.9237,"RA":150.2530,"AM":5.3700,"t":"S"},{"DE":-49.1010,"RA":168.1379,"AM":5.3700,"t":"S"},{"DE":58.4057,"RA":187.4890,"AM":5.3700,"t":"S"},{"DE":66.5973,"RA":194.9800,"AM":5.3700,"t":"S"},{"DE":-76.6627,"RA":224.4713,"AM":5.3700,"t":"S"},{"DE":59.7550,"RA":244.3139,"AM":5.3700,"t":"S"},{"DE":-39.1930,"RA":246.0053,"AM":5.3700,"t":"S"},{"DE":-24.2825,"RA":270.7129,"AM":5.3700,"t":"S"},{"DE":-32.9891,"RA":277.7702,"AM":5.3700,"t":"S"},{"DE":-22.3922,"RA":281.5859,"AM":5.3700,"t":"S"},{"DE":75.4340,"RA":281.5927,"AM":5.3700,"t":"S"},{"DE":-34.0150,"RA":332.4821,"AM":5.3700,"t":"S"},{"DE":60.7591,"RA":333.0084,"AM":5.3700,"t":"S"},{"DE":5.7895,"RA":335.1149,"AM":5.3700,"t":"S"},{"DE":-53.9649,"RA":346.1650,"AM":5.3700,"t":"S"},{"DE":8.1903,"RA":5.1494,"AM":5.3800,"t":"S"},{"DE":61.8311,"RA":6.1979,"AM":5.3800,"t":"S"},{"DE":20.2943,"RA":8.1478,"AM":5.3800,"t":"S"},{"DE":-65.4680,"RA":10.6180,"AM":5.3800,"t":"S"},{"DE":34.6876,"RA":38.9450,"AM":5.3800,"t":"S"},{"DE":-0.2689,"RA":60.6531,"AM":5.3800,"t":"S"},{"DE":-20.6396,"RA":65.1625,"AM":5.3800,"t":"S"},{"DE":25.6293,"RA":65.6456,"AM":5.3800,"t":"S"},{"DE":7.8710,"RA":69.7756,"AM":5.3800,"t":"S"},{"DE":33.7484,"RA":79.7501,"AM":5.3800,"t":"S"},{"DE":-52.0859,"RA":110.1617,"AM":5.3800,"t":"S"},{"DE":19.8840,"RA":118.9162,"AM":5.3800,"t":"S"},{"DE":-68.6896,"RA":139.3222,"AM":5.3800,"t":"S"},{"DE":-6.0712,"RA":141.9449,"AM":5.3800,"t":"S"},{"DE":-57.6761,"RA":185.7060,"AM":5.3800,"t":"S"},{"DE":-58.9918,"RA":186.8703,"AM":5.3800,"t":"S"},{"DE":83.4129,"RA":192.3074,"AM":5.3800,"t":"S"},{"DE":-58.7871,"RA":205.5046,"AM":5.3800,"t":"S"},{"DE":-49.5190,"RA":217.5873,"AM":5.3800,"t":"S"},{"DE":-52.8095,"RA":224.0718,"AM":5.3800,"t":"S"},{"DE":32.9337,"RA":230.4524,"AM":5.3800,"t":"S"},{"DE":-24.5332,"RA":238.4746,"AM":5.3800,"t":"S"},{"DE":32.4677,"RA":260.1648,"AM":5.3800,"t":"S"},{"DE":-1.9853,"RA":277.4208,"AM":5.3800,"t":"S"},{"DE":52.3535,"RA":278.4862,"AM":5.3800,"t":"S"},{"DE":9.1225,"RA":279.1160,"AM":5.3800,"t":"S"},{"DE":-5.7051,"RA":281.8706,"AM":5.3800,"t":"S"},{"DE":-45.4660,"RA":289.0906,"AM":5.3800,"t":"S"},{"DE":-10.7635,"RA":297.6949,"AM":5.3800,"t":"S"},{"DE":35.9725,"RA":301.5908,"AM":5.3800,"t":"S"},{"DE":81.4227,"RA":307.0603,"AM":5.3800,"t":"S"},{"DE":46.1558,"RA":315.2955,"AM":5.3800,"t":"S"},{"DE":-20.8519,"RA":321.0400,"AM":5.3800,"t":"S"},{"DE":50.8234,"RA":332.7910,"AM":5.3800,"t":"S"},{"DE":-46.3973,"RA":15.7050,"AM":5.3900,"t":"S"},{"DE":-27.9420,"RA":42.4757,"AM":5.3900,"t":"S"},{"DE":47.8714,"RA":58.9924,"AM":5.3900,"t":"S"},{"DE":26.4810,"RA":62.7078,"AM":5.3900,"t":"S"},{"DE":11.1461,"RA":71.1076,"AM":5.3900,"t":"S"},{"DE":-10.2633,"RA":74.9602,"AM":5.3900,"t":"S"},{"DE":9.9424,"RA":94.2776,"AM":5.3900,"t":"S"},{"DE":-51.2657,"RA":101.7195,"AM":5.3900,"t":"S"},{"DE":-15.1447,"RA":102.2406,"AM":5.3900,"t":"S"},{"DE":79.4796,"RA":121.1965,"AM":5.3900,"t":"S"},{"DE":35.1033,"RA":142.8851,"AM":5.3900,"t":"S"},{"DE":1.4078,"RA":171.0097,"AM":5.3900,"t":"S"},{"DE":-40.5866,"RA":173.4051,"AM":5.3900,"t":"S"},{"DE":-46.1334,"RA":219.3340,"AM":5.3900,"t":"S"},{"DE":44.4045,"RA":219.7093,"AM":5.3900,"t":"S"},{"DE":-1.8042,"RA":236.5235,"AM":5.3900,"t":"S"},{"DE":33.3035,"RA":240.2612,"AM":5.3900,"t":"S"},{"DE":-3.4667,"RA":242.4605,"AM":5.3900,"t":"S"},{"DE":20.9585,"RA":253.7299,"AM":5.3900,"t":"S"},{"DE":-70.1232,"RA":260.5245,"AM":5.3900,"t":"S"},{"DE":-15.8317,"RA":275.0366,"AM":5.3900,"t":"S"},{"DE":50.5335,"RA":285.0570,"AM":5.3900,"t":"S"},{"DE":29.4630,"RA":293.7122,"AM":5.3900,"t":"S"},{"DE":-72.5034,"RA":297.3554,"AM":5.3900,"t":"S"},{"DE":13.0273,"RA":308.4877,"AM":5.3900,"t":"S"},{"DE":27.6086,"RA":321.9169,"AM":5.3900,"t":"S"},{"DE":9.8221,"RA":347.5061,"AM":5.3900,"t":"S"},{"DE":-4.8366,"RA":15.7606,"AM":5.4000,"t":"S"},{"DE":-50.8003,"RA":40.6390,"AM":5.4000,"t":"S"},{"DE":70.8710,"RA":57.3071,"AM":5.4000,"t":"S"},{"DE":60.7356,"RA":65.4484,"AM":5.4000,"t":"S"},{"DE":13.7244,"RA":67.6557,"AM":5.4000,"t":"S"},{"DE":17.9622,"RA":81.7921,"AM":5.4000,"t":"S"},{"DE":30.4924,"RA":84.6587,"AM":5.4000,"t":"S"},{"DE":38.4455,"RA":99.1368,"AM":5.4000,"t":"S"},{"DE":-31.9238,"RA":110.7529,"AM":5.4000,"t":"S"},{"DE":30.5791,"RA":133.5614,"AM":5.4000,"t":"S"},{"DE":9.0568,"RA":142.1142,"AM":5.4000,"t":"S"},{"DE":45.6015,"RA":142.1666,"AM":5.4000,"t":"S"},{"DE":35.8101,"RA":143.9150,"AM":5.4000,"t":"S"},{"DE":-0.0695,"RA":168.4398,"AM":5.4000,"t":"S"},{"DE":59.9458,"RA":202.1130,"AM":5.4000,"t":"S"},{"DE":19.2269,"RA":216.6140,"AM":5.4000,"t":"S"},{"DE":-73.3896,"RA":232.8784,"AM":5.4000,"t":"S"},{"DE":33.7035,"RA":245.6217,"AM":5.4000,"t":"S"},{"DE":-29.7047,"RA":246.1657,"AM":5.4000,"t":"S"},{"DE":-39.6862,"RA":281.2382,"AM":5.4000,"t":"S"},{"DE":-3.6990,"RA":285.7271,"AM":5.4000,"t":"S"},{"DE":53.3967,"RA":286.2299,"AM":5.4000,"t":"S"},{"DE":-4.0314,"RA":286.2403,"AM":5.4000,"t":"S"},{"DE":61.9954,"RA":301.3867,"AM":5.4000,"t":"S"},{"DE":-17.9851,"RA":319.4887,"AM":5.4000,"t":"S"},{"DE":31.6012,"RA":250.3224,"AM":5.4000,"t":"S"},{"DE":10.0061,"RA":318.6209,"AM":5.4000,"t":"S"},{"DE":-27.7997,"RA":2.8934,"AM":5.4100,"t":"S"},{"DE":55.2214,"RA":11.3216,"AM":5.4100,"t":"S"},{"DE":-15.4002,"RA":23.9957,"AM":5.4100,"t":"S"},{"DE":-70.9634,"RA":102.8624,"AM":5.4100,"t":"S"},{"DE":-11.2940,"RA":106.6699,"AM":5.4100,"t":"S"},{"DE":-32.2021,"RA":110.8829,"AM":5.4100,"t":"S"},{"DE":-38.8121,"RA":112.2737,"AM":5.4100,"t":"S"},{"DE":-38.5335,"RA":115.3159,"AM":5.4100,"t":"S"},{"DE":-27.1389,"RA":189.4261,"AM":5.4100,"t":"S"},{"DE":-17.8598,"RA":206.8558,"AM":5.4100,"t":"S"},{"DE":13.0043,"RA":214.8178,"AM":5.4100,"t":"S"},{"DE":-15.6728,"RA":236.0183,"AM":5.4100,"t":"S"},{"DE":-23.9781,"RA":238.4828,"AM":5.4100,"t":"S"},{"DE":0.6650,"RA":247.1416,"AM":5.4100,"t":"S"},{"DE":35.9352,"RA":257.0086,"AM":5.4100,"t":"S"},{"DE":0.3306,"RA":262.2069,"AM":5.4100,"t":"S"},{"DE":7.2598,"RA":274.7897,"AM":5.4100,"t":"S"},{"DE":23.2852,"RA":275.5362,"AM":5.4100,"t":"S"},{"DE":33.4690,"RA":279.1556,"AM":5.4100,"t":"S"},{"DE":42.8183,"RA":294.8603,"AM":5.4100,"t":"S"},{"DE":-59.1937,"RA":297.6866,"AM":5.4100,"t":"S"},{"DE":50.3400,"RA":310.5526,"AM":5.4100,"t":"S"},{"DE":-68.7765,"RA":312.3260,"AM":5.4100,"t":"S"},{"DE":-27.6193,"RA":318.3222,"AM":5.4100,"t":"S"},{"DE":-27.9879,"RA":2.3378,"AM":5.4200,"t":"S"},{"DE":-39.9150,"RA":7.1104,"AM":5.4200,"t":"S"},{"DE":74.8476,"RA":11.9418,"AM":5.4200,"t":"S"},{"DE":-2.5004,"RA":19.1512,"AM":5.4200,"t":"S"},{"DE":-41.4925,"RA":21.1699,"AM":5.4200,"t":"S"},{"DE":40.7298,"RA":28.3223,"AM":5.4200,"t":"S"},{"DE":0.1285,"RA":30.7985,"AM":5.4200,"t":"S"},{"DE":-0.8849,"RA":35.5517,"AM":5.4200,"t":"S"},{"DE":80.8242,"RA":66.7621,"AM":5.4200,"t":"S"},{"DE":-36.2320,"RA":98.4562,"AM":5.4200,"t":"S"},{"DE":28.9709,"RA":101.1894,"AM":5.4200,"t":"S"},{"DE":-36.3384,"RA":113.4627,"AM":5.4200,"t":"S"},{"DE":-19.5775,"RA":127.8789,"AM":5.4200,"t":"S"},{"DE":29.6542,"RA":137.0002,"AM":5.4200,"t":"S"},{"DE":13.7283,"RA":154.1697,"AM":5.4200,"t":"S"},{"DE":-57.6965,"RA":176.8298,"AM":5.4200,"t":"S"},{"DE":33.2476,"RA":188.4121,"AM":5.4200,"t":"S"},{"DE":45.4403,"RA":191.2826,"AM":5.4200,"t":"S"},{"DE":-6.9005,"RA":217.1738,"AM":5.4200,"t":"S"},{"DE":-37.5660,"RA":246.1323,"AM":5.4200,"t":"S"},{"DE":-43.1859,"RA":279.8965,"AM":5.4200,"t":"S"},{"DE":11.3777,"RA":309.4547,"AM":5.4200,"t":"S"},{"DE":66.8091,"RA":321.9423,"AM":5.4200,"t":"S"},{"DE":2.1279,"RA":347.1705,"AM":5.4200,"t":"S"},{"DE":-20.8245,"RA":29.9425,"AM":5.4300,"t":"S"},{"DE":-8.5239,"RA":30.1118,"AM":5.4300,"t":"S"},{"DE":-10.7775,"RA":35.5064,"AM":5.4300,"t":"S"},{"DE":44.2970,"RA":41.0215,"AM":5.4300,"t":"S"},{"DE":9.8296,"RA":77.3318,"AM":5.4300,"t":"S"},{"DE":63.0672,"RA":82.5425,"AM":5.4300,"t":"S"},{"DE":-8.1582,"RA":97.9586,"AM":5.4300,"t":"S"},{"DE":-45.9125,"RA":131.6273,"AM":5.4300,"t":"S"},{"DE":-85.6632,"RA":134.1742,"AM":5.4300,"t":"S"},{"DE":-76.7761,"RA":146.5853,"AM":5.4300,"t":"S"},{"DE":14.1373,"RA":158.0491,"AM":5.4300,"t":"S"},{"DE":-35.8047,"RA":166.2258,"AM":5.4300,"t":"S"},{"DE":-28.0807,"RA":167.1834,"AM":5.4300,"t":"S"},{"DE":66.7903,"RA":191.8931,"AM":5.4300,"t":"S"},{"DE":-60.4963,"RA":229.7048,"AM":5.4300,"t":"S"},{"DE":-52.3727,"RA":234.7062,"AM":5.4300,"t":"S"},{"DE":37.9470,"RA":238.9483,"AM":5.4300,"t":"S"},{"DE":-24.8315,"RA":239.6453,"AM":5.4300,"t":"S"},{"DE":-8.5476,"RA":243.0305,"AM":5.4300,"t":"S"},{"DE":-10.5233,"RA":257.4498,"AM":5.4300,"t":"S"},{"DE":72.0051,"RA":268.7964,"AM":5.4300,"t":"S"},{"DE":6.6718,"RA":279.1628,"AM":5.4300,"t":"S"},{"DE":21.4251,"RA":283.0684,"AM":5.4300,"t":"S"},{"DE":-28.4537,"RA":330.2093,"AM":5.4300,"t":"S"},{"DE":-11.5649,"RA":332.6562,"AM":5.4300,"t":"S"},{"DE":55.9028,"RA":342.4428,"AM":5.4300,"t":"S"},{"DE":-39.1568,"RA":342.7590,"AM":5.4300,"t":"S"},{"DE":0.9629,"RA":344.8644,"AM":5.4300,"t":"S"},{"DE":62.2145,"RA":357.2091,"AM":5.4300,"t":"S"},{"DE":28.9922,"RA":14.4590,"AM":5.4400,"t":"S"},{"DE":-23.8622,"RA":44.3490,"AM":5.4400,"t":"S"},{"DE":77.7347,"RA":50.0817,"AM":5.4400,"t":"S"},{"DE":23.4213,"RA":57.0867,"AM":5.4400,"t":"S"},{"DE":-6.9239,"RA":62.5938,"AM":5.4400,"t":"S"},{"DE":73.9467,"RA":78.0936,"AM":5.4400,"t":"S"},{"DE":-50.6060,"RA":79.8422,"AM":5.4400,"t":"S"},{"DE":-32.6292,"RA":84.9577,"AM":5.4400,"t":"S"},{"DE":12.5511,"RA":93.9373,"AM":5.4400,"t":"S"},{"DE":79.5648,"RA":101.5601,"AM":5.4400,"t":"S"},{"DE":-1.1270,"RA":103.6028,"AM":5.4400,"t":"S"},{"DE":-0.3019,"RA":107.8484,"AM":5.4400,"t":"S"},{"DE":-36.3638,"RA":118.2646,"AM":5.4400,"t":"S"},{"DE":11.6260,"RA":133.9815,"AM":5.4400,"t":"S"},{"DE":32.9104,"RA":134.2358,"AM":5.4400,"t":"S"},{"DE":-53.6685,"RA":144.3028,"AM":5.4400,"t":"S"},{"DE":-17.2969,"RA":161.7169,"AM":5.4400,"t":"S"},{"DE":-56.3173,"RA":179.5635,"AM":5.4400,"t":"S"},{"DE":-65.3060,"RA":197.0298,"AM":5.4400,"t":"S"},{"DE":-44.3968,"RA":234.0505,"AM":5.4400,"t":"S"},{"DE":67.8101,"RA":241.5821,"AM":5.4400,"t":"S"},{"DE":-42.6740,"RA":244.8235,"AM":5.4400,"t":"S"},{"DE":-4.0818,"RA":269.1989,"AM":5.4400,"t":"S"},{"DE":-48.1172,"RA":276.7250,"AM":5.4400,"t":"S"},{"DE":-1.0093,"RA":303.3078,"AM":5.4400,"t":"S"},{"DE":49.2203,"RA":307.8284,"AM":5.4400,"t":"S"},{"DE":-7.6938,"RA":346.2908,"AM":5.4400,"t":"S"},{"DE":48.6253,"RA":349.8742,"AM":5.4400,"t":"S"},{"DE":35.3995,"RA":9.3384,"AM":5.4500,"t":"S"},{"DE":49.3546,"RA":9.7912,"AM":5.4500,"t":"S"},{"DE":-69.5271,"RA":13.7513,"AM":5.4500,"t":"S"},{"DE":21.9614,"RA":39.7041,"AM":5.4500,"t":"S"},{"DE":25.2552,"RA":46.3612,"AM":5.4500,"t":"S"},{"DE":24.2895,"RA":56.2009,"AM":5.4500,"t":"S"},{"DE":8.1973,"RA":60.9858,"AM":5.4500,"t":"S"},{"DE":-16.3859,"RA":62.3243,"AM":5.4500,"t":"S"},{"DE":-62.1918,"RA":63.7023,"AM":5.4500,"t":"S"},{"DE":12.1976,"RA":70.0142,"AM":5.4500,"t":"S"},{"DE":-38.5134,"RA":83.2142,"AM":5.4500,"t":"S"},{"DE":-79.4202,"RA":104.1437,"AM":5.4500,"t":"S"},{"DE":-24.6308,"RA":104.3913,"AM":5.4500,"t":"S"},{"DE":17.0860,"RA":112.9517,"AM":5.4500,"t":"S"},{"DE":-42.1531,"RA":126.4663,"AM":5.4500,"t":"S"},{"DE":-62.8535,"RA":129.3285,"AM":5.4500,"t":"S"},{"DE":-53.4398,"RA":129.8494,"AM":5.4500,"t":"S"},{"DE":24.4529,"RA":135.6844,"AM":5.4500,"t":"S"},{"DE":-51.5172,"RA":142.5213,"AM":5.4500,"t":"S"},{"DE":-2.1292,"RA":163.4321,"AM":5.4500,"t":"S"},{"DE":-23.6024,"RA":182.7660,"AM":5.4500,"t":"S"},{"DE":-39.0412,"RA":187.0936,"AM":5.4500,"t":"S"},{"DE":-85.1234,"RA":193.7433,"AM":5.4500,"t":"S"},{"DE":-32.6433,"RA":225.7470,"AM":5.4500,"t":"S"},{"DE":-55.3460,"RA":227.8166,"AM":5.4500,"t":"S"},{"DE":20.3110,"RA":238.6442,"AM":5.4500,"t":"S"},{"DE":-53.8111,"RA":244.1803,"AM":5.4500,"t":"S"},{"DE":-44.2065,"RA":273.9726,"AM":5.4500,"t":"S"},{"DE":-23.9625,"RA":291.3736,"AM":5.4500,"t":"S"},{"DE":-4.6476,"RA":294.4471,"AM":5.4500,"t":"S"},{"DE":-88.9565,"RA":317.1918,"AM":5.4500,"t":"S"},{"DE":-37.2537,"RA":329.0949,"AM":5.4500,"t":"S"},{"DE":-27.7669,"RA":333.5781,"AM":5.4500,"t":"S"},{"DE":78.8243,"RA":337.4707,"AM":5.4500,"t":"S"},{"DE":20.7688,"RA":344.3666,"AM":5.4500,"t":"S"},{"DE":23.6283,"RA":13.7421,"AM":5.4600,"t":"S"},{"DE":24.1060,"RA":61.0903,"AM":5.4600,"t":"S"},{"DE":50.0487,"RA":64.8051,"AM":5.4600,"t":"S"},{"DE":-14.3592,"RA":69.8321,"AM":5.4600,"t":"S"},{"DE":41.0862,"RA":80.0611,"AM":5.4600,"t":"S"},{"DE":-47.0777,"RA":82.5395,"AM":5.4600,"t":"S"},{"DE":3.2921,"RA":82.8105,"AM":5.4600,"t":"S"},{"DE":49.8263,"RA":86.4752,"AM":5.4600,"t":"S"},{"DE":-79.3614,"RA":87.5700,"AM":5.4600,"t":"S"},{"DE":-23.1108,"RA":91.6337,"AM":5.4600,"t":"S"},{"DE":-27.4915,"RA":107.5805,"AM":5.4600,"t":"S"},{"DE":51.4287,"RA":108.3475,"AM":5.4600,"t":"S"},{"DE":-15.5857,"RA":109.0607,"AM":5.4600,"t":"S"},{"DE":-78.9634,"RA":130.3316,"AM":5.4600,"t":"S"},{"DE":-71.6019,"RA":141.7768,"AM":5.4600,"t":"S"},{"DE":-73.0809,"RA":142.9013,"AM":5.4600,"t":"S"},{"DE":-80.4696,"RA":161.3182,"AM":5.4600,"t":"S"},{"DE":61.0825,"RA":173.0865,"AM":5.4600,"t":"S"},{"DE":-47.7473,"RA":174.3917,"AM":5.4600,"t":"S"},{"DE":-28.3240,"RA":191.0022,"AM":5.4600,"t":"S"},{"DE":-42.9157,"RA":193.8310,"AM":5.4600,"t":"S"},{"DE":52.9212,"RA":204.8771,"AM":5.4600,"t":"S"},{"DE":-50.3207,"RA":206.9108,"AM":5.4600,"t":"S"},{"DE":-9.3135,"RA":211.6784,"AM":5.4600,"t":"S"},{"DE":34.3360,"RA":231.5725,"AM":5.4600,"t":"S"},{"DE":-36.7676,"RA":231.8256,"AM":5.4600,"t":"S"},{"DE":5.0211,"RA":243.3143,"AM":5.4600,"t":"S"},{"DE":-42.8589,"RA":249.0940,"AM":5.4600,"t":"S"},{"DE":-41.8064,"RA":253.5077,"AM":5.4600,"t":"S"},{"DE":-43.6800,"RA":282.2104,"AM":5.4600,"t":"S"},{"DE":41.6027,"RA":283.7174,"AM":5.4600,"t":"S"},{"DE":23.0255,"RA":289.4318,"AM":5.4600,"t":"S"},{"DE":-0.8922,"RA":290.1487,"AM":5.4600,"t":"S"},{"DE":-26.9856,"RA":292.4674,"AM":5.4600,"t":"S"},{"DE":-14.3018,"RA":294.3934,"AM":5.4600,"t":"S"},{"DE":40.3678,"RA":299.3078,"AM":5.4600,"t":"S"},{"DE":19.3186,"RA":324.4393,"AM":5.4600,"t":"S"},{"DE":-24.0058,"RA":13.1693,"AM":5.4700,"t":"S"},{"DE":47.2207,"RA":44.9575,"AM":5.4700,"t":"S"},{"DE":48.0235,"RA":53.0358,"AM":5.4700,"t":"S"},{"DE":83.3404,"RA":67.5024,"AM":5.4700,"t":"S"},{"DE":15.6919,"RA":67.6620,"AM":5.4700,"t":"S"},{"DE":63.5054,"RA":73.0216,"AM":5.4700,"t":"S"},{"DE":-74.9369,"RA":73.7965,"AM":5.4700,"t":"S"},{"DE":25.1502,"RA":82.3187,"AM":5.4700,"t":"S"},{"DE":17.7291,"RA":86.8591,"AM":5.4700,"t":"S"},{"DE":15.9307,"RA":107.0918,"AM":5.4700,"t":"S"},{"DE":47.5646,"RA":118.6780,"AM":5.4700,"t":"S"},{"DE":65.1452,"RA":128.6507,"AM":5.4700,"t":"S"},{"DE":-40.3202,"RA":132.4132,"AM":5.4700,"t":"S"},{"DE":-8.7876,"RA":137.3982,"AM":5.4700,"t":"S"},{"DE":-58.7333,"RA":159.3628,"AM":5.4700,"t":"S"},{"DE":45.5263,"RA":165.0613,"AM":5.4700,"t":"S"},{"DE":75.1606,"RA":184.7085,"AM":5.4700,"t":"S"},{"DE":24.1089,"RA":187.3627,"AM":5.4700,"t":"S"},{"DE":24.5672,"RA":187.7523,"AM":5.4700,"t":"S"},{"DE":-52.7478,"RA":200.1576,"AM":5.4700,"t":"S"},{"DE":-27.4298,"RA":210.5949,"AM":5.4700,"t":"S"},{"DE":37.2720,"RA":222.6237,"AM":5.4700,"t":"S"},{"DE":-16.5333,"RA":240.0817,"AM":5.4700,"t":"S"},{"DE":-46.6362,"RA":259.7648,"AM":5.4700,"t":"S"},{"DE":26.0500,"RA":268.8549,"AM":5.4700,"t":"S"},{"DE":-62.0022,"RA":272.6092,"AM":5.4700,"t":"S"},{"DE":-41.3361,"RA":273.3029,"AM":5.4700,"t":"S"},{"DE":-75.0443,"RA":275.9018,"AM":5.4700,"t":"S"},{"DE":-14.8657,"RA":278.1805,"AM":5.4700,"t":"S"},{"DE":30.5542,"RA":278.2081,"AM":5.4700,"t":"S"},{"DE":-33.4318,"RA":310.0826,"AM":5.4700,"t":"S"},{"DE":33.4379,"RA":313.4746,"AM":5.4700,"t":"S"},{"DE":-69.5054,"RA":322.1868,"AM":5.4700,"t":"S"},{"DE":70.7709,"RA":336.5033,"AM":5.4700,"t":"S"},{"DE":-39.1318,"RA":337.1634,"AM":5.4700,"t":"S"},{"DE":10.6106,"RA":36.2044,"AM":5.4800,"t":"S"},{"DE":-35.6758,"RA":42.6684,"AM":5.4800,"t":"S"},{"DE":-5.3613,"RA":58.1736,"AM":5.4800,"t":"S"},{"DE":-13.5198,"RA":79.4177,"AM":5.4800,"t":"S"},{"DE":-11.7732,"RA":95.3530,"AM":5.4800,"t":"S"},{"DE":-12.1927,"RA":116.9863,"AM":5.4800,"t":"S"},{"DE":-35.8773,"RA":118.5459,"AM":5.4800,"t":"S"},{"DE":-48.0991,"RA":130.5675,"AM":5.4800,"t":"S"},{"DE":48.5303,"RA":136.3504,"AM":5.4800,"t":"S"},{"DE":-13.2019,"RA":174.6667,"AM":5.4800,"t":"S"},{"DE":-9.4521,"RA":188.4448,"AM":5.4800,"t":"S"},{"DE":59.2940,"RA":222.8604,"AM":5.4800,"t":"S"},{"DE":-11.4097,"RA":224.1921,"AM":5.4800,"t":"S"},{"DE":52.3609,"RA":235.7116,"AM":5.4800,"t":"S"},{"DE":75.8776,"RA":242.7064,"AM":5.4800,"t":"S"},{"DE":39.7086,"RA":244.9799,"AM":5.4800,"t":"S"},{"DE":-39.3770,"RA":251.6998,"AM":5.4800,"t":"S"},{"DE":7.2477,"RA":252.5808,"AM":5.4800,"t":"S"},{"DE":-33.2595,"RA":254.2966,"AM":5.4800,"t":"S"},{"DE":-39.1993,"RA":311.5836,"AM":5.4800,"t":"S"},{"DE":45.1817,"RA":313.3274,"AM":5.4800,"t":"S"},{"DE":-12.8781,"RA":321.0479,"AM":5.4800,"t":"S"},{"DE":-3.5567,"RA":321.3207,"AM":5.4800,"t":"S"},{"DE":-22.5221,"RA":11.5489,"AM":5.4900,"t":"S"},{"DE":-36.8652,"RA":23.2335,"AM":5.4900,"t":"S"},{"DE":-50.8163,"RA":26.5248,"AM":5.4900,"t":"S"},{"DE":79.4185,"RA":46.5330,"AM":5.4900,"t":"S"},{"DE":44.0250,"RA":49.4473,"AM":5.4900,"t":"S"},{"DE":35.0809,"RA":59.1195,"AM":5.4900,"t":"S"},{"DE":-16.9345,"RA":71.9012,"AM":5.4900,"t":"S"},{"DE":-14.4837,"RA":87.4023,"AM":5.4900,"t":"S"},{"DE":-22.4274,"RA":92.2411,"AM":5.4900,"t":"S"},{"DE":-6.7725,"RA":116.5091,"AM":5.4900,"t":"S"},{"DE":-53.1001,"RA":130.5792,"AM":5.4900,"t":"S"},{"DE":-8.7448,"RA":139.1724,"AM":5.4900,"t":"S"},{"DE":-26.5896,"RA":142.4771,"AM":5.4900,"t":"S"},{"DE":29.3105,"RA":154.0602,"AM":5.4900,"t":"S"},{"DE":14.1946,"RA":161.6053,"AM":5.4900,"t":"S"},{"DE":-59.4239,"RA":187.9181,"AM":5.4900,"t":"S"},{"DE":21.0626,"RA":189.7805,"AM":5.4900,"t":"S"},{"DE":-8.3694,"RA":243.9053,"AM":5.4900,"t":"S"},{"DE":36.4013,"RA":272.0094,"AM":5.4900,"t":"S"},{"DE":-21.7132,"RA":273.5662,"AM":5.4900,"t":"S"},{"DE":-24.0323,"RA":278.4729,"AM":5.4900,"t":"S"},{"DE":-31.0471,"RA":286.1044,"AM":5.4900,"t":"S"},{"DE":-15.4701,"RA":295.8897,"AM":5.4900,"t":"S"},{"DE":-9.6975,"RA":314.2251,"AM":5.4900,"t":"S"},{"DE":-77.5116,"RA":334.4611,"AM":5.4900,"t":"S"},{"DE":18.4007,"RA":354.4867,"AM":5.4900,"t":"S"},{"DE":-2.7616,"RA":356.9856,"AM":5.4900,"t":"S"},{"DE":-69.6249,"RA":5.1627,"AM":5.5000,"t":"S"},{"DE":-31.5520,"RA":15.6101,"AM":5.5000,"t":"S"},{"DE":31.8043,"RA":15.7046,"AM":5.5000,"t":"S"},{"DE":19.2404,"RA":21.6736,"AM":5.5000,"t":"S"},{"DE":33.2841,"RA":30.7415,"AM":5.5000,"t":"S"},{"DE":-23.6351,"RA":50.3500,"AM":5.5000,"t":"S"},{"DE":24.7241,"RA":51.0770,"AM":5.5000,"t":"S"},{"DE":21.1423,"RA":64.8587,"AM":5.5000,"t":"S"},{"DE":-5.1714,"RA":74.1008,"AM":5.5000,"t":"S"},{"DE":24.2652,"RA":77.0276,"AM":5.5000,"t":"S"},{"DE":5.1562,"RA":78.6835,"AM":5.5000,"t":"S"},{"DE":17.0581,"RA":83.0589,"AM":5.5000,"t":"S"},{"DE":-42.1540,"RA":91.9703,"AM":5.5000,"t":"S"},{"DE":-59.1781,"RA":105.8129,"AM":5.5000,"t":"S"},{"DE":-52.3115,"RA":110.0893,"AM":5.5000,"t":"S"},{"DE":56.8118,"RA":149.9654,"AM":5.5000,"t":"S"},{"DE":-39.5626,"RA":158.8036,"AM":5.5000,"t":"S"},{"DE":18.8915,"RA":161.6023,"AM":5.5000,"t":"S"},{"DE":-49.1365,"RA":173.7371,"AM":5.5000,"t":"S"},{"DE":71.2423,"RA":204.2960,"AM":5.5000,"t":"S"},{"DE":-12.4265,"RA":206.4847,"AM":5.5000,"t":"S"},{"DE":-19.6705,"RA":233.1529,"AM":5.5000,"t":"S"},{"DE":-1.1864,"RA":233.2414,"AM":5.5000,"t":"S"},{"DE":-33.5458,"RA":242.4691,"AM":5.5000,"t":"S"},{"DE":-70.9881,"RA":248.5807,"AM":5.5000,"t":"S"},{"DE":-65.4954,"RA":248.9366,"AM":5.5000,"t":"S"},{"DE":3.3243,"RA":272.6679,"AM":5.5000,"t":"S"},{"DE":25.7719,"RA":295.9289,"AM":5.5000,"t":"S"},{"DE":24.4461,"RA":305.5143,"AM":5.5000,"t":"S"},{"DE":-42.5479,"RA":321.7568,"AM":5.5000,"t":"S"},{"DE":-38.3951,"RA":329.8246,"AM":5.5000,"t":"S"},{"DE":-87.4822,"RA":352.0149,"AM":5.5000,"t":"S"},{"DE":-48.0009,"RA":8.9215,"AM":5.5100,"t":"S"},{"DE":11.9738,"RA":11.7561,"AM":5.5100,"t":"S"},{"DE":5.6498,"RA":17.0925,"AM":5.5100,"t":"S"},{"DE":-13.0565,"RA":21.7149,"AM":5.5100,"t":"S"},{"DE":-6.4221,"RA":34.2460,"AM":5.5100,"t":"S"},{"DE":-71.9025,"RA":45.5642,"AM":5.5100,"t":"S"},{"DE":-77.3885,"RA":48.9893,"AM":5.5100,"t":"S"},{"DE":19.6092,"RA":62.2915,"AM":5.5100,"t":"S"},{"DE":83.8078,"RA":67.0554,"AM":5.5100,"t":"S"},{"DE":17.1537,"RA":74.3431,"AM":5.5100,"t":"S"},{"DE":-19.9670,"RA":94.5572,"AM":5.5100,"t":"S"},{"DE":-70.0935,"RA":126.8199,"AM":5.5100,"t":"S"},{"DE":-43.1909,"RA":144.5060,"AM":5.5100,"t":"S"},{"DE":-65.1002,"RA":160.0477,"AM":5.5100,"t":"S"},{"DE":26.3256,"RA":160.7579,"AM":5.5100,"t":"S"},{"DE":-11.3035,"RA":165.8120,"AM":5.5100,"t":"S"},{"DE":-41.2316,"RA":182.2275,"AM":5.5100,"t":"S"},{"DE":38.5427,"RA":206.7492,"AM":5.5100,"t":"S"},{"DE":-45.3214,"RA":217.5360,"AM":5.5100,"t":"S"},{"DE":-0.1676,"RA":224.3885,"AM":5.5100,"t":"S"},{"DE":29.6162,"RA":230.0357,"AM":5.5100,"t":"S"},{"DE":1.2159,"RA":252.8539,"AM":5.5100,"t":"S"},{"DE":46.2408,"RA":260.0880,"AM":5.5100,"t":"S"},{"DE":29.3221,"RA":267.5954,"AM":5.5100,"t":"S"},{"DE":52.9751,"RA":282.8957,"AM":5.5100,"t":"S"},{"DE":-46.5951,"RA":283.1134,"AM":5.5100,"t":"S"},{"DE":-12.8405,"RA":284.8492,"AM":5.5100,"t":"S"},{"DE":55.6583,"RA":285.1811,"AM":5.5100,"t":"S"},{"DE":-12.2826,"RA":288.3147,"AM":5.5100,"t":"S"},{"DE":-31.9086,"RA":296.5051,"AM":5.5100,"t":"S"},{"DE":30.9837,"RA":299.6582,"AM":5.5100,"t":"S"},{"DE":7.2780,"RA":301.0346,"AM":5.5100,"t":"S"},{"DE":26.9042,"RA":302.6397,"AM":5.5100,"t":"S"},{"DE":26.8090,"RA":302.9499,"AM":5.5100,"t":"S"},{"DE":10.8393,"RA":314.6081,"AM":5.5100,"t":"S"},{"DE":58.6235,"RA":319.8154,"AM":5.5100,"t":"S"},{"DE":41.1550,"RA":325.7770,"AM":5.5100,"t":"S"},{"DE":4.4317,"RA":337.4914,"AM":5.5100,"t":"S"},{"DE":-29.4623,"RA":344.8990,"AM":5.5100,"t":"S"},{"DE":-53.7408,"RA":25.6219,"AM":5.5200,"t":"S"},{"DE":15.0821,"RA":42.8733,"AM":5.5200,"t":"S"},{"DE":-30.1679,"RA":56.9835,"AM":5.5200,"t":"S"},{"DE":38.0397,"RA":62.1525,"AM":5.5200,"t":"S"},{"DE":55.2591,"RA":73.7631,"AM":5.5200,"t":"S"},{"DE":11.3414,"RA":79.0172,"AM":5.5200,"t":"S"},{"DE":15.8741,"RA":81.9400,"AM":5.5200,"t":"S"},{"DE":-31.3824,"RA":89.0873,"AM":5.5200,"t":"S"},{"DE":-5.2111,"RA":99.1472,"AM":5.5200,"t":"S"},{"DE":-41.3098,"RA":120.6866,"AM":5.5200,"t":"S"},{"DE":-53.1079,"RA":121.2654,"AM":5.5200,"t":"S"},{"DE":-50.1961,"RA":123.3927,"AM":5.5200,"t":"S"},{"DE":53.2197,"RA":125.9521,"AM":5.5200,"t":"S"},{"DE":-12.5346,"RA":126.6748,"AM":5.5200,"t":"S"},{"DE":-28.9920,"RA":154.5316,"AM":5.5200,"t":"S"},{"DE":33.7185,"RA":156.0359,"AM":5.5200,"t":"S"},{"DE":84.2520,"RA":157.4256,"AM":5.5200,"t":"S"},{"DE":1.9555,"RA":166.7259,"AM":5.5200,"t":"S"},{"DE":26.6195,"RA":185.0820,"AM":5.5200,"t":"S"},{"DE":-15.3630,"RA":203.2152,"AM":5.5200,"t":"S"},{"DE":-2.7549,"RA":225.3326,"AM":5.5200,"t":"S"},{"DE":35.2058,"RA":225.7752,"AM":5.5200,"t":"S"},{"DE":-22.3994,"RA":229.0959,"AM":5.5200,"t":"S"},{"DE":20.0810,"RA":261.7047,"AM":5.5200,"t":"S"},{"DE":-17.1542,"RA":271.9514,"AM":5.5200,"t":"S"},{"DE":-36.2380,"RA":275.8701,"AM":5.5200,"t":"S"},{"DE":-66.6610,"RA":289.3009,"AM":5.5200,"t":"S"},{"DE":-37.9133,"RA":312.7532,"AM":5.5200,"t":"S"},{"DE":-69.6294,"RA":327.6967,"AM":5.5200,"t":"S"},{"DE":28.7935,"RA":328.1247,"AM":5.5200,"t":"S"},{"DE":70.1326,"RA":332.6619,"AM":5.5200,"t":"S"},{"DE":65.1323,"RA":336.7721,"AM":5.5200,"t":"S"},{"DE":-46.5473,"RA":341.4200,"AM":5.5200,"t":"S"},{"DE":-50.3374,"RA":0.3338,"AM":5.5300,"t":"S"},{"DE":55.1474,"RA":27.9971,"AM":5.5300,"t":"S"},{"DE":-7.8316,"RA":39.0002,"AM":5.5300,"t":"S"},{"DE":-62.5753,"RA":49.4385,"AM":5.5300,"t":"S"},{"DE":-5.2107,"RA":55.1597,"AM":5.5300,"t":"S"},{"DE":22.9963,"RA":66.8227,"AM":5.5300,"t":"S"},{"DE":1.3808,"RA":67.1338,"AM":5.5300,"t":"S"},{"DE":-70.9310,"RA":70.7665,"AM":5.5300,"t":"S"},{"DE":-18.6666,"RA":71.0332,"AM":5.5300,"t":"S"},{"DE":-20.8637,"RA":82.7818,"AM":5.5300,"t":"S"},{"DE":17.0403,"RA":84.2656,"AM":5.5300,"t":"S"},{"DE":56.2851,"RA":96.6077,"AM":5.5300,"t":"S"},{"DE":-13.7992,"RA":122.6660,"AM":5.5300,"t":"S"},{"DE":-82.2147,"RA":150.1829,"AM":5.5300,"t":"S"},{"DE":15.6468,"RA":178.9189,"AM":5.5300,"t":"S"},{"DE":22.6162,"RA":196.5942,"AM":5.5300,"t":"S"},{"DE":-35.6642,"RA":208.3866,"AM":5.5300,"t":"S"},{"DE":-53.6657,"RA":213.3184,"AM":5.5300,"t":"S"},{"DE":12.9594,"RA":213.5216,"AM":5.5300,"t":"S"},{"DE":-18.2007,"RA":213.8504,"AM":5.5300,"t":"S"},{"DE":-16.8528,"RA":233.2301,"AM":5.5300,"t":"S"},{"DE":-3.8185,"RA":237.2367,"AM":5.5300,"t":"S"},{"DE":-8.4114,"RA":240.1985,"AM":5.5300,"t":"S"},{"DE":-30.9067,"RA":244.8864,"AM":5.5300,"t":"S"},{"DE":37.3941,"RA":246.3507,"AM":5.5300,"t":"S"},{"DE":52.9000,"RA":249.0476,"AM":5.5300,"t":"S"},{"DE":-50.6412,"RA":254.5748,"AM":5.5300,"t":"S"},{"DE":-32.6628,"RA":259.2652,"AM":5.5300,"t":"S"},{"DE":-36.9456,"RA":265.7129,"AM":5.5300,"t":"S"},{"DE":-30.7287,"RA":272.5242,"AM":5.5300,"t":"S"},{"DE":28.6286,"RA":286.6572,"AM":5.5300,"t":"S"},{"DE":12.3747,"RA":289.9140,"AM":5.5300,"t":"S"},{"DE":32.3073,"RA":310.2606,"AM":5.5300,"t":"S"},{"DE":-5.8231,"RA":316.0197,"AM":5.5300,"t":"S"},{"DE":60.4594,"RA":322.7471,"AM":5.5300,"t":"S"},{"DE":60.6927,"RA":326.8554,"AM":5.5300,"t":"S"},{"DE":45.4406,"RA":333.4551,"AM":5.5300,"t":"S"},{"DE":-24.7627,"RA":335.8785,"AM":5.5300,"t":"S"},{"DE":-16.2720,"RA":343.6895,"AM":5.5300,"t":"S"},{"DE":-68.8202,"RA":346.2174,"AM":5.5300,"t":"S"},{"DE":-52.7216,"RA":351.6524,"AM":5.5300,"t":"S"},{"DE":11.1458,"RA":2.5092,"AM":5.5400,"t":"S"},{"DE":12.1415,"RA":24.2746,"AM":5.5400,"t":"S"},{"DE":41.0293,"RA":80.7097,"AM":5.5400,"t":"S"},{"DE":14.3056,"RA":87.6204,"AM":5.5400,"t":"S"},{"DE":-33.9118,"RA":90.3179,"AM":5.5400,"t":"S"},{"DE":-40.3538,"RA":92.5434,"AM":5.5400,"t":"S"},{"DE":-37.7374,"RA":94.2551,"AM":5.5400,"t":"S"},{"DE":55.7042,"RA":102.0511,"AM":5.5400,"t":"S"},{"DE":47.2400,"RA":108.9589,"AM":5.5400,"t":"S"},{"DE":-79.0942,"RA":111.4091,"AM":5.5400,"t":"S"},{"DE":-59.4139,"RA":138.2318,"AM":5.5400,"t":"S"},{"DE":18.4098,"RA":172.6210,"AM":5.5400,"t":"S"},{"DE":-43.0957,"RA":175.3325,"AM":5.5400,"t":"S"},{"DE":-10.4460,"RA":180.1852,"AM":5.5400,"t":"S"},{"DE":57.8641,"RA":185.2119,"AM":5.5400,"t":"S"},{"DE":-5.8249,"RA":230.2817,"AM":5.5400,"t":"S"},{"DE":-65.4423,"RA":236.9712,"AM":5.5400,"t":"S"},{"DE":14.4145,"RA":239.3107,"AM":5.5400,"t":"S"},{"DE":62.8743,"RA":258.1357,"AM":5.5400,"t":"S"},{"DE":-11.2420,"RA":263.6931,"AM":5.5400,"t":"S"},{"DE":15.9524,"RA":265.4943,"AM":5.5400,"t":"S"},{"DE":24.9922,"RA":298.0066,"AM":5.5400,"t":"S"},{"DE":16.7892,"RA":299.4394,"AM":5.5400,"t":"S"},{"DE":12.5686,"RA":313.9107,"AM":5.5400,"t":"S"},{"DE":59.4386,"RA":314.8557,"AM":5.5400,"t":"S"},{"DE":12.0765,"RA":329.2349,"AM":5.5400,"t":"S"},{"DE":-40.8244,"RA":349.5411,"AM":5.5400,"t":"S"},{"DE":13.3963,"RA":1.4248,"AM":5.5500,"t":"S"},{"DE":-29.5583,"RA":8.4210,"AM":5.5500,"t":"S"},{"DE":27.7103,"RA":12.4715,"AM":5.5500,"t":"S"},{"DE":21.4654,"RA":16.4238,"AM":5.5500,"t":"S"},{"DE":57.9776,"RA":24.5315,"AM":5.5500,"t":"S"},{"DE":31.8013,"RA":36.8657,"AM":5.5500,"t":"S"},{"DE":6.6609,"RA":48.1099,"AM":5.5500,"t":"S"},{"DE":27.6076,"RA":50.5495,"AM":5.5500,"t":"S"},{"DE":3.0569,"RA":54.9630,"AM":5.5500,"t":"S"},{"DE":37.5802,"RA":55.2827,"AM":5.5500,"t":"S"},{"DE":50.9209,"RA":65.0480,"AM":5.5500,"t":"S"},{"DE":42.7921,"RA":79.5654,"AM":5.5500,"t":"S"},{"DE":-39.9579,"RA":88.7187,"AM":5.5500,"t":"S"},{"DE":-34.1441,"RA":95.1510,"AM":5.5500,"t":"S"},{"DE":-0.2760,"RA":96.8150,"AM":5.5500,"t":"S"},{"DE":2.9083,"RA":96.8352,"AM":5.5500,"t":"S"},{"DE":34.4740,"RA":106.5483,"AM":5.5500,"t":"S"},{"DE":-29.1559,"RA":111.9965,"AM":5.5500,"t":"S"},{"DE":14.2085,"RA":115.5134,"AM":5.5500,"t":"S"},{"DE":75.7569,"RA":124.8843,"AM":5.5500,"t":"S"},{"DE":-7.1772,"RA":132.8934,"AM":5.5500,"t":"S"},{"DE":53.6683,"RA":159.7737,"AM":5.5500,"t":"S"},{"DE":-72.2566,"RA":171.0465,"AM":5.5500,"t":"S"},{"DE":-71.9863,"RA":192.4373,"AM":5.5500,"t":"S"},{"DE":-16.1791,"RA":206.1243,"AM":5.5500,"t":"S"},{"DE":-43.0588,"RA":215.0404,"AM":5.5500,"t":"S"},{"DE":-46.2455,"RA":219.0793,"AM":5.5500,"t":"S"},{"DE":11.6607,"RA":220.4313,"AM":5.5500,"t":"S"},{"DE":78.9639,"RA":246.4311,"AM":5.5500,"t":"S"},{"DE":-19.9244,"RA":250.4737,"AM":5.5500,"t":"S"},{"DE":-58.3414,"RA":251.8319,"AM":5.5500,"t":"S"},{"DE":39.9746,"RA":260.4317,"AM":5.5500,"t":"S"},{"DE":50.3067,"RA":292.8306,"AM":5.5500,"t":"S"},{"DE":-5.5071,"RA":313.0362,"AM":5.5500,"t":"S"},{"DE":44.4717,"RA":314.5810,"AM":5.5500,"t":"S"},{"DE":-41.3860,"RA":316.6063,"AM":5.5500,"t":"S"},{"DE":58.0004,"RA":330.5191,"AM":5.5500,"t":"S"},{"DE":-6.5224,"RA":330.8186,"AM":5.5500,"t":"S"},{"DE":-16.7421,"RA":336.6428,"AM":5.5500,"t":"S"},{"DE":-28.8540,"RA":345.3308,"AM":5.5500,"t":"S"},{"DE":70.8881,"RA":348.9072,"AM":5.5500,"t":"S"},{"DE":40.2364,"RA":353.6564,"AM":5.5500,"t":"S"},{"DE":57.4514,"RA":356.7580,"AM":5.5500,"t":"S"},{"DE":60.3628,"RA":14.1957,"AM":5.5600,"t":"S"},{"DE":20.7391,"RA":16.9882,"AM":5.5600,"t":"S"},{"DE":64.2027,"RA":17.8564,"AM":5.5600,"t":"S"},{"DE":-2.4650,"RA":44.9215,"AM":5.5600,"t":"S"},{"DE":-11.1938,"RA":53.9903,"AM":5.5600,"t":"S"},{"DE":-0.2967,"RA":56.2354,"AM":5.5600,"t":"S"},{"DE":-24.4824,"RA":70.0284,"AM":5.5600,"t":"S"},{"DE":-37.2308,"RA":82.0639,"AM":5.5600,"t":"S"},{"DE":-14.5846,"RA":92.3939,"AM":5.5600,"t":"S"},{"DE":-69.9840,"RA":95.6594,"AM":5.5600,"t":"S"},{"DE":-43.6080,"RA":105.9889,"AM":5.5600,"t":"S"},{"DE":12.6546,"RA":126.6831,"AM":5.5600,"t":"S"},{"DE":-53.0154,"RA":130.0728,"AM":5.5600,"t":"S"},{"DE":-41.8643,"RA":135.3369,"AM":5.5600,"t":"S"},{"DE":-43.6133,"RA":138.1272,"AM":5.5600,"t":"S"},{"DE":-42.1949,"RA":140.4624,"AM":5.5600,"t":"S"},{"DE":-5.9149,"RA":143.6360,"AM":5.5600,"t":"S"},{"DE":-53.8913,"RA":145.9261,"AM":5.5600,"t":"S"},{"DE":-62.7451,"RA":147.7316,"AM":5.5600,"t":"S"},{"DE":43.6254,"RA":174.5858,"AM":5.5600,"t":"S"},{"DE":-56.9877,"RA":178.0431,"AM":5.5600,"t":"S"},{"DE":-32.8301,"RA":186.7154,"AM":5.5600,"t":"S"},{"DE":-85.7860,"RA":205.2339,"AM":5.5600,"t":"S"},{"DE":-68.1953,"RA":216.2764,"AM":5.5600,"t":"S"},{"DE":39.5815,"RA":230.6557,"AM":5.5600,"t":"S"},{"DE":22.0842,"RA":256.5752,"AM":5.5600,"t":"S"},{"DE":24.5641,"RA":265.6182,"AM":5.5600,"t":"S"},{"DE":42.1593,"RA":273.9116,"AM":5.5600,"t":"S"},{"DE":-16.3766,"RA":283.8792,"AM":5.5600,"t":"S"},{"DE":2.5353,"RA":284.3191,"AM":5.5600,"t":"S"},{"DE":-19.2903,"RA":287.0696,"AM":5.5600,"t":"S"},{"DE":24.3194,"RA":298.6295,"AM":5.5600,"t":"S"},{"DE":-67.4891,"RA":337.1564,"AM":5.5600,"t":"S"},{"DE":-3.4964,"RA":348.8927,"AM":5.5600,"t":"S"},{"DE":-5.1244,"RA":349.8499,"AM":5.5600,"t":"S"},{"DE":60.1335,"RA":350.6355,"AM":5.5600,"t":"S"},{"DE":32.3849,"RA":351.2118,"AM":5.5600,"t":"S"},{"DE":87.3075,"RA":351.7498,"AM":5.5600,"t":"S"},{"DE":64.1962,"RA":1.6105,"AM":5.5700,"t":"S"},{"DE":18.2120,"RA":2.2601,"AM":5.5700,"t":"S"},{"DE":-52.3731,"RA":8.6156,"AM":5.5700,"t":"S"},{"DE":-24.7673,"RA":9.3359,"AM":5.5700,"t":"S"},{"DE":-21.7225,"RA":12.0044,"AM":5.5700,"t":"S"},{"DE":19.6584,"RA":17.4550,"AM":5.5700,"t":"S"},{"DE":65.0189,"RA":17.9224,"AM":5.5700,"t":"S"},{"DE":68.0430,"RA":25.5853,"AM":5.5700,"t":"S"},{"DE":-42.0305,"RA":29.9118,"AM":5.5700,"t":"S"},{"DE":-67.8414,"RA":33.5605,"AM":5.5700,"t":"S"},{"DE":25.0430,"RA":33.9283,"AM":5.5700,"t":"S"},{"DE":50.1515,"RA":35.2425,"AM":5.5700,"t":"S"},{"DE":-12.6747,"RA":52.4001,"AM":5.5700,"t":"S"},{"DE":31.4374,"RA":72.3035,"AM":5.5700,"t":"S"},{"DE":14.1552,"RA":98.4007,"AM":5.5700,"t":"S"},{"DE":-56.4104,"RA":117.2780,"AM":5.5700,"t":"S"},{"DE":64.6038,"RA":134.1561,"AM":5.5700,"t":"S"},{"DE":31.1617,"RA":144.1785,"AM":5.5700,"t":"S"},{"DE":-30.6071,"RA":157.3974,"AM":5.5700,"t":"S"},{"DE":34.9887,"RA":158.3788,"AM":5.5700,"t":"S"},{"DE":59.3201,"RA":162.8489,"AM":5.5700,"t":"S"},{"DE":6.8066,"RA":190.4880,"AM":5.5700,"t":"S"},{"DE":-8.9844,"RA":197.1353,"AM":5.5700,"t":"S"},{"DE":10.7463,"RA":204.8942,"AM":5.5700,"t":"S"},{"DE":-34.7868,"RA":215.5822,"AM":5.5700,"t":"S"},{"DE":-84.4653,"RA":235.8174,"AM":5.5700,"t":"S"},{"DE":32.5158,"RA":235.9971,"AM":5.5700,"t":"S"},{"DE":5.4473,"RA":236.3478,"AM":5.5700,"t":"S"},{"DE":-57.9343,"RA":242.3273,"AM":5.5700,"t":"S"},{"DE":-48.7630,"RA":250.3351,"AM":5.5700,"t":"S"},{"DE":-23.1503,"RA":254.2002,"AM":5.5700,"t":"S"},{"DE":2.7245,"RA":262.8389,"AM":5.5700,"t":"S"},{"DE":36.4663,"RA":272.4958,"AM":5.5700,"t":"S"},{"DE":-21.7767,"RA":291.5798,"AM":5.5700,"t":"S"},{"DE":14.5960,"RA":292.3423,"AM":5.5700,"t":"S"},{"DE":6.0082,"RA":311.9514,"AM":5.5700,"t":"S"},{"DE":-44.8487,"RA":323.3480,"AM":5.5700,"t":"S"},{"DE":-11.3660,"RA":326.6337,"AM":5.5700,"t":"S"},{"DE":-47.3036,"RA":327.0654,"AM":5.5700,"t":"S"},{"DE":44.6499,"RA":330.7361,"AM":5.5700,"t":"S"},{"DE":57.1684,"RA":348.3165,"AM":5.5700,"t":"S"},{"DE":55.7057,"RA":359.2853,"AM":5.5700,"t":"S"},{"DE":61.2228,"RA":0.4042,"AM":5.5800,"t":"S"},{"DE":52.0199,"RA":6.0652,"AM":5.5800,"t":"S"},{"DE":-9.8394,"RA":16.5214,"AM":5.5800,"t":"S"},{"DE":-21.2754,"RA":24.7158,"AM":5.5800,"t":"S"},{"DE":19.9012,"RA":34.5314,"AM":5.5800,"t":"S"},{"DE":18.0231,"RA":44.1089,"AM":5.5800,"t":"S"},{"DE":49.8484,"RA":52.2180,"AM":5.5800,"t":"S"},{"DE":14.0352,"RA":64.9904,"AM":5.5800,"t":"S"},{"DE":15.6378,"RA":67.5358,"AM":5.5800,"t":"S"},{"DE":-53.4615,"RA":72.7306,"AM":5.5800,"t":"S"},{"DE":-51.8260,"RA":97.8262,"AM":5.5800,"t":"S"},{"DE":-27.0380,"RA":108.7132,"AM":5.5800,"t":"S"},{"DE":35.0485,"RA":114.6369,"AM":5.5800,"t":"S"},{"DE":48.1315,"RA":115.3017,"AM":5.5800,"t":"S"},{"DE":-20.0791,"RA":125.3384,"AM":5.5800,"t":"S"},{"DE":27.8936,"RA":126.6154,"AM":5.5800,"t":"S"},{"DE":-44.7551,"RA":146.6266,"AM":5.5800,"t":"S"},{"DE":-54.8773,"RA":156.7039,"AM":5.5800,"t":"S"},{"DE":-29.6638,"RA":157.3707,"AM":5.5800,"t":"S"},{"DE":-70.8779,"RA":166.7080,"AM":5.5800,"t":"S"},{"DE":16.4565,"RA":171.4016,"AM":5.5800,"t":"S"},{"DE":8.4439,"RA":178.7631,"AM":5.5800,"t":"S"},{"DE":-12.8302,"RA":188.3927,"AM":5.5800,"t":"S"},{"DE":-20.5835,"RA":195.9421,"AM":5.5800,"t":"S"},{"DE":49.8449,"RA":217.1580,"AM":5.5800,"t":"S"},{"DE":-34.8951,"RA":268.3478,"AM":5.5800,"t":"S"},{"DE":-63.0554,"RA":273.9193,"AM":5.5800,"t":"S"},{"DE":-30.7566,"RA":276.2560,"AM":5.5800,"t":"S"},{"DE":36.9717,"RA":283.4315,"AM":5.5800,"t":"S"},{"DE":6.6153,"RA":283.8644,"AM":5.5800,"t":"S"},{"DE":15.0837,"RA":288.8337,"AM":5.5800,"t":"S"},{"DE":36.9998,"RA":304.6194,"AM":5.5800,"t":"S"},{"DE":45.7950,"RA":305.5223,"AM":5.5800,"t":"S"},{"DE":23.8560,"RA":320.2683,"AM":5.5800,"t":"S"},{"DE":33.1723,"RA":332.3068,"AM":5.5800,"t":"S"},{"DE":-25.1809,"RA":333.4351,"AM":5.5800,"t":"S"},{"DE":53.2135,"RA":349.1761,"AM":5.5800,"t":"S"},{"DE":30.4149,"RA":350.2065,"AM":5.5800,"t":"S"},{"DE":-71.4369,"RA":1.1720,"AM":5.5900,"t":"S"},{"DE":52.8395,"RA":7.9216,"AM":5.5900,"t":"S"},{"DE":-13.5613,"RA":12.3567,"AM":5.5900,"t":"S"},{"DE":83.7074,"RA":13.7200,"AM":5.5900,"t":"S"},{"DE":-38.9165,"RA":15.3261,"AM":5.5900,"t":"S"},{"DE":64.3900,"RA":30.7508,"AM":5.5900,"t":"S"},{"DE":61.5211,"RA":43.9868,"AM":5.5900,"t":"S"},{"DE":-10.4857,"RA":55.8910,"AM":5.5900,"t":"S"},{"DE":-27.6518,"RA":61.4059,"AM":5.5900,"t":"S"},{"DE":-62.0772,"RA":69.1902,"AM":5.5900,"t":"S"},{"DE":-36.7799,"RA":98.8509,"AM":5.5900,"t":"S"},{"DE":-25.4142,"RA":104.6496,"AM":5.5900,"t":"S"},{"DE":-14.3605,"RA":110.2429,"AM":5.5900,"t":"S"},{"DE":3.2904,"RA":113.2986,"AM":5.5900,"t":"S"},{"DE":-60.3031,"RA":119.4442,"AM":5.5900,"t":"S"},{"DE":-35.4517,"RA":124.5725,"AM":5.5900,"t":"S"},{"DE":-57.6336,"RA":132.9022,"AM":5.5900,"t":"S"},{"DE":-30.3654,"RA":137.4851,"AM":5.5900,"t":"S"},{"DE":-17.1417,"RA":151.7896,"AM":5.5900,"t":"S"},{"DE":-43.1124,"RA":153.8815,"AM":5.5900,"t":"S"},{"DE":-13.5885,"RA":157.7493,"AM":5.5900,"t":"S"},{"DE":-62.4487,"RA":179.4168,"AM":5.5900,"t":"S"},{"DE":-64.3396,"RA":179.6986,"AM":5.5900,"t":"S"},{"DE":36.0421,"RA":180.4145,"AM":5.5900,"t":"S"},{"DE":-41.5884,"RA":196.6461,"AM":5.5900,"t":"S"},{"DE":-73.1901,"RA":223.3065,"AM":5.5900,"t":"S"},{"DE":48.1510,"RA":226.3577,"AM":5.5900,"t":"S"},{"DE":-40.7882,"RA":229.7349,"AM":5.5900,"t":"S"},{"DE":-33.9643,"RA":239.2255,"AM":5.5900,"t":"S"},{"DE":4.8348,"RA":289.1293,"AM":5.5900,"t":"S"},{"DE":-35.4215,"RA":289.9166,"AM":5.5900,"t":"S"},{"DE":-22.4025,"RA":290.1590,"AM":5.5900,"t":"S"},{"DE":-45.2717,"RA":293.3401,"AM":5.5900,"t":"S"},{"DE":68.8803,"RA":305.0250,"AM":5.5900,"t":"S"},{"DE":26.4619,"RA":309.2695,"AM":5.5900,"t":"S"},{"DE":66.6574,"RA":310.7958,"AM":5.5900,"t":"S"},{"DE":50.4618,"RA":314.6251,"AM":5.5900,"t":"S"},{"DE":46.7143,"RA":321.3312,"AM":5.5900,"t":"S"},{"DE":2.9304,"RA":357.9910,"AM":5.5900,"t":"S"},{"DE":-29.4852,"RA":359.8662,"AM":5.5900,"t":"S"},{"DE":79.6740,"RA":18.0690,"AM":5.6000,"t":"S"},{"DE":37.7149,"RA":20.9192,"AM":5.6000,"t":"S"},{"DE":1.7578,"RA":34.5060,"AM":5.6000,"t":"S"},{"DE":36.4601,"RA":56.1309,"AM":5.6000,"t":"S"},{"DE":-11.8491,"RA":77.8453,"AM":5.6000,"t":"S"},{"DE":-10.3289,"RA":81.2573,"AM":5.6000,"t":"S"},{"DE":14.3056,"RA":83.4762,"AM":5.6000,"t":"S"},{"DE":10.2401,"RA":83.8052,"AM":5.6000,"t":"S"},{"DE":27.9679,"RA":87.7421,"AM":5.6000,"t":"S"},{"DE":14.1718,"RA":88.0929,"AM":5.6000,"t":"S"},{"DE":-56.3700,"RA":95.7327,"AM":5.6000,"t":"S"},{"DE":-5.8688,"RA":98.0964,"AM":5.6000,"t":"S"},{"DE":-55.5400,"RA":101.8280,"AM":5.6000,"t":"S"},{"DE":-17.8649,"RA":111.7833,"AM":5.6000,"t":"S"},{"DE":-1.9053,"RA":112.3278,"AM":5.6000,"t":"S"},{"DE":-36.0501,"RA":115.7999,"AM":5.6000,"t":"S"},{"DE":-9.1834,"RA":117.5441,"AM":5.6000,"t":"S"},{"DE":17.3087,"RA":120.1971,"AM":5.6000,"t":"S"},{"DE":-3.9875,"RA":126.6134,"AM":5.6000,"t":"S"},{"DE":-8.5895,"RA":137.1757,"AM":5.6000,"t":"S"},{"DE":-5.1174,"RA":141.3501,"AM":5.6000,"t":"S"},{"DE":-7.0598,"RA":156.4345,"AM":5.6000,"t":"S"},{"DE":20.5421,"RA":183.0387,"AM":5.6000,"t":"S"},{"DE":40.1505,"RA":200.0790,"AM":5.6000,"t":"S"},{"DE":55.3484,"RA":203.5305,"AM":5.6000,"t":"S"},{"DE":15.7453,"RA":251.3438,"AM":5.6000,"t":"S"},{"DE":-33.5484,"RA":258.8302,"AM":5.6000,"t":"S"},{"DE":-43.4341,"RA":282.3958,"AM":5.6000,"t":"S"},{"DE":20.0977,"RA":291.5552,"AM":5.6000,"t":"S"},{"DE":47.0273,"RA":297.9961,"AM":5.6000,"t":"S"},{"DE":0.2736,"RA":298.6867,"AM":5.6000,"t":"S"},{"DE":-42.0495,"RA":305.6146,"AM":5.6000,"t":"S"},{"DE":47.8319,"RA":311.9554,"AM":5.6000,"t":"S"},{"DE":30.2056,"RA":317.1620,"AM":5.6000,"t":"S"},{"DE":0.6047,"RA":330.2709,"AM":5.6000,"t":"S"},{"DE":9.1290,"RA":337.2833,"AM":5.6000,"t":"S"},{"DE":41.6039,"RA":344.0985,"AM":5.6000,"t":"S"},{"DE":-28.8237,"RA":347.0878,"AM":5.6000,"t":"S"},{"DE":-56.8490,"RA":351.3309,"AM":5.6000,"t":"S"},{"DE":70.3598,"RA":351.8187,"AM":5.6000,"t":"S"},{"DE":-11.8711,"RA":39.8919,"AM":5.6000,"t":"S"},{"DE":-27.7690,"RA":146.0490,"AM":5.6000,"t":"S"},{"DE":-20.0580,"RA":5.4428,"AM":5.6100,"t":"S"},{"DE":-4.1035,"RA":30.9187,"AM":5.6100,"t":"S"},{"DE":30.5567,"RA":48.8352,"AM":5.6100,"t":"S"},{"DE":-12.5744,"RA":59.8755,"AM":5.6100,"t":"S"},{"DE":-13.0484,"RA":67.2789,"AM":5.6100,"t":"S"},{"DE":-24.3882,"RA":75.9720,"AM":5.6100,"t":"S"},{"DE":-25.5776,"RA":95.9830,"AM":5.6100,"t":"S"},{"DE":-80.8136,"RA":100.0121,"AM":5.6100,"t":"S"},{"DE":-33.2889,"RA":117.3975,"AM":5.6100,"t":"S"},{"DE":-3.7512,"RA":126.1459,"AM":5.6100,"t":"S"},{"DE":-32.1593,"RA":127.6192,"AM":5.6100,"t":"S"},{"DE":-55.5147,"RA":140.4586,"AM":5.6100,"t":"S"},{"DE":39.7579,"RA":145.5015,"AM":5.6100,"t":"S"},{"DE":8.7848,"RA":156.3133,"AM":5.6100,"t":"S"},{"DE":-34.0582,"RA":162.4876,"AM":5.6100,"t":"S"},{"DE":38.3149,"RA":194.0020,"AM":5.6100,"t":"S"},{"DE":-40.0517,"RA":204.9523,"AM":5.6100,"t":"S"},{"DE":31.1902,"RA":207.1614,"AM":5.6100,"t":"S"},{"DE":-41.8375,"RA":213.6779,"AM":5.6100,"t":"S"},{"DE":-25.6243,"RA":221.8440,"AM":5.6100,"t":"S"},{"DE":-34.6825,"RA":236.6842,"AM":5.6100,"t":"S"},{"DE":36.6438,"RA":239.7405,"AM":5.6100,"t":"S"},{"DE":-57.9124,"RA":243.9575,"AM":5.6100,"t":"S"},{"DE":45.5983,"RA":247.9468,"AM":5.6100,"t":"S"},{"DE":-5.7448,"RA":263.3743,"AM":5.6100,"t":"S"},{"DE":17.6970,"RA":266.7835,"AM":5.6100,"t":"S"},{"DE":29.8589,"RA":275.2374,"AM":5.6100,"t":"S"},{"DE":13.1198,"RA":330.2723,"AM":5.6100,"t":"S"},{"DE":61.6967,"RA":342.8440,"AM":5.6100,"t":"S"},{"DE":-11.3800,"RA":14.6828,"AM":5.6200,"t":"S"},{"DE":-15.6764,"RA":23.6574,"AM":5.6200,"t":"S"},{"DE":4.3529,"RA":45.5938,"AM":5.6200,"t":"S"},{"DE":-0.9303,"RA":49.5934,"AM":5.6200,"t":"S"},{"DE":84.9110,"RA":53.0823,"AM":5.6200,"t":"S"},{"DE":22.4780,"RA":59.2170,"AM":5.6200,"t":"S"},{"DE":-12.7923,"RA":61.0947,"AM":5.6200,"t":"S"},{"DE":65.6976,"RA":85.6102,"AM":5.6200,"t":"S"},{"DE":-37.6311,"RA":88.1382,"AM":5.6200,"t":"S"},{"DE":-11.7742,"RA":88.6818,"AM":5.6200,"t":"S"},{"DE":-0.5122,"RA":93.8928,"AM":5.6200,"t":"S"},{"DE":-36.7078,"RA":96.0042,"AM":5.6200,"t":"S"},{"DE":-32.7163,"RA":98.6472,"AM":5.6200,"t":"S"},{"DE":-30.9490,"RA":101.3800,"AM":5.6200,"t":"S"},{"DE":-24.6741,"RA":116.1424,"AM":5.6200,"t":"S"},{"DE":-21.1737,"RA":117.9293,"AM":5.6200,"t":"S"},{"DE":-57.3028,"RA":118.7223,"AM":5.6200,"t":"S"},{"DE":29.6565,"RA":123.2869,"AM":5.6200,"t":"S"},{"DE":12.6809,"RA":130.8014,"AM":5.6200,"t":"S"},{"DE":-32.1786,"RA":144.2912,"AM":5.6200,"t":"S"},{"DE":-46.1939,"RA":147.8322,"AM":5.6200,"t":"S"},{"DE":-5.3333,"RA":177.7593,"AM":5.6200,"t":"S"},{"DE":-47.8792,"RA":224.1336,"AM":5.6200,"t":"S"},{"DE":0.3721,"RA":228.9545,"AM":5.6200,"t":"S"},{"DE":36.4251,"RA":242.9502,"AM":5.6200,"t":"S"},{"DE":-49.6516,"RA":250.4176,"AM":5.6200,"t":"S"},{"DE":22.4642,"RA":268.9617,"AM":5.6200,"t":"S"},{"DE":23.6055,"RA":278.8767,"AM":5.6200,"t":"S"},{"DE":65.2581,"RA":284.1072,"AM":5.6200,"t":"S"},{"DE":32.2186,"RA":301.1507,"AM":5.6200,"t":"S"},{"DE":-64.7125,"RA":327.5005,"AM":5.6200,"t":"S"},{"DE":-59.6361,"RA":331.4624,"AM":5.6200,"t":"S"},{"DE":-45.9285,"RA":335.7830,"AM":5.6200,"t":"S"},{"DE":-38.8923,"RA":346.7234,"AM":5.6200,"t":"S"},{"DE":43.2977,"RA":25.1651,"AM":5.6300,"t":"S"},{"DE":35.2457,"RA":25.5145,"AM":5.6300,"t":"S"},{"DE":63.8525,"RA":26.9350,"AM":5.6300,"t":"S"},{"DE":-24.1229,"RA":49.8954,"AM":5.6300,"t":"S"},{"DE":4.1587,"RA":91.2432,"AM":5.6300,"t":"S"},{"DE":-5.3240,"RA":106.0219,"AM":5.6300,"t":"S"},{"DE":68.4656,"RA":112.7196,"AM":5.6300,"t":"S"},{"DE":59.5711,"RA":124.4601,"AM":5.6300,"t":"S"},{"DE":-71.5054,"RA":125.0023,"AM":5.6300,"t":"S"},{"DE":65.0209,"RA":129.7989,"AM":5.6300,"t":"S"},{"DE":10.0817,"RA":131.1877,"AM":5.6300,"t":"S"},{"DE":-32.7157,"RA":160.6800,"AM":5.6300,"t":"S"},{"DE":54.7854,"RA":173.7704,"AM":5.6300,"t":"S"},{"DE":-23.6964,"RA":187.5727,"AM":5.6300,"t":"S"},{"DE":-35.8620,"RA":196.7260,"AM":5.6300,"t":"S"},{"DE":-61.6919,"RA":204.3012,"AM":5.6300,"t":"S"},{"DE":22.4958,"RA":205.2598,"AM":5.6300,"t":"S"},{"DE":82.5119,"RA":222.5822,"AM":5.6300,"t":"S"},{"DE":49.6284,"RA":224.0959,"AM":5.6300,"t":"S"},{"DE":-26.2660,"RA":238.8753,"AM":5.6300,"t":"S"},{"DE":9.8917,"RA":241.9064,"AM":5.6300,"t":"S"},{"DE":5.5212,"RA":248.1487,"AM":5.6300,"t":"S"},{"DE":-0.8921,"RA":256.3844,"AM":5.6300,"t":"S"},{"DE":31.1581,"RA":262.7307,"AM":5.6300,"t":"S"},{"DE":-38.9957,"RA":277.1130,"AM":5.6300,"t":"S"},{"DE":-18.7288,"RA":277.5494,"AM":5.6300,"t":"S"},{"DE":-24.8468,"RA":285.6153,"AM":5.6300,"t":"S"},{"DE":31.7441,"RA":286.2411,"AM":5.6300,"t":"S"},{"DE":-3.1145,"RA":298.3281,"AM":5.6300,"t":"S"},{"DE":38.4403,"RA":306.8928,"AM":5.6300,"t":"S"},{"DE":5.5029,"RA":316.1444,"AM":5.6300,"t":"S"},{"DE":-22.6690,"RA":320.7520,"AM":5.6300,"t":"S"},{"DE":2.6861,"RA":326.8082,"AM":5.6300,"t":"S"},{"DE":-58.4761,"RA":351.8124,"AM":5.6300,"t":"S"},{"DE":33.4973,"RA":353.6592,"AM":5.6300,"t":"S"},{"DE":54.4691,"RA":256.3307,"AM":5.6300,"t":"S"},{"DE":74.9881,"RA":11.4129,"AM":5.6400,"t":"S"},{"DE":14.9461,"RA":16.2723,"AM":5.6400,"t":"S"},{"DE":25.9355,"RA":30.9139,"AM":5.6400,"t":"S"},{"DE":8.5698,"RA":32.8378,"AM":5.6400,"t":"S"},{"DE":12.4476,"RA":39.1580,"AM":5.6400,"t":"S"},{"DE":13.1873,"RA":46.5987,"AM":5.6400,"t":"S"},{"DE":21.5793,"RA":64.5967,"AM":5.6400,"t":"S"},{"DE":16.7773,"RA":65.8544,"AM":5.6400,"t":"S"},{"DE":48.7407,"RA":72.7889,"AM":5.6400,"t":"S"},{"DE":62.6537,"RA":80.0942,"AM":5.6400,"t":"S"},{"DE":-16.9758,"RA":81.1187,"AM":5.6400,"t":"S"},{"DE":-25.2156,"RA":105.2748,"AM":5.6400,"t":"S"},{"DE":-46.7745,"RA":109.0645,"AM":5.6400,"t":"S"},{"DE":-19.4125,"RA":113.3315,"AM":5.6400,"t":"S"},{"DE":-26.3513,"RA":115.7006,"AM":5.6400,"t":"S"},{"DE":-0.4827,"RA":135.4916,"AM":5.6400,"t":"S"},{"DE":29.9745,"RA":145.8886,"AM":5.6400,"t":"S"},{"DE":-8.4185,"RA":152.7328,"AM":5.6400,"t":"S"},{"DE":-40.4362,"RA":173.2004,"AM":5.6400,"t":"S"},{"DE":-47.3726,"RA":173.8055,"AM":5.6400,"t":"S"},{"DE":-75.8965,"RA":174.3161,"AM":5.6400,"t":"S"},{"DE":45.2685,"RA":196.4678,"AM":5.6400,"t":"S"},{"DE":11.3317,"RA":198.6303,"AM":5.6400,"t":"S"},{"DE":39.2653,"RA":224.9040,"AM":5.6400,"t":"S"},{"DE":-16.7165,"RA":232.0642,"AM":5.6400,"t":"S"},{"DE":-73.4467,"RA":235.0890,"AM":5.6400,"t":"S"},{"DE":-40.8397,"RA":251.1775,"AM":5.6400,"t":"S"},{"DE":-54.5972,"RA":255.0262,"AM":5.6400,"t":"S"},{"DE":8.0320,"RA":276.4117,"AM":5.6400,"t":"S"},{"DE":27.9095,"RA":283.5552,"AM":5.6400,"t":"S"},{"DE":-24.7191,"RA":294.0069,"AM":5.6400,"t":"S"},{"DE":-0.6212,"RA":295.1805,"AM":5.6400,"t":"S"},{"DE":-42.4229,"RA":305.9716,"AM":5.6400,"t":"S"},{"DE":59.9866,"RA":317.9510,"AM":5.6400,"t":"S"},{"DE":-37.8294,"RA":321.5952,"AM":5.6400,"t":"S"},{"DE":32.5726,"RA":337.5075,"AM":5.6400,"t":"S"},{"DE":-62.0012,"RA":349.2399,"AM":5.6400,"t":"S"},{"DE":-2.3936,"RA":33.1981,"AM":5.6500,"t":"S"},{"DE":-3.3962,"RA":39.4242,"AM":5.6500,"t":"S"},{"DE":44.9679,"RA":57.5185,"AM":5.6500,"t":"S"},{"DE":-16.3760,"RA":74.7557,"AM":5.6500,"t":"S"},{"DE":-80.4691,"RA":84.2874,"AM":5.6500,"t":"S"},{"DE":-51.2163,"RA":90.2049,"AM":5.6500,"t":"S"},{"DE":-32.1724,"RA":91.0844,"AM":5.6500,"t":"S"},{"DE":-19.0328,"RA":103.3284,"AM":5.6500,"t":"S"},{"DE":-23.0860,"RA":111.7478,"AM":5.6500,"t":"S"},{"DE":4.8798,"RA":120.3079,"AM":5.6500,"t":"S"},{"DE":1.7856,"RA":146.5984,"AM":5.6500,"t":"S"},{"DE":-13.7580,"RA":163.5741,"AM":5.6500,"t":"S"},{"DE":9.5397,"RA":191.5939,"AM":5.6500,"t":"S"},{"DE":-27.5974,"RA":192.1095,"AM":5.6500,"t":"S"},{"DE":-70.6272,"RA":201.4599,"AM":5.6500,"t":"S"},{"DE":10.8183,"RA":202.3042,"AM":5.6500,"t":"S"},{"DE":-27.6573,"RA":224.6636,"AM":5.6500,"t":"S"},{"DE":-83.2276,"RA":225.4613,"AM":5.6500,"t":"S"},{"DE":-83.0383,"RA":226.1957,"AM":5.6500,"t":"S"},{"DE":51.9585,"RA":230.0214,"AM":5.6500,"t":"S"},{"DE":-48.3176,"RA":230.4526,"AM":5.6500,"t":"S"},{"DE":-60.6572,"RA":230.7940,"AM":5.6500,"t":"S"},{"DE":69.2833,"RA":234.4133,"AM":5.6500,"t":"S"},{"DE":60.0484,"RA":261.4223,"AM":5.6500,"t":"S"},{"DE":19.2567,"RA":263.3451,"AM":5.6500,"t":"S"},{"DE":77.5471,"RA":277.4373,"AM":5.6500,"t":"S"},{"DE":21.2321,"RA":288.8223,"AM":5.6500,"t":"S"},{"DE":14.5446,"RA":289.1116,"AM":5.6500,"t":"S"},{"DE":-33.7035,"RA":300.0843,"AM":5.6500,"t":"S"},{"DE":-52.4458,"RA":303.5793,"AM":5.6500,"t":"S"},{"DE":8.2572,"RA":330.2885,"AM":5.6500,"t":"S"},{"DE":-26.9868,"RA":350.3146,"AM":5.6500,"t":"S"},{"DE":-31.4464,"RA":4.0369,"AM":5.6600,"t":"S"},{"DE":47.8640,"RA":11.1092,"AM":5.6600,"t":"S"},{"DE":-84.7696,"RA":24.3658,"AM":5.6600,"t":"S"},{"DE":58.4236,"RA":32.1691,"AM":5.6600,"t":"S"},{"DE":24.8393,"RA":56.2906,"AM":5.6600,"t":"S"},{"DE":45.6819,"RA":56.4969,"AM":5.6600,"t":"S"},{"DE":6.5349,"RA":58.0010,"AM":5.6600,"t":"S"},{"DE":48.3009,"RA":70.3505,"AM":5.6600,"t":"S"},{"DE":-30.7656,"RA":70.7887,"AM":5.6600,"t":"S"},{"DE":29.5699,"RA":80.3029,"AM":5.6600,"t":"S"},{"DE":-10.1074,"RA":101.6626,"AM":5.6600,"t":"S"},{"DE":-14.4928,"RA":114.0162,"AM":5.6600,"t":"S"},{"DE":46.1803,"RA":114.1318,"AM":5.6600,"t":"S"},{"DE":-48.6844,"RA":122.2896,"AM":5.6600,"t":"S"},{"DE":-16.2489,"RA":122.3689,"AM":5.6600,"t":"S"},{"DE":-56.0854,"RA":122.3901,"AM":5.6600,"t":"S"},{"DE":53.4015,"RA":129.5926,"AM":5.6600,"t":"S"},{"DE":-20.7491,"RA":142.3027,"AM":5.6600,"t":"S"},{"DE":-64.6763,"RA":154.7712,"AM":5.6600,"t":"S"},{"DE":-47.6991,"RA":155.0697,"AM":5.6600,"t":"S"},{"DE":56.5823,"RA":162.7960,"AM":5.6600,"t":"S"},{"DE":25.8703,"RA":182.9632,"AM":5.6600,"t":"S"},{"DE":-24.8407,"RA":185.8399,"AM":5.6600,"t":"S"},{"DE":-52.1608,"RA":208.8006,"AM":5.6600,"t":"S"},{"DE":-14.5509,"RA":247.4455,"AM":5.6600,"t":"S"},{"DE":-39.5069,"RA":258.0675,"AM":5.6600,"t":"S"},{"DE":28.4075,"RA":262.9566,"AM":5.6600,"t":"S"},{"DE":-29.7432,"RA":291.7353,"AM":5.6600,"t":"S"},{"DE":-18.2311,"RA":294.2639,"AM":5.6600,"t":"S"},{"DE":-9.8534,"RA":308.0987,"AM":5.6600,"t":"S"},{"DE":28.2505,"RA":312.8677,"AM":5.6600,"t":"S"},{"DE":5.7717,"RA":324.6331,"AM":5.6600,"t":"S"},{"DE":1.2853,"RA":325.5421,"AM":5.6600,"t":"S"},{"DE":-33.0813,"RA":339.7144,"AM":5.6600,"t":"S"},{"DE":-25.1642,"RA":345.0241,"AM":5.6600,"t":"S"},{"DE":-63.1107,"RA":352.2540,"AM":5.6600,"t":"S"},{"DE":-13.0602,"RA":354.4148,"AM":5.6600,"t":"S"},{"DE":-33.5293,"RA":2.0145,"AM":5.6700,"t":"S"},{"DE":-48.2149,"RA":7.6086,"AM":5.6700,"t":"S"},{"DE":42.0815,"RA":17.5782,"AM":5.6700,"t":"S"},{"DE":-67.7464,"RA":33.8691,"AM":5.6700,"t":"S"},{"DE":-78.9892,"RA":46.8831,"AM":5.6700,"t":"S"},{"DE":-50.3786,"RA":53.1449,"AM":5.6700,"t":"S"},{"DE":9.9980,"RA":60.4422,"AM":5.6700,"t":"S"},{"DE":-80.2140,"RA":64.4966,"AM":5.6700,"t":"S"},{"DE":5.5686,"RA":68.5344,"AM":5.6700,"t":"S"},{"DE":46.9621,"RA":77.6788,"AM":5.6700,"t":"S"},{"DE":18.5402,"RA":83.3818,"AM":5.6700,"t":"S"},{"DE":-6.0093,"RA":83.7542,"AM":5.6700,"t":"S"},{"DE":5.4200,"RA":91.2424,"AM":5.6700,"t":"S"},{"DE":14.6511,"RA":95.0176,"AM":5.6700,"t":"S"},{"DE":-80.9142,"RA":126.0846,"AM":5.6700,"t":"S"},{"DE":-23.1537,"RA":126.2299,"AM":5.6700,"t":"S"},{"DE":-45.1911,"RA":130.1469,"AM":5.6700,"t":"S"},{"DE":32.4742,"RA":133.1443,"AM":5.6700,"t":"S"},{"DE":11.8100,"RA":146.5972,"AM":5.6700,"t":"S"},{"DE":8.6504,"RA":158.7590,"AM":5.6700,"t":"S"},{"DE":-47.6791,"RA":166.1301,"AM":5.6700,"t":"S"},{"DE":-36.1349,"RA":220.2558,"AM":5.6700,"t":"S"},{"DE":26.3012,"RA":227.0991,"AM":5.6700,"t":"S"},{"DE":-28.4173,"RA":243.0668,"AM":5.6700,"t":"S"},{"DE":61.6965,"RA":245.9466,"AM":5.6700,"t":"S"},{"DE":-58.5998,"RA":247.0632,"AM":5.6700,"t":"S"},{"DE":3.1198,"RA":272.4751,"AM":5.6700,"t":"S"},{"DE":-38.7260,"RA":278.3464,"AM":5.6700,"t":"S"},{"DE":57.8149,"RA":284.1878,"AM":5.6700,"t":"S"},{"DE":16.4628,"RA":294.3225,"AM":5.6700,"t":"S"},{"DE":-0.7093,"RA":301.0965,"AM":5.6700,"t":"S"},{"DE":-62.4293,"RA":312.9102,"AM":5.6700,"t":"S"},{"DE":-73.1730,"RA":317.3408,"AM":5.6700,"t":"S"},{"DE":26.1746,"RA":321.1417,"AM":5.6700,"t":"S"},{"DE":67.1664,"RA":1.1746,"AM":5.6800,"t":"S"},{"DE":19.5003,"RA":32.6566,"AM":5.6800,"t":"S"},{"DE":-78.3518,"RA":52.4955,"AM":5.6800,"t":"S"},{"DE":19.7003,"RA":55.5789,"AM":5.6800,"t":"S"},{"DE":42.5866,"RA":73.1990,"AM":5.6800,"t":"S"},{"DE":-0.4165,"RA":80.3827,"AM":5.6800,"t":"S"},{"DE":13.4132,"RA":102.6062,"AM":5.6800,"t":"S"},{"DE":23.6017,"RA":103.0000,"AM":5.6800,"t":"S"},{"DE":-70.4971,"RA":107.1765,"AM":5.6800,"t":"S"},{"DE":-48.6014,"RA":114.5759,"AM":5.6800,"t":"S"},{"DE":-53.2119,"RA":128.0207,"AM":5.6800,"t":"S"},{"DE":15.5813,"RA":134.3967,"AM":5.6800,"t":"S"},{"DE":-25.2968,"RA":144.2509,"AM":5.6800,"t":"S"},{"DE":21.9493,"RA":150.7040,"AM":5.6800,"t":"S"},{"DE":-62.6494,"RA":177.6137,"AM":5.6800,"t":"S"},{"DE":55.7127,"RA":186.8963,"AM":5.6800,"t":"S"},{"DE":20.8961,"RA":187.4302,"AM":5.6800,"t":"S"},{"DE":1.8547,"RA":189.5934,"AM":5.6800,"t":"S"},{"DE":54.4327,"RA":206.6486,"AM":5.6800,"t":"S"},{"DE":0.7173,"RA":221.3759,"AM":5.6800,"t":"S"},{"DE":-24.2515,"RA":222.3281,"AM":5.6800,"t":"S"},{"DE":48.7208,"RA":222.4221,"AM":5.6800,"t":"S"},{"DE":20.5728,"RA":229.6021,"AM":5.6800,"t":"S"},{"DE":28.8230,"RA":259.7022,"AM":5.6800,"t":"S"},{"DE":16.3176,"RA":263.4141,"AM":5.6800,"t":"S"},{"DE":-53.6124,"RA":267.6183,"AM":5.6800,"t":"S"},{"DE":31.9266,"RA":280.9650,"AM":5.6800,"t":"S"},{"DE":-21.3598,"RA":283.5004,"AM":5.6800,"t":"S"},{"DE":40.5998,"RA":297.6555,"AM":5.6800,"t":"S"},{"DE":23.1013,"RA":299.7939,"AM":5.6800,"t":"S"},{"DE":21.4096,"RA":306.4189,"AM":5.6800,"t":"S"},{"DE":30.3343,"RA":309.7480,"AM":5.6800,"t":"S"},{"DE":41.7169,"RA":310.4854,"AM":5.6800,"t":"S"},{"DE":47.4177,"RA":313.9575,"AM":5.6800,"t":"S"},{"DE":49.3888,"RA":320.5017,"AM":5.6800,"t":"S"},{"DE":-14.0564,"RA":341.9282,"AM":5.6800,"t":"S"},{"DE":-50.9500,"RA":345.2814,"AM":5.6800,"t":"S"},{"DE":49.2958,"RA":346.9389,"AM":5.6800,"t":"S"},{"DE":59.3327,"RA":347.4339,"AM":5.6800,"t":"S"},{"DE":17.5944,"RA":347.6776,"AM":5.6800,"t":"S"},{"DE":2.1022,"RA":354.0970,"AM":5.6800,"t":"S"},{"DE":6.9555,"RA":8.0991,"AM":5.6900,"t":"S"},{"DE":44.7132,"RA":15.0148,"AM":5.6900,"t":"S"},{"DE":58.3273,"RA":23.3571,"AM":5.6900,"t":"S"},{"DE":-29.9073,"RA":24.0354,"AM":5.6900,"t":"S"},{"DE":37.2518,"RA":29.0389,"AM":5.6900,"t":"S"},{"DE":-25.2741,"RA":44.9007,"AM":5.6900,"t":"S"},{"DE":61.8500,"RA":64.2231,"AM":5.6900,"t":"S"},{"DE":-0.1598,"RA":80.9263,"AM":5.6900,"t":"S"},{"DE":30.2086,"RA":81.7845,"AM":5.6900,"t":"S"},{"DE":-58.7538,"RA":97.9930,"AM":5.6900,"t":"S"},{"DE":70.8083,"RA":105.3392,"AM":5.6900,"t":"S"},{"DE":-25.2310,"RA":107.4293,"AM":5.6900,"t":"S"},{"DE":-19.7023,"RA":114.1710,"AM":5.6900,"t":"S"},{"DE":-48.8302,"RA":114.1830,"AM":5.6900,"t":"S"},{"DE":-14.8462,"RA":118.0787,"AM":5.6900,"t":"S"},{"DE":-27.2879,"RA":166.4899,"AM":5.6900,"t":"S"},{"DE":40.6602,"RA":184.0314,"AM":5.6900,"t":"S"},{"DE":2.0872,"RA":200.4235,"AM":5.6900,"t":"S"},{"DE":-41.4976,"RA":201.7338,"AM":5.6900,"t":"S"},{"DE":-28.6928,"RA":203.1496,"AM":5.6900,"t":"S"},{"DE":-76.7968,"RA":211.3335,"AM":5.6900,"t":"S"},{"DE":8.5343,"RA":242.1170,"AM":5.6900,"t":"S"},{"DE":22.6321,"RA":255.2422,"AM":5.6900,"t":"S"},{"DE":53.4204,"RA":260.4390,"AM":5.6900,"t":"S"},{"DE":-62.8642,"RA":261.0045,"AM":5.6900,"t":"S"},{"DE":-32.5817,"RA":263.6771,"AM":5.6900,"t":"S"},{"DE":20.5654,"RA":267.1032,"AM":5.6900,"t":"S"},{"DE":45.5014,"RA":269.9842,"AM":5.6900,"t":"S"},{"DE":-47.2205,"RA":277.4831,"AM":5.6900,"t":"S"},{"DE":-10.1250,"RA":281.6805,"AM":5.6900,"t":"S"},{"DE":18.1054,"RA":284.0255,"AM":5.6900,"t":"S"},{"DE":26.2914,"RA":285.3223,"AM":5.6900,"t":"S"},{"DE":-13.6372,"RA":300.4942,"AM":5.6900,"t":"S"},{"DE":63.9801,"RA":305.2980,"AM":5.6900,"t":"S"},{"DE":13.3151,"RA":309.6833,"AM":5.6900,"t":"S"},{"DE":19.3296,"RA":315.1154,"AM":5.6900,"t":"S"},{"DE":-30.1251,"RA":316.5048,"AM":5.6900,"t":"S"},{"DE":38.2836,"RA":325.8569,"AM":5.6900,"t":"S"},{"DE":19.6684,"RA":328.4058,"AM":5.6900,"t":"S"},{"DE":28.9640,"RA":331.3945,"AM":5.6900,"t":"S"},{"DE":8.4855,"RA":0.6238,"AM":5.7000,"t":"S"},{"DE":-49.0752,"RA":1.5792,"AM":5.7000,"t":"S"},{"DE":-18.0613,"RA":11.9301,"AM":5.7000,"t":"S"},{"DE":-0.9738,"RA":18.7049,"AM":5.7000,"t":"S"},{"DE":-60.7893,"RA":25.4498,"AM":5.7000,"t":"S"},{"DE":-36.8323,"RA":25.5125,"AM":5.7000,"t":"S"},{"DE":50.7928,"RA":28.0390,"AM":5.7000,"t":"S"},{"DE":49.2044,"RA":29.6396,"AM":5.7000,"t":"S"},{"DE":3.6756,"RA":50.2784,"AM":5.7000,"t":"S"},{"DE":-40.3570,"RA":58.5965,"AM":5.7000,"t":"S"},{"DE":-8.8198,"RA":62.6990,"AM":5.7000,"t":"S"},{"DE":12.8083,"RA":89.7218,"AM":5.7000,"t":"S"},{"DE":2.4997,"RA":92.2413,"AM":5.7000,"t":"S"},{"DE":5.1001,"RA":94.3172,"AM":5.7000,"t":"S"},{"DE":39.3909,"RA":99.6648,"AM":5.7000,"t":"S"},{"DE":-30.4705,"RA":99.9278,"AM":5.7000,"t":"S"},{"DE":-16.3952,"RA":109.8674,"AM":5.7000,"t":"S"},{"DE":48.1839,"RA":112.2145,"AM":5.7000,"t":"S"},{"DE":-54.3672,"RA":118.1239,"AM":5.7000,"t":"S"},{"DE":-2.0487,"RA":131.5103,"AM":5.7000,"t":"S"},{"DE":-54.9658,"RA":133.7990,"AM":5.7000,"t":"S"},{"DE":-24.2855,"RA":151.0873,"AM":5.7000,"t":"S"},{"DE":-58.0605,"RA":152.9436,"AM":5.7000,"t":"S"},{"DE":-33.7376,"RA":164.8073,"AM":5.7000,"t":"S"},{"DE":24.6585,"RA":167.2045,"AM":5.7000,"t":"S"},{"DE":17.0895,"RA":189.2431,"AM":5.7000,"t":"S"},{"DE":-52.7874,"RA":192.7412,"AM":5.7000,"t":"S"},{"DE":-53.4598,"RA":196.9096,"AM":5.7000,"t":"S"},{"DE":-5.3962,"RA":203.8804,"AM":5.7000,"t":"S"},{"DE":53.7287,"RA":208.4626,"AM":5.7000,"t":"S"},{"DE":-24.9978,"RA":220.8065,"AM":5.7000,"t":"S"},{"DE":-48.7437,"RA":227.9904,"AM":5.7000,"t":"S"},{"DE":-72.4009,"RA":241.4828,"AM":5.7000,"t":"S"},{"DE":22.9603,"RA":261.0274,"AM":5.7000,"t":"S"},{"DE":-54.3253,"RA":291.9505,"AM":5.7000,"t":"S"},{"DE":-43.4452,"RA":292.3493,"AM":5.7000,"t":"S"},{"DE":-8.2273,"RA":298.6569,"AM":5.7000,"t":"S"},{"DE":62.0785,"RA":302.8951,"AM":5.7000,"t":"S"},{"DE":33.7291,"RA":303.8491,"AM":5.7000,"t":"S"},{"DE":-26.2964,"RA":314.1972,"AM":5.7000,"t":"S"},{"DE":24.2741,"RA":320.9951,"AM":5.7000,"t":"S"},{"DE":-20.0843,"RA":323.7127,"AM":5.7000,"t":"S"},{"DE":55.7967,"RA":328.0043,"AM":5.7000,"t":"S"},{"DE":76.2264,"RA":338.0678,"AM":5.7000,"t":"S"},{"DE":-14.4015,"RA":357.6387,"AM":5.7000,"t":"S"},{"DE":18.6471,"RA":76.8634,"AM":5.7000,"t":"S"},{"DE":-48.8099,"RA":0.2691,"AM":5.7100,"t":"S"},{"DE":41.0354,"RA":3.3786,"AM":5.7100,"t":"S"},{"DE":-9.7856,"RA":16.9425,"AM":5.7100,"t":"S"},{"DE":-57.3215,"RA":48.1381,"AM":5.7100,"t":"S"},{"DE":-35.6813,"RA":51.8892,"AM":5.7100,"t":"S"},{"DE":5.5230,"RA":62.8345,"AM":5.7100,"t":"S"},{"DE":-6.7389,"RA":68.4780,"AM":5.7100,"t":"S"},{"DE":-16.7407,"RA":73.7784,"AM":5.7100,"t":"S"},{"DE":-16.4178,"RA":73.8277,"AM":5.7100,"t":"S"},{"DE":-26.1524,"RA":76.3175,"AM":5.7100,"t":"S"},{"DE":-6.0648,"RA":84.1487,"AM":5.7100,"t":"S"},{"DE":47.9019,"RA":90.2440,"AM":5.7100,"t":"S"},{"DE":-22.7743,"RA":92.4498,"AM":5.7100,"t":"S"},{"DE":-18.6599,"RA":99.0952,"AM":5.7100,"t":"S"},{"DE":12.1158,"RA":108.6359,"AM":5.7100,"t":"S"},{"DE":-17.5863,"RA":125.4775,"AM":5.7100,"t":"S"},{"DE":24.0811,"RA":127.8772,"AM":5.7100,"t":"S"},{"DE":-46.1554,"RA":131.8285,"AM":5.7100,"t":"S"},{"DE":-50.2440,"RA":148.7135,"AM":5.7100,"t":"S"},{"DE":53.8917,"RA":151.1514,"AM":5.7100,"t":"S"},{"DE":-12.2301,"RA":159.1349,"AM":5.7100,"t":"S"},{"DE":36.3094,"RA":167.3295,"AM":5.7100,"t":"S"},{"DE":-33.5701,"RA":174.1456,"AM":5.7100,"t":"S"},{"DE":28.9372,"RA":184.3774,"AM":5.7100,"t":"S"},{"DE":-35.1864,"RA":186.3406,"AM":5.7100,"t":"S"},{"DE":14.1226,"RA":192.2259,"AM":5.7100,"t":"S"},{"DE":-60.3298,"RA":192.8249,"AM":5.7100,"t":"S"},{"DE":17.9329,"RA":208.3039,"AM":5.7100,"t":"S"},{"DE":-0.1403,"RA":225.4538,"AM":5.7100,"t":"S"},{"DE":-64.5315,"RA":231.8879,"AM":5.7100,"t":"S"},{"DE":14.1153,"RA":236.8222,"AM":5.7100,"t":"S"},{"DE":3.9933,"RA":272.3912,"AM":5.7100,"t":"S"},{"DE":-12.0148,"RA":275.8007,"AM":5.7100,"t":"S"},{"DE":6.1941,"RA":276.9949,"AM":5.7100,"t":"S"},{"DE":-43.5074,"RA":277.9843,"AM":5.7100,"t":"S"},{"DE":-65.0777,"RA":282.1581,"AM":5.7100,"t":"S"},{"DE":-15.0533,"RA":291.5460,"AM":5.7100,"t":"S"},{"DE":51.2366,"RA":293.5824,"AM":5.7100,"t":"S"},{"DE":16.6348,"RA":299.0053,"AM":5.7100,"t":"S"},{"DE":62.2575,"RA":304.9029,"AM":5.7100,"t":"S"},{"DE":-9.7486,"RA":321.3043,"AM":5.7100,"t":"S"},{"DE":-4.2762,"RA":328.5432,"AM":5.7100,"t":"S"},{"DE":53.0468,"RA":6.2767,"AM":5.7200,"t":"S"},{"DE":-3.9573,"RA":7.5098,"AM":5.7200,"t":"S"},{"DE":-56.5013,"RA":10.4431,"AM":5.7200,"t":"S"},{"DE":15.2799,"RA":33.2638,"AM":5.7200,"t":"S"},{"DE":37.3123,"RA":38.9114,"AM":5.7200,"t":"S"},{"DE":-0.6957,"RA":40.3083,"AM":5.7200,"t":"S"},{"DE":-18.5598,"RA":49.6714,"AM":5.7200,"t":"S"},{"DE":33.8076,"RA":52.0862,"AM":5.7200,"t":"S"},{"DE":-47.3595,"RA":56.3162,"AM":5.7200,"t":"S"},{"DE":57.8604,"RA":64.2837,"AM":5.7200,"t":"S"},{"DE":14.0772,"RA":65.5146,"AM":5.7200,"t":"S"},{"DE":21.6199,"RA":67.0032,"AM":5.7200,"t":"S"},{"DE":-21.2834,"RA":71.2673,"AM":5.7200,"t":"S"},{"DE":14.4883,"RA":86.8048,"AM":5.7200,"t":"S"},{"DE":-66.0396,"RA":91.5390,"AM":5.7200,"t":"S"},{"DE":-27.1543,"RA":92.6445,"AM":5.7200,"t":"S"},{"DE":-36.9907,"RA":99.3077,"AM":5.7200,"t":"S"},{"DE":32.6068,"RA":102.4221,"AM":5.7200,"t":"S"},{"DE":-46.8497,"RA":108.6918,"AM":5.7200,"t":"S"},{"DE":-7.9823,"RA":128.8675,"AM":5.7200,"t":"S"},{"DE":61.9623,"RA":133.3440,"AM":5.7200,"t":"S"},{"DE":45.6316,"RA":134.2083,"AM":5.7200,"t":"S"},{"DE":-19.7476,"RA":137.9948,"AM":5.7200,"t":"S"},{"DE":8.1883,"RA":142.1216,"AM":5.7200,"t":"S"},{"DE":69.2375,"RA":145.5621,"AM":5.7200,"t":"S"},{"DE":-46.9339,"RA":147.6748,"AM":5.7200,"t":"S"},{"DE":-45.2835,"RA":148.5736,"AM":5.7200,"t":"S"},{"DE":5.8070,"RA":182.5142,"AM":5.7200,"t":"S"},{"DE":70.2000,"RA":183.7855,"AM":5.7200,"t":"S"},{"DE":24.6133,"RA":204.2462,"AM":5.7200,"t":"S"},{"DE":-66.5879,"RA":214.1613,"AM":5.7200,"t":"S"},{"DE":40.4593,"RA":220.9352,"AM":5.7200,"t":"S"},{"DE":16.3881,"RA":224.2987,"AM":5.7200,"t":"S"},{"DE":-21.4155,"RA":224.3665,"AM":5.7200,"t":"S"},{"DE":63.3414,"RA":230.6601,"AM":5.7200,"t":"S"},{"DE":-12.3695,"RA":230.9677,"AM":5.7200,"t":"S"},{"DE":-36.7557,"RA":241.8175,"AM":5.7200,"t":"S"},{"DE":18.8081,"RA":243.8693,"AM":5.7200,"t":"S"},{"DE":-52.2972,"RA":261.9900,"AM":5.7200,"t":"S"},{"DE":41.2434,"RA":263.2803,"AM":5.7200,"t":"S"},{"DE":-22.7803,"RA":270.4766,"AM":5.7200,"t":"S"},{"DE":32.2307,"RA":271.4567,"AM":5.7200,"t":"S"},{"DE":-13.8971,"RA":291.3400,"AM":5.7200,"t":"S"},{"DE":42.9539,"RA":333.6848,"AM":5.7200,"t":"S"},{"DE":56.6247,"RA":338.4192,"AM":5.7200,"t":"S"},{"DE":14.5492,"RA":340.2195,"AM":5.7200,"t":"S"},{"DE":-4.9879,"RA":343.7957,"AM":5.7200,"t":"S"},{"DE":-47.9692,"RA":344.1992,"AM":5.7200,"t":"S"},{"DE":-82.1698,"RA":359.3874,"AM":5.7200,"t":"S"},{"DE":-62.8714,"RA":13.4076,"AM":5.7300,"t":"S"},{"DE":-63.7046,"RA":41.3644,"AM":5.7300,"t":"S"},{"DE":34.1308,"RA":66.1215,"AM":5.7300,"t":"S"},{"DE":28.6150,"RA":70.3323,"AM":5.7300,"t":"S"},{"DE":-39.6784,"RA":80.8501,"AM":5.7300,"t":"S"},{"DE":-18.5575,"RA":85.8403,"AM":5.7300,"t":"S"},{"DE":-32.0304,"RA":98.1624,"AM":5.7300,"t":"S"},{"DE":16.0790,"RA":105.0659,"AM":5.7300,"t":"S"},{"DE":-38.1393,"RA":114.9326,"AM":5.7300,"t":"S"},{"DE":25.5073,"RA":122.6133,"AM":5.7300,"t":"S"},{"DE":62.5072,"RA":124.8216,"AM":5.7300,"t":"S"},{"DE":-18.3285,"RA":137.2675,"AM":5.7300,"t":"S"},{"DE":16.4380,"RA":144.2608,"AM":5.7300,"t":"S"},{"DE":41.2295,"RA":155.5441,"AM":5.7300,"t":"S"},{"DE":34.0348,"RA":163.7424,"AM":5.7300,"t":"S"},{"DE":55.8505,"RA":171.4881,"AM":5.7300,"t":"S"},{"DE":31.7461,"RA":175.3929,"AM":5.7300,"t":"S"},{"DE":34.9318,"RA":177.4239,"AM":5.7300,"t":"S"},{"DE":-68.3073,"RA":185.5501,"AM":5.7300,"t":"S"},{"DE":-26.4952,"RA":204.2019,"AM":5.7300,"t":"S"},{"DE":19.9557,"RA":205.1686,"AM":5.7300,"t":"S"},{"DE":-69.4013,"RA":207.9476,"AM":5.7300,"t":"S"},{"DE":42.5662,"RA":238.8775,"AM":5.7300,"t":"S"},{"DE":76.7939,"RA":240.8808,"AM":5.7300,"t":"S"},{"DE":29.8065,"RA":252.6623,"AM":5.7300,"t":"S"},{"DE":-57.7122,"RA":256.1030,"AM":5.7300,"t":"S"},{"DE":24.3278,"RA":265.8399,"AM":5.7300,"t":"S"},{"DE":37.5946,"RA":281.2008,"AM":5.7300,"t":"S"},{"DE":-38.2531,"RA":285.8237,"AM":5.7300,"t":"S"},{"DE":52.3204,"RA":291.8582,"AM":5.7300,"t":"S"},{"DE":16.0313,"RA":300.8751,"AM":5.7300,"t":"S"},{"DE":29.8968,"RA":300.9056,"AM":5.7300,"t":"S"},{"DE":-27.0330,"RA":303.8221,"AM":5.7300,"t":"S"},{"DE":49.3834,"RA":306.7594,"AM":5.7300,"t":"S"},{"DE":-53.2631,"RA":318.9411,"AM":5.7300,"t":"S"},{"DE":-26.1715,"RA":324.0457,"AM":5.7300,"t":"S"},{"DE":41.0770,"RA":325.5956,"AM":5.7300,"t":"S"},{"DE":39.6343,"RA":338.9679,"AM":5.7300,"t":"S"},{"DE":36.3514,"RA":343.9354,"AM":5.7300,"t":"S"},{"DE":-64.4045,"RA":356.0501,"AM":5.7300,"t":"S"},{"DE":61.5332,"RA":4.2377,"AM":5.7400,"t":"S"},{"DE":5.2806,"RA":12.0957,"AM":5.7400,"t":"S","name":"96 G. Psc"},{"DE":-7.8594,"RA":38.6776,"AM":5.7400,"t":"S"},{"DE":-30.0450,"RA":39.0386,"AM":5.7400,"t":"S"},{"DE":20.0115,"RA":40.5914,"AM":5.7400,"t":"S"},{"DE":29.0771,"RA":47.4031,"AM":5.7400,"t":"S"},{"DE":-11.2866,"RA":52.0040,"AM":5.7400,"t":"S"},{"DE":59.9694,"RA":55.6781,"AM":5.7400,"t":"S"},{"DE":-62.5212,"RA":66.9418,"AM":5.7400,"t":"S"},{"DE":-22.7951,"RA":75.6874,"AM":5.7400,"t":"S"},{"DE":54.4287,"RA":84.1468,"AM":5.7400,"t":"S"},{"DE":-21.8123,"RA":91.7396,"AM":5.7400,"t":"S"},{"DE":-32.3713,"RA":97.1635,"AM":5.7400,"t":"S"},{"DE":-31.7061,"RA":102.5973,"AM":5.7400,"t":"S"},{"DE":25.3757,"RA":103.8278,"AM":5.7400,"t":"S"},{"DE":7.4712,"RA":106.9562,"AM":5.7400,"t":"S"},{"DE":45.2282,"RA":110.3230,"AM":5.7400,"t":"S"},{"DE":-60.5264,"RA":119.0777,"AM":5.7400,"t":"S"},{"DE":2.1022,"RA":126.3981,"AM":5.7400,"t":"S"},{"DE":-37.1472,"RA":131.2164,"AM":5.7400,"t":"S"},{"DE":54.2839,"RA":136.0017,"AM":5.7400,"t":"S"},{"DE":-46.0474,"RA":140.6000,"AM":5.7400,"t":"S"},{"DE":-19.4003,"RA":143.0850,"AM":5.7400,"t":"S"},{"DE":65.1084,"RA":154.5087,"AM":5.7400,"t":"S"},{"DE":68.4435,"RA":160.4512,"AM":5.7400,"t":"S"},{"DE":-64.2490,"RA":160.9634,"AM":5.7400,"t":"S"},{"DE":-59.6193,"RA":168.3783,"AM":5.7400,"t":"S"},{"DE":15.4133,"RA":172.4244,"AM":5.7400,"t":"S"},{"DE":-13.8591,"RA":188.1500,"AM":5.7400,"t":"S"},{"DE":78.6439,"RA":201.7381,"AM":5.7400,"t":"S"},{"DE":-49.9500,"RA":204.9993,"AM":5.7400,"t":"S"},{"DE":-67.6521,"RA":208.7047,"AM":5.7400,"t":"S"},{"DE":55.3980,"RA":218.1289,"AM":5.7400,"t":"S"},{"DE":49.3684,"RA":218.6651,"AM":5.7400,"t":"S"},{"DE":-40.2116,"RA":219.1839,"AM":5.7400,"t":"S"},{"DE":43.6421,"RA":219.5526,"AM":5.7400,"t":"S"},{"DE":-47.4411,"RA":221.6209,"AM":5.7400,"t":"S"},{"DE":-60.9040,"RA":229.1529,"AM":5.7400,"t":"S"},{"DE":64.2087,"RA":232.7327,"AM":5.7400,"t":"S"},{"DE":-55.0555,"RA":237.7784,"AM":5.7400,"t":"S"},{"DE":-65.0376,"RA":239.7423,"AM":5.7400,"t":"S"},{"DE":23.4948,"RA":242.9085,"AM":5.7400,"t":"S"},{"DE":1.1812,"RA":250.4270,"AM":5.7400,"t":"S"},{"DE":-58.5036,"RA":251.5884,"AM":5.7400,"t":"S"},{"DE":-24.9891,"RA":255.0396,"AM":5.7400,"t":"S"},{"DE":80.1364,"RA":259.9044,"AM":5.7400,"t":"S"},{"DE":-10.9263,"RA":264.5396,"AM":5.7400,"t":"S"},{"DE":-36.8584,"RA":269.7320,"AM":5.7400,"t":"S"},{"DE":80.0041,"RA":270.0379,"AM":5.7400,"t":"S"},{"DE":-4.7513,"RA":271.5633,"AM":5.7400,"t":"S"},{"DE":-57.5231,"RA":277.4863,"AM":5.7400,"t":"S"},{"DE":-14.8536,"RA":278.4126,"AM":5.7400,"t":"S"},{"DE":62.5266,"RA":279.3896,"AM":5.7400,"t":"S"},{"DE":-69.1640,"RA":299.6717,"AM":5.7400,"t":"S"},{"DE":57.4890,"RA":324.7401,"AM":5.7400,"t":"S"},{"DE":56.6112,"RA":328.7215,"AM":5.7400,"t":"S"},{"DE":19.4755,"RA":331.8691,"AM":5.7400,"t":"S"},{"DE":-78.7914,"RA":356.1696,"AM":5.7400,"t":"S"},{"DE":-11.9111,"RA":356.8163,"AM":5.7400,"t":"S"},{"DE":-7.0253,"RA":23.4285,"AM":5.7500,"t":"S"},{"DE":-11.3247,"RA":25.4368,"AM":5.7500,"t":"S"},{"DE":57.8998,"RA":34.4994,"AM":5.7500,"t":"S"},{"DE":-7.6630,"RA":45.2918,"AM":5.7500,"t":"S"},{"DE":33.5868,"RA":62.7459,"AM":5.7500,"t":"S"},{"DE":52.8698,"RA":74.0295,"AM":5.7500,"t":"S"},{"DE":-35.9770,"RA":78.6202,"AM":5.7500,"t":"S"},{"DE":-35.1394,"RA":83.2807,"AM":5.7500,"t":"S"},{"DE":23.1135,"RA":92.4333,"AM":5.7500,"t":"S"},{"DE":30.4930,"RA":97.1420,"AM":5.7500,"t":"S"},{"DE":77.9958,"RA":100.1202,"AM":5.7500,"t":"S"},{"DE":-1.3189,"RA":102.0794,"AM":5.7500,"t":"S"},{"DE":-2.2720,"RA":102.3184,"AM":5.7500,"t":"S"},{"DE":8.3804,"RA":103.2061,"AM":5.7500,"t":"S"},{"DE":-23.8407,"RA":106.8441,"AM":5.7500,"t":"S"},{"DE":26.8566,"RA":107.8461,"AM":5.7500,"t":"S"},{"DE":27.8974,"RA":108.9882,"AM":5.7500,"t":"S"},{"DE":-10.3267,"RA":112.3421,"AM":5.7500,"t":"S"},{"DE":-35.1138,"RA":126.9976,"AM":5.7500,"t":"S"},{"DE":-18.2412,"RA":133.8018,"AM":5.7500,"t":"S"},{"DE":-31.8892,"RA":142.6921,"AM":5.7500,"t":"S"},{"DE":29.6452,"RA":149.9009,"AM":5.7500,"t":"S"},{"DE":-53.2318,"RA":168.4142,"AM":5.7500,"t":"S"},{"DE":-44.3260,"RA":182.2242,"AM":5.7500,"t":"S"},{"DE":-60.3285,"RA":193.3412,"AM":5.7500,"t":"S"},{"DE":47.1967,"RA":193.7355,"AM":5.7500,"t":"S"},{"DE":23.8544,"RA":201.2778,"AM":5.7500,"t":"S"},{"DE":-40.5839,"RA":227.0505,"AM":5.7500,"t":"S"},{"DE":-26.3326,"RA":227.5776,"AM":5.7500,"t":"S"},{"DE":-70.0795,"RA":228.5799,"AM":5.7500,"t":"S"},{"DE":-12.7454,"RA":241.9017,"AM":5.7500,"t":"S"},{"DE":55.2051,"RA":246.1056,"AM":5.7500,"t":"S"},{"DE":16.3010,"RA":261.1314,"AM":5.7500,"t":"S"},{"DE":53.8017,"RA":265.9965,"AM":5.7500,"t":"S"},{"DE":11.8159,"RA":297.1752,"AM":5.7500,"t":"S"},{"DE":-66.9494,"RA":300.0963,"AM":5.7500,"t":"S"},{"DE":-31.5983,"RA":310.3485,"AM":5.7500,"t":"S"},{"DE":82.5312,"RA":310.6463,"AM":5.7500,"t":"S"},{"DE":-63.9283,"RA":317.1363,"AM":5.7500,"t":"S"},{"DE":53.5631,"RA":317.5648,"AM":5.7500,"t":"S"},{"DE":49.5103,"RA":319.8698,"AM":5.7500,"t":"S"},{"DE":32.2253,"RA":322.0343,"AM":5.7500,"t":"S"},{"DE":26.6737,"RA":331.2972,"AM":5.7500,"t":"S"},{"DE":-5.3872,"RA":334.2771,"AM":5.7500,"t":"S"},{"DE":62.8044,"RA":334.5526,"AM":5.7500,"t":"S"},{"DE":-51.8912,"RA":351.0552,"AM":5.7500,"t":"S"},{"DE":42.9120,"RA":351.7808,"AM":5.7500,"t":"S"},{"DE":-56.1964,"RA":24.9475,"AM":5.7600,"t":"S"},{"DE":23.5773,"RA":28.9627,"AM":5.7600,"t":"S"},{"DE":55.1060,"RA":40.7618,"AM":5.7600,"t":"S"},{"DE":18.3316,"RA":43.9521,"AM":5.7600,"t":"S"},{"DE":-42.6343,"RA":52.4798,"AM":5.7600,"t":"S"},{"DE":9.3734,"RA":53.1498,"AM":5.7600,"t":"S"},{"DE":24.5545,"RA":56.4770,"AM":5.7600,"t":"S"},{"DE":48.6505,"RA":58.4112,"AM":5.7600,"t":"S"},{"DE":6.1308,"RA":65.1718,"AM":5.7600,"t":"S"},{"DE":-3.2095,"RA":68.1565,"AM":5.7600,"t":"S"},{"DE":-16.3295,"RA":72.1356,"AM":5.7600,"t":"S"},{"DE":-33.0797,"RA":83.8145,"AM":5.7600,"t":"S"},{"DE":19.7905,"RA":93.0056,"AM":5.7600,"t":"S"},{"DE":-34.3966,"RA":94.9206,"AM":5.7600,"t":"S"},{"DE":-48.1769,"RA":96.4319,"AM":5.7600,"t":"S"},{"DE":-17.4660,"RA":97.1559,"AM":5.7600,"t":"S"},{"DE":28.9844,"RA":99.5959,"AM":5.7600,"t":"S"},{"DE":-38.2607,"RA":114.9495,"AM":5.7600,"t":"S"},{"DE":-5.4283,"RA":118.1994,"AM":5.7600,"t":"S"},{"DE":36.4196,"RA":128.6829,"AM":5.7600,"t":"S"},{"DE":-12.3577,"RA":137.2980,"AM":5.7600,"t":"S"},{"DE":-45.0667,"RA":157.9893,"AM":5.7600,"t":"S"},{"DE":3.0602,"RA":173.5915,"AM":5.7600,"t":"S"},{"DE":-44.6730,"RA":188.6767,"AM":5.7600,"t":"S"},{"DE":27.5524,"RA":192.3227,"AM":5.7600,"t":"S"},{"DE":11.5561,"RA":198.1372,"AM":5.7600,"t":"S"},{"DE":-46.8800,"RA":200.2405,"AM":5.7600,"t":"S"},{"DE":-5.1640,"RA":201.1385,"AM":5.7600,"t":"S"},{"DE":21.6962,"RA":209.6622,"AM":5.7600,"t":"S"},{"DE":-26.6462,"RA":221.9898,"AM":5.7600,"t":"S"},{"DE":46.1162,"RA":222.3278,"AM":5.7600,"t":"S"},{"DE":-67.0841,"RA":227.3747,"AM":5.7600,"t":"S"},{"DE":46.7978,"RA":234.5675,"AM":5.7600,"t":"S"},{"DE":-60.4825,"RA":239.0247,"AM":5.7600,"t":"S"},{"DE":-55.1397,"RA":245.1052,"AM":5.7600,"t":"S"},{"DE":22.1955,"RA":247.8060,"AM":5.7600,"t":"S"},{"DE":25.5056,"RA":255.5779,"AM":5.7600,"t":"S"},{"DE":-44.1297,"RA":259.6993,"AM":5.7600,"t":"S"},{"DE":-56.5255,"RA":260.7797,"AM":5.7600,"t":"S"},{"DE":-60.6738,"RA":261.0783,"AM":5.7600,"t":"S"},{"DE":24.3100,"RA":264.3796,"AM":5.7600,"t":"S"},{"DE":-28.0654,"RA":269.1743,"AM":5.7600,"t":"S"},{"DE":-18.8600,"RA":275.3458,"AM":5.7600,"t":"S"},{"DE":16.9286,"RA":277.7685,"AM":5.7600,"t":"S"},{"DE":-0.3095,"RA":279.3998,"AM":5.7600,"t":"S"},{"DE":-64.5514,"RA":280.9055,"AM":5.7600,"t":"S"},{"DE":13.0238,"RA":291.6006,"AM":5.7600,"t":"S"},{"DE":-53.1856,"RA":293.2242,"AM":5.7600,"t":"S"},{"DE":-54.9710,"RA":298.1571,"AM":5.7600,"t":"S"},{"DE":-8.5742,"RA":298.5345,"AM":5.7600,"t":"S"},{"DE":55.3971,"RA":304.6031,"AM":5.7600,"t":"S"},{"DE":-80.9649,"RA":308.3234,"AM":5.7600,"t":"S"},{"DE":-51.2653,"RA":315.0896,"AM":5.7600,"t":"S"},{"DE":-41.0067,"RA":321.1034,"AM":5.7600,"t":"S"},{"DE":63.2910,"RA":333.0935,"AM":5.7600,"t":"S"},{"DE":-13.5294,"RA":336.1128,"AM":5.7600,"t":"S"},{"DE":4.3938,"RA":336.6558,"AM":5.7600,"t":"S"},{"DE":-85.9673,"RA":337.9075,"AM":5.7600,"t":"S"},{"DE":11.7288,"RA":344.7992,"AM":5.7600,"t":"S"},{"DE":-8.9968,"RA":358.2105,"AM":5.7600,"t":"S"},{"DE":-9.5696,"RA":3.7271,"AM":5.7700,"t":"S"},{"DE":1.9397,"RA":6.3509,"AM":5.7700,"t":"S"},{"DE":58.2634,"RA":17.1394,"AM":5.7700,"t":"S"},{"DE":33.9597,"RA":66.1561,"AM":5.7700,"t":"S"},{"DE":-5.6740,"RA":72.1516,"AM":5.7700,"t":"S"},{"DE":17.2391,"RA":82.0067,"AM":5.7700,"t":"S"},{"DE":1.7893,"RA":82.4782,"AM":5.7700,"t":"S"},{"DE":-17.0846,"RA":102.5907,"AM":5.7700,"t":"S"},{"DE":-11.2513,"RA":108.2800,"AM":5.7700,"t":"S"},{"DE":27.6379,"RA":111.1394,"AM":5.7700,"t":"S"},{"DE":38.3445,"RA":115.0613,"AM":5.7700,"t":"S"},{"DE":-60.8245,"RA":119.7107,"AM":5.7700,"t":"S"},{"DE":-46.6444,"RA":122.9999,"AM":5.7700,"t":"S"},{"DE":-35.4900,"RA":123.5553,"AM":5.7700,"t":"S"},{"DE":-61.9505,"RA":141.3638,"AM":5.7700,"t":"S"},{"DE":72.2057,"RA":143.7226,"AM":5.7700,"t":"S"},{"DE":4.6147,"RA":153.2015,"AM":5.7700,"t":"S"},{"DE":4.7477,"RA":160.8372,"AM":5.7700,"t":"S"},{"DE":-44.3722,"RA":168.3112,"AM":5.7700,"t":"S"},{"DE":-24.4640,"RA":172.4109,"AM":5.7700,"t":"S"},{"DE":-38.9292,"RA":183.3543,"AM":5.7700,"t":"S"},{"DE":40.8552,"RA":198.8832,"AM":5.7700,"t":"S"},{"DE":-46.8987,"RA":207.9468,"AM":5.7700,"t":"S"},{"DE":-25.0104,"RA":210.0006,"AM":5.7700,"t":"S"},{"DE":-49.0886,"RA":226.8581,"AM":5.7700,"t":"S"},{"DE":54.6306,"RA":233.9877,"AM":5.7700,"t":"S"},{"DE":-2.3246,"RA":249.0894,"AM":5.7700,"t":"S"},{"DE":4.2198,"RA":250.1612,"AM":5.7700,"t":"S"},{"DE":8.8526,"RA":260.9901,"AM":5.7700,"t":"S"},{"DE":6.1014,"RA":268.3091,"AM":5.7700,"t":"S"},{"DE":-10.7958,"RA":277.8571,"AM":5.7700,"t":"S"},{"DE":31.1847,"RA":316.6260,"AM":5.7700,"t":"S"},{"DE":49.9776,"RA":323.2358,"AM":5.7700,"t":"S"},{"DE":20.2655,"RA":324.7549,"AM":5.7700,"t":"S"},{"DE":-41.1054,"RA":348.7442,"AM":5.7700,"t":"S"},{"DE":38.1823,"RA":350.2218,"AM":5.7700,"t":"S"},{"DE":1.0761,"RA":357.3645,"AM":5.7700,"t":"S"},{"DE":9.3134,"RA":357.8385,"AM":5.7700,"t":"S"},{"DE":-16.5290,"RA":1.0825,"AM":5.7800,"t":"S"},{"DE":-84.9940,"RA":3.3315,"AM":5.7800,"t":"S"},{"DE":60.3262,"RA":9.1139,"AM":5.7800,"t":"S"},{"DE":60.5513,"RA":25.8323,"AM":5.7800,"t":"S"},{"DE":32.6902,"RA":27.1732,"AM":5.7800,"t":"S"},{"DE":-16.9292,"RA":28.2171,"AM":5.7800,"t":"S"},{"DE":-34.5780,"RA":39.2442,"AM":5.7800,"t":"S"},{"DE":15.3119,"RA":41.1374,"AM":5.7800,"t":"S"},{"DE":27.2570,"RA":48.0594,"AM":5.7800,"t":"S"},{"DE":33.5360,"RA":51.1237,"AM":5.7800,"t":"S"},{"DE":34.3591,"RA":57.9738,"AM":5.7800,"t":"S"},{"DE":-81.5799,"RA":65.2418,"AM":5.7800,"t":"S"},{"DE":53.9108,"RA":68.0077,"AM":5.7800,"t":"S"},{"DE":16.0333,"RA":69.5393,"AM":5.7800,"t":"S"},{"DE":-8.5036,"RA":71.0222,"AM":5.7800,"t":"S"},{"DE":8.4286,"RA":80.4315,"AM":5.7800,"t":"S"},{"DE":-19.6954,"RA":81.4993,"AM":5.7800,"t":"S"},{"DE":9.5223,"RA":86.7172,"AM":5.7800,"t":"S"},{"DE":48.7110,"RA":92.9024,"AM":5.7800,"t":"S"},{"DE":32.6934,"RA":93.0838,"AM":5.7800,"t":"S"},{"DE":-60.2813,"RA":96.0577,"AM":5.7800,"t":"S"},{"DE":0.8902,"RA":98.8160,"AM":5.7800,"t":"S"},{"DE":-0.5409,"RA":102.7076,"AM":5.7800,"t":"S"},{"DE":15.3360,"RA":105.5729,"AM":5.7800,"t":"S"},{"DE":9.1858,"RA":106.4126,"AM":5.7800,"t":"S"},{"DE":7.9777,"RA":108.9143,"AM":5.7800,"t":"S"},{"DE":-31.4562,"RA":112.2705,"AM":5.7800,"t":"S"},{"DE":-27.0123,"RA":113.6450,"AM":5.7800,"t":"S"},{"DE":-36.4968,"RA":114.6829,"AM":5.7800,"t":"S"},{"DE":-60.2837,"RA":117.3039,"AM":5.7800,"t":"S"},{"DE":-66.1960,"RA":117.4208,"AM":5.7800,"t":"S"},{"DE":59.0474,"RA":120.3365,"AM":5.7800,"t":"S"},{"DE":-60.3539,"RA":133.4528,"AM":5.7800,"t":"S"},{"DE":-46.5839,"RA":137.8891,"AM":5.7800,"t":"S"},{"DE":-51.7558,"RA":153.3667,"AM":5.7800,"t":"S"},{"DE":76.9057,"RA":181.3118,"AM":5.7800,"t":"S"},{"DE":-56.5249,"RA":187.4758,"AM":5.7800,"t":"S"},{"DE":-39.8695,"RA":189.0043,"AM":5.7800,"t":"S"},{"DE":-42.2329,"RA":197.7871,"AM":5.7800,"t":"S"},{"DE":15.1318,"RA":221.5248,"AM":5.7800,"t":"S"},{"DE":-11.8983,"RA":223.5953,"AM":5.7800,"t":"S"},{"DE":-53.2098,"RA":237.5296,"AM":5.7800,"t":"S"},{"DE":-60.1776,"RA":238.8850,"AM":5.7800,"t":"S"},{"DE":-36.1853,"RA":239.3389,"AM":5.7800,"t":"S"},{"DE":-55.5409,"RA":243.3448,"AM":5.7800,"t":"S"},{"DE":-41.1509,"RA":253.7438,"AM":5.7800,"t":"S"},{"DE":86.9680,"RA":262.6958,"AM":5.7800,"t":"S"},{"DE":-46.9218,"RA":265.3177,"AM":5.7800,"t":"S"},{"DE":-60.1641,"RA":267.8978,"AM":5.7800,"t":"S"},{"DE":-23.5049,"RA":279.6280,"AM":5.7800,"t":"S"},{"DE":24.2508,"RA":286.6600,"AM":5.7800,"t":"S"},{"DE":46.6939,"RA":308.4785,"AM":5.7800,"t":"S"},{"DE":-17.9229,"RA":313.6992,"AM":5.7800,"t":"S"},{"DE":-21.1962,"RA":321.8118,"AM":5.7800,"t":"S"},{"DE":19.8267,"RA":327.8927,"AM":5.7800,"t":"S"},{"DE":11.6245,"RA":332.6560,"AM":5.7800,"t":"S"},{"DE":-70.4316,"RA":336.2936,"AM":5.7800,"t":"S"},{"DE":0.1093,"RA":358.6943,"AM":5.7800,"t":"S"},{"DE":32.9112,"RA":5.1897,"AM":5.7900,"t":"S"},{"DE":-30.2831,"RA":22.9302,"AM":5.7900,"t":"S"},{"DE":25.7829,"RA":33.9418,"AM":5.7900,"t":"S"},{"DE":6.8869,"RA":39.0204,"AM":5.7900,"t":"S","name":"268 G. Cet"},{"DE":-9.4529,"RA":40.0518,"AM":5.7900,"t":"S"},{"DE":57.1406,"RA":48.9499,"AM":5.7900,"t":"S"},{"DE":39.8995,"RA":53.3960,"AM":5.7900,"t":"S"},{"DE":67.2016,"RA":56.5036,"AM":5.7900,"t":"S"},{"DE":-62.8237,"RA":68.3918,"AM":5.7900,"t":"S"},{"DE":15.0403,"RA":73.9590,"AM":5.7900,"t":"S"},{"DE":23.9486,"RA":74.4527,"AM":5.7900,"t":"S"},{"DE":25.0504,"RA":74.5391,"AM":5.7900,"t":"S"},{"DE":-73.7413,"RA":83.6866,"AM":5.7900,"t":"S"},{"DE":9.8712,"RA":87.5112,"AM":5.7900,"t":"S"},{"DE":-29.7586,"RA":91.5231,"AM":5.7900,"t":"S"},{"DE":-20.9256,"RA":94.7457,"AM":5.7900,"t":"S"},{"DE":0.4953,"RA":100.2727,"AM":5.7900,"t":"S"},{"DE":-13.7520,"RA":111.2847,"AM":5.7900,"t":"S"},{"DE":-25.2178,"RA":111.3553,"AM":5.7900,"t":"S"},{"DE":-11.5569,"RA":111.9652,"AM":5.7900,"t":"S"},{"DE":13.4805,"RA":115.4660,"AM":5.7900,"t":"S"},{"DE":-50.9697,"RA":128.9668,"AM":5.7900,"t":"S"},{"DE":-79.5044,"RA":131.4801,"AM":5.7900,"t":"S"},{"DE":-38.7241,"RA":133.2001,"AM":5.7900,"t":"S"},{"DE":-15.8347,"RA":139.8880,"AM":5.7900,"t":"S"},{"DE":56.6992,"RA":140.4304,"AM":5.7900,"t":"S"},{"DE":-59.4258,"RA":147.8002,"AM":5.7900,"t":"S"},{"DE":38.9251,"RA":157.5269,"AM":5.7900,"t":"S"},{"DE":57.1992,"RA":160.9305,"AM":5.7900,"t":"S"},{"DE":-32.3675,"RA":167.4725,"AM":5.7900,"t":"S"},{"DE":8.0607,"RA":168.5076,"AM":5.7900,"t":"S"},{"DE":-38.9114,"RA":185.9365,"AM":5.7900,"t":"S"},{"DE":-3.8119,"RA":194.9146,"AM":5.7900,"t":"S"},{"DE":10.0225,"RA":197.3018,"AM":5.7900,"t":"S"},{"DE":-64.5766,"RA":205.0448,"AM":5.7900,"t":"S"},{"DE":-23.1417,"RA":234.4502,"AM":5.7900,"t":"S"},{"DE":36.6318,"RA":240.8307,"AM":5.7900,"t":"S"},{"DE":-37.1799,"RA":247.0603,"AM":5.7900,"t":"S"},{"DE":-69.2682,"RA":254.8916,"AM":5.7900,"t":"S"},{"DE":26.0973,"RA":271.9563,"AM":5.7900,"t":"S"},{"DE":18.2034,"RA":278.8025,"AM":5.7900,"t":"S"},{"DE":-25.9068,"RA":288.3069,"AM":5.7900,"t":"S"},{"DE":1.9504,"RA":292.2541,"AM":5.7900,"t":"S"},{"DE":36.9957,"RA":298.7010,"AM":5.7900,"t":"S"},{"DE":-16.1242,"RA":310.1355,"AM":5.7900,"t":"S"},{"DE":-3.9833,"RA":323.8234,"AM":5.7900,"t":"S"},{"DE":52.8823,"RA":330.4608,"AM":5.7900,"t":"S"},{"DE":21.7029,"RA":331.9596,"AM":5.7900,"t":"S"},{"DE":-4.8370,"RA":336.0287,"AM":5.7900,"t":"S"},{"DE":26.7632,"RA":337.2926,"AM":5.7900,"t":"S"},{"DE":44.7492,"RA":343.4173,"AM":5.7900,"t":"S"},{"DE":-41.4789,"RA":345.9985,"AM":5.7900,"t":"S"},{"DE":27.0823,"RA":0.5421,"AM":5.8000,"t":"S"},{"DE":61.3140,"RA":1.2756,"AM":5.8000,"t":"S"},{"DE":-47.5520,"RA":11.4398,"AM":5.8000,"t":"S"},{"DE":19.1884,"RA":13.6468,"AM":5.8000,"t":"S"},{"DE":37.7241,"RA":17.7928,"AM":5.8000,"t":"S"},{"DE":65.7453,"RA":39.4001,"AM":5.8000,"t":"S"},{"DE":81.4485,"RA":41.9485,"AM":5.8000,"t":"S"},{"DE":20.6687,"RA":44.5217,"AM":5.8000,"t":"S"},{"DE":57.9751,"RA":58.4302,"AM":5.8000,"t":"S"},{"DE":-20.3562,"RA":62.9008,"AM":5.8000,"t":"S"},{"DE":-8.6653,"RA":77.0841,"AM":5.8000,"t":"S"},{"DE":-3.4464,"RA":82.3487,"AM":5.8000,"t":"S"},{"DE":-35.5136,"RA":91.3632,"AM":5.8000,"t":"S"},{"DE":-20.4049,"RA":103.7614,"AM":5.8000,"t":"S"},{"DE":-40.8933,"RA":106.7795,"AM":5.8000,"t":"S"},{"DE":-3.9018,"RA":108.5452,"AM":5.8000,"t":"S"},{"DE":55.2814,"RA":110.7169,"AM":5.8000,"t":"S"},{"DE":51.8873,"RA":111.2379,"AM":5.8000,"t":"S"},{"DE":-36.0625,"RA":116.0404,"AM":5.8000,"t":"S"},{"DE":15.7903,"RA":119.2477,"AM":5.8000,"t":"S"},{"DE":20.7477,"RA":125.0874,"AM":5.8000,"t":"S"},{"DE":-2.1516,"RA":128.5067,"AM":5.8000,"t":"S"},{"DE":-16.1327,"RA":134.6830,"AM":5.8000,"t":"S"},{"DE":-60.9638,"RA":135.1906,"AM":5.8000,"t":"S"},{"DE":-57.2595,"RA":145.2589,"AM":5.8000,"t":"S"},{"DE":6.7086,"RA":146.5419,"AM":5.8000,"t":"S"},{"DE":-68.6828,"RA":152.3758,"AM":5.8000,"t":"S"},{"DE":-56.1104,"RA":154.6584,"AM":5.8000,"t":"S"},{"DE":-8.8978,"RA":162.5752,"AM":5.8000,"t":"S"},{"DE":11.4303,"RA":171.2455,"AM":5.8000,"t":"S"},{"DE":-53.1599,"RA":171.6970,"AM":5.8000,"t":"S"},{"DE":27.7814,"RA":174.0748,"AM":5.8000,"t":"S"},{"DE":53.1913,"RA":184.3733,"AM":5.8000,"t":"S"},{"DE":-23.1530,"RA":221.5282,"AM":5.8000,"t":"S"},{"DE":28.6158,"RA":222.4933,"AM":5.8000,"t":"S"},{"DE":18.4640,"RA":235.4780,"AM":5.8000,"t":"S"},{"DE":29.1503,"RA":244.1866,"AM":5.8000,"t":"S"},{"DE":9.5867,"RA":263.6529,"AM":5.8000,"t":"S"},{"DE":-45.8101,"RA":282.3639,"AM":5.8000,"t":"S"},{"DE":-45.1129,"RA":300.2014,"AM":5.8000,"t":"S"},{"DE":17.0702,"RA":301.0260,"AM":5.8000,"t":"S"},{"DE":-18.5196,"RA":332.2458,"AM":5.8000,"t":"S"},{"DE":-9.0401,"RA":334.2190,"AM":5.8000,"t":"S"},{"DE":75.3718,"RA":339.3037,"AM":5.8000,"t":"S"},{"DE":-11.6165,"RA":343.3696,"AM":5.8000,"t":"S"},{"DE":-56.1946,"RA":24.9450,"AM":5.8000,"t":"S","name":"p Eridani"},{"DE":25.4578,"RA":17.5810,"AM":5.8100,"t":"S"},{"DE":-55.9448,"RA":34.9761,"AM":5.8100,"t":"S"},{"DE":41.3963,"RA":35.7097,"AM":5.8100,"t":"S"},{"DE":7.7300,"RA":39.1461,"AM":5.8100,"t":"S"},{"DE":-46.9750,"RA":45.7327,"AM":5.8100,"t":"S"},{"DE":-66.4897,"RA":52.7154,"AM":5.8100,"t":"S"},{"DE":-20.9030,"RA":57.1488,"AM":5.8100,"t":"S"},{"DE":-24.8922,"RA":65.7736,"AM":5.8100,"t":"S"},{"DE":73.2681,"RA":79.5552,"AM":5.8100,"t":"S"},{"DE":-40.7073,"RA":84.6814,"AM":5.8100,"t":"S"},{"DE":-44.0346,"RA":89.6565,"AM":5.8100,"t":"S"},{"DE":-52.4097,"RA":101.4738,"AM":5.8100,"t":"S"},{"DE":-38.3189,"RA":109.1327,"AM":5.8100,"t":"S"},{"DE":23.1062,"RA":154.3107,"AM":5.8100,"t":"S"},{"DE":-43.8071,"RA":164.9975,"AM":5.8100,"t":"S"},{"DE":34.0983,"RA":199.6155,"AM":5.8100,"t":"S"},{"DE":-52.1830,"RA":200.5679,"AM":5.8100,"t":"S"},{"DE":-29.5609,"RA":204.6753,"AM":5.8100,"t":"S"},{"DE":-26.1160,"RA":206.4037,"AM":5.8100,"t":"S"},{"DE":55.8267,"RA":238.0690,"AM":5.8100,"t":"S"},{"DE":72.1569,"RA":265.4919,"AM":5.8100,"t":"S"},{"DE":-17.3739,"RA":274.2984,"AM":5.8100,"t":"S"},{"DE":29.8289,"RA":276.4949,"AM":5.8100,"t":"S"},{"DE":-0.2523,"RA":290.5898,"AM":5.8100,"t":"S"},{"DE":53.1657,"RA":301.5573,"AM":5.8100,"t":"S"},{"DE":60.6406,"RA":303.3650,"AM":5.8100,"t":"S"},{"DE":7.3545,"RA":320.2701,"AM":5.8100,"t":"S"},{"DE":-50.6867,"RA":346.8116,"AM":5.8100,"t":"S"},{"DE":42.0780,"RA":349.9684,"AM":5.8100,"t":"S"},{"DE":44.4290,"RA":354.3835,"AM":5.8100,"t":"S"},{"DE":33.7239,"RA":359.8721,"AM":5.8100,"t":"S"},{"DE":70.2646,"RA":22.8067,"AM":5.8200,"t":"S"},{"DE":-23.6060,"RA":44.5239,"AM":5.8200,"t":"S"},{"DE":48.1036,"RA":52.6539,"AM":5.8200,"t":"S"},{"DE":0.5878,"RA":54.1970,"AM":5.8200,"t":"S"},{"DE":63.2970,"RA":57.4025,"AM":5.8200,"t":"S"},{"DE":-34.9063,"RA":72.8676,"AM":5.8200,"t":"S"},{"DE":-34.3120,"RA":91.7653,"AM":5.8200,"t":"S"},{"DE":-58.0021,"RA":96.7672,"AM":5.8200,"t":"S"},{"DE":-35.2588,"RA":97.8046,"AM":5.8200,"t":"S"},{"DE":32.4549,"RA":98.1133,"AM":5.8200,"t":"S"},{"DE":-46.8577,"RA":117.3036,"AM":5.8200,"t":"S"},{"DE":-44.1604,"RA":127.2815,"AM":5.8200,"t":"S"},{"DE":-56.7794,"RA":170.7839,"AM":5.8200,"t":"S"},{"DE":-20.8442,"RA":183.7483,"AM":5.8200,"t":"S"},{"DE":56.7778,"RA":186.2634,"AM":5.8200,"t":"S"},{"DE":-43.9795,"RA":199.3080,"AM":5.8200,"t":"S"},{"DE":72.3915,"RA":201.5335,"AM":5.8200,"t":"S"},{"DE":-46.5929,"RA":209.0826,"AM":5.8200,"t":"S"},{"DE":25.1086,"RA":227.1482,"AM":5.8200,"t":"S"},{"DE":-16.6095,"RA":232.6683,"AM":5.8200,"t":"S"},{"DE":-40.0664,"RA":233.5071,"AM":5.8200,"t":"S"},{"DE":-21.0163,"RA":234.5678,"AM":5.8200,"t":"S"},{"DE":4.4274,"RA":240.2131,"AM":5.8200,"t":"S"},{"DE":-21.4415,"RA":261.1751,"AM":5.8200,"t":"S"},{"DE":0.6704,"RA":269.0767,"AM":5.8200,"t":"S"},{"DE":-7.7908,"RA":280.0016,"AM":5.8200,"t":"S"},{"DE":-25.0109,"RA":281.2067,"AM":5.8200,"t":"S"},{"DE":5.5001,"RA":281.3682,"AM":5.8200,"t":"S"},{"DE":-9.7741,"RA":282.7438,"AM":5.8200,"t":"S"},{"DE":1.8188,"RA":285.8844,"AM":5.8200,"t":"S"},{"DE":24.7687,"RA":292.2378,"AM":5.8200,"t":"S"},{"DE":17.7929,"RA":305.0892,"AM":5.8200,"t":"S"},{"DE":-31.6638,"RA":339.1477,"AM":5.8200,"t":"S"},{"DE":37.4167,"RA":342.0460,"AM":5.8200,"t":"S"},{"DE":40.3769,"RA":343.5290,"AM":5.8200,"t":"S"},{"DE":-77.3853,"RA":353.3315,"AM":5.8200,"t":"S"},{"DE":66.1476,"RA":10.5143,"AM":5.8300,"t":"S"},{"DE":61.5802,"RA":16.0813,"AM":5.8300,"t":"S"},{"DE":22.2753,"RA":27.5357,"AM":5.8300,"t":"S"},{"DE":18.2838,"RA":42.1337,"AM":5.8300,"t":"S"},{"DE":26.9245,"RA":84.2868,"AM":5.8300,"t":"S"},{"DE":24.4203,"RA":92.8846,"AM":5.8300,"t":"S"},{"DE":-3.7414,"RA":93.4760,"AM":5.8300,"t":"S"},{"DE":-4.5685,"RA":93.6529,"AM":5.8300,"t":"S"},{"DE":-5.9828,"RA":110.6058,"AM":5.8300,"t":"S"},{"DE":3.3717,"RA":113.5662,"AM":5.8300,"t":"S"},{"DE":-32.4635,"RA":120.7673,"AM":5.8300,"t":"S"},{"DE":-48.4620,"RA":122.7950,"AM":5.8300,"t":"S"},{"DE":-14.5741,"RA":139.2822,"AM":5.8300,"t":"S"},{"DE":-51.5607,"RA":139.6765,"AM":5.8300,"t":"S"},{"DE":-33.4185,"RA":149.1479,"AM":5.8300,"t":"S"},{"DE":61.7784,"RA":172.2693,"AM":5.8300,"t":"S"},{"DE":56.5986,"RA":178.9934,"AM":5.8300,"t":"S"},{"DE":60.3198,"RA":192.1642,"AM":5.8300,"t":"S"},{"DE":-47.1282,"RA":208.4885,"AM":5.8300,"t":"S"},{"DE":-46.1343,"RA":216.8009,"AM":5.8300,"t":"S"},{"DE":54.0233,"RA":219.5634,"AM":5.8300,"t":"S"},{"DE":-28.0606,"RA":225.5268,"AM":5.8300,"t":"S"},{"DE":6.9482,"RA":246.0451,"AM":5.8300,"t":"S"},{"DE":46.6133,"RA":249.0467,"AM":5.8300,"t":"S"},{"DE":-43.3984,"RA":249.6096,"AM":5.8300,"t":"S"},{"DE":48.2601,"RA":261.6843,"AM":5.8300,"t":"S"},{"DE":-80.8591,"RA":262.8645,"AM":5.8300,"t":"S"},{"DE":26.1013,"RA":271.9565,"AM":5.8300,"t":"S"},{"DE":38.4076,"RA":296.8657,"AM":5.8300,"t":"S"},{"DE":40.7321,"RA":304.5291,"AM":5.8300,"t":"S"},{"DE":50.7286,"RA":314.1061,"AM":5.8300,"t":"S"},{"DE":56.6696,"RA":315.5375,"AM":5.8300,"t":"S"},{"DE":-40.2694,"RA":318.0571,"AM":5.8300,"t":"S"},{"DE":-4.5195,"RA":319.5461,"AM":5.8300,"t":"S"},{"DE":11.3866,"RA":330.8293,"AM":5.8300,"t":"S"},{"DE":78.7859,"RA":336.6768,"AM":5.8300,"t":"S"},{"DE":-42.8613,"RA":347.4893,"AM":5.8300,"t":"S"},{"DE":-5.2486,"RA":2.5786,"AM":5.8400,"t":"S"},{"DE":-12.5799,"RA":2.6785,"AM":5.8400,"t":"S"},{"DE":-30.9456,"RA":20.8790,"AM":5.8400,"t":"S"},{"DE":27.8044,"RA":29.4323,"AM":5.8400,"t":"S"},{"DE":-43.5166,"RA":32.2888,"AM":5.8400,"t":"S"},{"DE":34.5424,"RA":38.2193,"AM":5.8400,"t":"S"},{"DE":-30.1941,"RA":39.5777,"AM":5.8400,"t":"S"},{"DE":-9.9614,"RA":45.4838,"AM":5.8400,"t":"S"},{"DE":-47.7517,"RA":49.3608,"AM":5.8400,"t":"S"},{"DE":86.6261,"RA":62.5013,"AM":5.8400,"t":"S"},{"DE":32.5882,"RA":72.3295,"AM":5.8400,"t":"S"},{"DE":-82.4705,"RA":74.7124,"AM":5.8400,"t":"S"},{"DE":21.7048,"RA":76.9810,"AM":5.8400,"t":"S"},{"DE":-20.8831,"RA":107.9233,"AM":5.8400,"t":"S"},{"DE":24.8850,"RA":108.6749,"AM":5.8400,"t":"S"},{"DE":-24.7107,"RA":113.2907,"AM":5.8400,"t":"S"},{"DE":25.3707,"RA":154.1740,"AM":5.8400,"t":"S"},{"DE":37.9100,"RA":159.7819,"AM":5.8400,"t":"S"},{"DE":-61.0524,"RA":174.0932,"AM":5.8400,"t":"S"},{"DE":-46.1456,"RA":190.3458,"AM":5.8400,"t":"S"},{"DE":54.0995,"RA":194.0733,"AM":5.8400,"t":"S"},{"DE":-78.4475,"RA":198.5723,"AM":5.8400,"t":"S"},{"DE":-48.9570,"RA":198.6804,"AM":5.8400,"t":"S"},{"DE":15.2634,"RA":214.3686,"AM":5.8400,"t":"S"},{"DE":-67.7172,"RA":217.8184,"AM":5.8400,"t":"S"},{"DE":-26.1936,"RA":228.4721,"AM":5.8400,"t":"S"},{"DE":50.4233,"RA":234.6425,"AM":5.8400,"t":"S"},{"DE":-20.9831,"RA":239.4186,"AM":5.8400,"t":"S"},{"DE":-33.1458,"RA":250.4394,"AM":5.8400,"t":"S"},{"DE":-42.4789,"RA":253.6123,"AM":5.8400,"t":"S"},{"DE":-41.1731,"RA":263.2808,"AM":5.8400,"t":"S"},{"DE":-34.4168,"RA":268.0823,"AM":5.8400,"t":"S"},{"DE":-8.3240,"RA":271.5308,"AM":5.8400,"t":"S"},{"DE":-47.9098,"RA":279.8095,"AM":5.8400,"t":"S"},{"DE":48.8594,"RA":283.6964,"AM":5.8400,"t":"S"},{"DE":-18.3084,"RA":290.4621,"AM":5.8400,"t":"S"},{"DE":19.8915,"RA":291.6195,"AM":5.8400,"t":"S"},{"DE":2.9300,"RA":292.0867,"AM":5.8400,"t":"S"},{"DE":-12.6175,"RA":303.1078,"AM":5.8400,"t":"S"},{"DE":22.1794,"RA":322.2491,"AM":5.8400,"t":"S"},{"DE":65.3208,"RA":328.8791,"AM":5.8400,"t":"S"},{"DE":19.5223,"RA":339.7191,"AM":5.8400,"t":"S"},{"DE":44.5461,"RA":341.5425,"AM":5.8400,"t":"S"},{"DE":53.5261,"RA":40.7479,"AM":5.8500,"t":"S"},{"DE":-5.4699,"RA":59.7183,"AM":5.8500,"t":"S"},{"DE":-7.5925,"RA":65.1785,"AM":5.8500,"t":"S"},{"DE":20.6847,"RA":69.5660,"AM":5.8500,"t":"S"},{"DE":46.2740,"RA":104.1336,"AM":5.8500,"t":"S"},{"DE":24.1286,"RA":108.1099,"AM":5.8500,"t":"S"},{"DE":7.2983,"RA":135.6867,"AM":5.8500,"t":"S"},{"DE":-44.1458,"RA":138.5342,"AM":5.8500,"t":"S"},{"DE":-37.6024,"RA":138.7382,"AM":5.8500,"t":"S"},{"DE":8.9332,"RA":149.1082,"AM":5.8500,"t":"S"},{"DE":-59.3238,"RA":162.3519,"AM":5.8500,"t":"S"},{"DE":-9.8527,"RA":162.4312,"AM":5.8500,"t":"S"},{"DE":-30.8348,"RA":177.9234,"AM":5.8500,"t":"S"},{"DE":10.2623,"RA":183.3581,"AM":5.8500,"t":"S"},{"DE":64.8224,"RA":205.3744,"AM":5.8500,"t":"S"},{"DE":-33.3006,"RA":223.6580,"AM":5.8500,"t":"S"},{"DE":-42.8679,"RA":227.1633,"AM":5.8500,"t":"S"},{"DE":54.5087,"RA":234.3834,"AM":5.8500,"t":"S"},{"DE":55.3766,"RA":236.9080,"AM":5.8500,"t":"S"},{"DE":-21.0519,"RA":279.7225,"AM":5.8500,"t":"S"},{"DE":49.8558,"RA":288.0212,"AM":5.8500,"t":"S"},{"DE":43.3882,"RA":290.9854,"AM":5.8500,"t":"S"},{"DE":-40.5910,"RA":339.2452,"AM":5.8500,"t":"S"},{"DE":3.0118,"RA":345.1788,"AM":5.8500,"t":"S"},{"DE":11.0650,"RA":348.3604,"AM":5.8500,"t":"S"},{"DE":-14.2512,"RA":358.1250,"AM":5.8500,"t":"S"},{"DE":47.9474,"RA":4.2877,"AM":5.8600,"t":"S"},{"DE":72.6745,"RA":12.0373,"AM":5.8600,"t":"S"},{"DE":16.9556,"RA":27.0456,"AM":5.8600,"t":"S"},{"DE":-21.0001,"RA":33.2541,"AM":5.8600,"t":"S"},{"DE":46.8419,"RA":42.9239,"AM":5.8600,"t":"S"},{"DE":-7.3919,"RA":54.6219,"AM":5.8600,"t":"S"},{"DE":-0.0982,"RA":65.3627,"AM":5.8600,"t":"S"},{"DE":49.9738,"RA":70.8400,"AM":5.8600,"t":"S"},{"DE":-4.2101,"RA":75.6891,"AM":5.8600,"t":"S"},{"DE":-40.9435,"RA":81.7722,"AM":5.8600,"t":"S"},{"DE":-45.9253,"RA":82.9000,"AM":5.8600,"t":"S"},{"DE":17.9064,"RA":93.6191,"AM":5.8600,"t":"S"},{"DE":58.1626,"RA":97.6963,"AM":5.8600,"t":"S"},{"DE":16.6744,"RA":105.6387,"AM":5.8600,"t":"S"},{"DE":-43.9868,"RA":109.5177,"AM":5.8600,"t":"S"},{"DE":-7.5512,"RA":112.3568,"AM":5.8600,"t":"S"},{"DE":8.8628,"RA":118.8810,"AM":5.8600,"t":"S"},{"DE":-45.8345,"RA":123.5995,"AM":5.8600,"t":"S"},{"DE":-29.4630,"RA":132.5093,"AM":5.8600,"t":"S"},{"DE":-74.7346,"RA":139.3651,"AM":5.8600,"t":"S"},{"DE":-15.5774,"RA":142.5937,"AM":5.8600,"t":"S"},{"DE":-35.7148,"RA":142.8876,"AM":5.8600,"t":"S"},{"DE":72.8795,"RA":149.5953,"AM":5.8600,"t":"S"},{"DE":37.4019,"RA":152.8033,"AM":5.8600,"t":"S"},{"DE":-14.0834,"RA":165.0487,"AM":5.8600,"t":"S"},{"DE":21.8814,"RA":188.7840,"AM":5.8600,"t":"S"},{"DE":-30.4224,"RA":189.7644,"AM":5.8600,"t":"S"},{"DE":-18.7160,"RA":214.6594,"AM":5.8600,"t":"S"},{"DE":-52.6795,"RA":218.3749,"AM":5.8600,"t":"S"},{"DE":-54.9986,"RA":218.3851,"AM":5.8600,"t":"S"},{"DE":23.9118,"RA":222.5658,"AM":5.8600,"t":"S"},{"DE":2.5152,"RA":236.0076,"AM":5.8600,"t":"S"},{"DE":-48.9124,"RA":237.4896,"AM":5.8600,"t":"S"},{"DE":-23.6854,"RA":242.1822,"AM":5.8600,"t":"S"},{"DE":-41.1198,"RA":242.8238,"AM":5.8600,"t":"S"},{"DE":42.2389,"RA":251.8323,"AM":5.8600,"t":"S"},{"DE":-20.4156,"RA":253.3551,"AM":5.8600,"t":"S"},{"DE":-58.0103,"RA":260.7301,"AM":5.8600,"t":"S"},{"DE":-4.8211,"RA":269.9032,"AM":5.8600,"t":"S"},{"DE":-41.3591,"RA":272.7731,"AM":5.8600,"t":"S"},{"DE":-75.8915,"RA":272.8157,"AM":5.8600,"t":"S"},{"DE":-73.6724,"RA":273.1422,"AM":5.8600,"t":"S"},{"DE":-41.8923,"RA":287.4902,"AM":5.8600,"t":"S"},{"DE":41.7731,"RA":295.9379,"AM":5.8600,"t":"S"},{"DE":-21.8100,"RA":304.5058,"AM":5.8600,"t":"S"},{"DE":-28.6633,"RA":306.3618,"AM":5.8600,"t":"S"},{"DE":-25.7812,"RA":312.3234,"AM":5.8600,"t":"S"},{"DE":16.8412,"RA":343.2594,"AM":5.8600,"t":"S"},{"DE":71.6420,"RA":353.7460,"AM":5.8600,"t":"S"},{"DE":36.4253,"RA":357.4207,"AM":5.8600,"t":"S"},{"DE":66.0990,"RA":0.6504,"AM":5.8700,"t":"S"},{"DE":71.7438,"RA":19.0496,"AM":5.8700,"t":"S"},{"DE":-0.5090,"RA":19.9512,"AM":5.8700,"t":"S"},{"DE":-15.3059,"RA":30.7440,"AM":5.8700,"t":"S"},{"DE":11.2123,"RA":66.8699,"AM":5.8700,"t":"S"},{"DE":7.5414,"RA":84.5047,"AM":5.8700,"t":"S"},{"DE":-22.9719,"RA":87.4729,"AM":5.8700,"t":"S"},{"DE":-4.6165,"RA":88.8757,"AM":5.8700,"t":"S"},{"DE":-1.5073,"RA":96.6649,"AM":5.8700,"t":"S"},{"DE":56.8575,"RA":99.4100,"AM":5.8700,"t":"S"},{"DE":16.2029,"RA":102.4577,"AM":5.8700,"t":"S"},{"DE":40.8834,"RA":109.5092,"AM":5.8700,"t":"S"},{"DE":-25.8916,"RA":110.2681,"AM":5.8700,"t":"S"},{"DE":-52.6512,"RA":112.4989,"AM":5.8700,"t":"S"},{"DE":-37.9337,"RA":116.5439,"AM":5.8700,"t":"S"},{"DE":-54.1513,"RA":120.2081,"AM":5.8700,"t":"S"},{"DE":25.3928,"RA":120.2328,"AM":5.8700,"t":"S"},{"DE":33.6557,"RA":142.6801,"AM":5.8700,"t":"S"},{"DE":-31.6879,"RA":162.0588,"AM":5.8700,"t":"S"},{"DE":-37.7476,"RA":171.3879,"AM":5.8700,"t":"S"},{"DE":-33.3155,"RA":191.6926,"AM":5.8700,"t":"S"},{"DE":37.5169,"RA":192.5448,"AM":5.8700,"t":"S"},{"DE":-53.3733,"RA":208.4296,"AM":5.8700,"t":"S"},{"DE":-25.8154,"RA":214.7538,"AM":5.8700,"t":"S"},{"DE":-65.8216,"RA":216.7796,"AM":5.8700,"t":"S"},{"DE":-25.2437,"RA":238.6647,"AM":5.8700,"t":"S"},{"DE":-67.1966,"RA":258.3251,"AM":5.8700,"t":"S"},{"DE":72.4558,"RA":264.2869,"AM":5.8700,"t":"S"},{"DE":-42.7293,"RA":266.1750,"AM":5.8700,"t":"S"},{"DE":23.8662,"RA":277.3988,"AM":5.8700,"t":"S"},{"DE":-9.9582,"RA":299.9473,"AM":5.8700,"t":"S"},{"DE":45.5795,"RA":304.0026,"AM":5.8700,"t":"S"},{"DE":37.4764,"RA":305.9349,"AM":5.8700,"t":"S"},{"DE":-12.5449,"RA":312.6741,"AM":5.8700,"t":"S"},{"DE":-4.5601,"RA":320.2680,"AM":5.8700,"t":"S"},{"DE":28.6080,"RA":333.4112,"AM":5.8700,"t":"S"},{"DE":31.5172,"RA":4.6594,"AM":5.8800,"t":"S"},{"DE":33.5816,"RA":7.8568,"AM":5.8800,"t":"S"},{"DE":21.2505,"RA":9.8409,"AM":5.8800,"t":"S"},{"DE":-7.3471,"RA":13.9267,"AM":5.8800,"t":"S"},{"DE":-82.9750,"RA":24.4794,"AM":5.8800,"t":"S"},{"DE":-15.3412,"RA":36.5015,"AM":5.8800,"t":"S"},{"DE":25.2350,"RA":37.6348,"AM":5.8800,"t":"S"},{"DE":-28.0916,"RA":45.4067,"AM":5.8800,"t":"S"},{"DE":68.6800,"RA":61.5132,"AM":5.8800,"t":"S"},{"DE":-63.2554,"RA":64.4178,"AM":5.8800,"t":"S"},{"DE":28.9611,"RA":68.6583,"AM":5.8800,"t":"S"},{"DE":1.0370,"RA":77.9390,"AM":5.8800,"t":"S"},{"DE":-22.3737,"RA":85.5582,"AM":5.8800,"t":"S"},{"DE":-10.2426,"RA":91.3626,"AM":5.8800,"t":"S"},{"DE":-20.2722,"RA":93.7850,"AM":5.8800,"t":"S"},{"DE":-37.2535,"RA":94.2899,"AM":5.8800,"t":"S"},{"DE":-0.9459,"RA":96.3189,"AM":5.8800,"t":"S"},{"DE":46.6856,"RA":97.5124,"AM":5.8800,"t":"S"},{"DE":4.8560,"RA":98.0800,"AM":5.8800,"t":"S"},{"DE":71.7488,"RA":100.1344,"AM":5.8800,"t":"S"},{"DE":3.9325,"RA":100.9110,"AM":5.8800,"t":"S"},{"DE":46.7054,"RA":104.2336,"AM":5.8800,"t":"S"},{"DE":56.4522,"RA":123.4591,"AM":5.8800,"t":"S"},{"DE":-26.3482,"RA":125.7081,"AM":5.8800,"t":"S"},{"DE":38.0164,"RA":128.2292,"AM":5.8800,"t":"S"},{"DE":-48.5729,"RA":134.4815,"AM":5.8800,"t":"S"},{"DE":-58.3618,"RA":142.5977,"AM":5.8800,"t":"S"},{"DE":68.7477,"RA":155.2641,"AM":5.8800,"t":"S"},{"DE":-16.3537,"RA":164.8789,"AM":5.8800,"t":"S"},{"DE":49.4763,"RA":169.1745,"AM":5.8800,"t":"S"},{"DE":-73.0011,"RA":188.0413,"AM":5.8800,"t":"S"},{"DE":-5.8319,"RA":189.1973,"AM":5.8800,"t":"S"},{"DE":62.7812,"RA":191.8289,"AM":5.8800,"t":"S"},{"DE":-4.9244,"RA":200.8287,"AM":5.8800,"t":"S"},{"DE":46.0281,"RA":201.5691,"AM":5.8800,"t":"S"},{"DE":41.0887,"RA":206.5565,"AM":5.8800,"t":"S"},{"DE":-41.5174,"RA":218.8812,"AM":5.8800,"t":"S"},{"DE":-11.1440,"RA":224.7233,"AM":5.8800,"t":"S"},{"DE":-38.0584,"RA":225.3045,"AM":5.8800,"t":"S"},{"DE":-84.7878,"RA":227.7867,"AM":5.8800,"t":"S"},{"DE":-0.4612,"RA":229.6089,"AM":5.8800,"t":"S"},{"DE":-25.0922,"RA":254.9904,"AM":5.8800,"t":"S"},{"DE":-34.7992,"RA":268.0569,"AM":5.8800,"t":"S"},{"DE":23.6168,"RA":278.1923,"AM":5.8800,"t":"S"},{"DE":-73.9656,"RA":278.2306,"AM":5.8800,"t":"S"},{"DE":52.4257,"RA":287.1076,"AM":5.8800,"t":"S"},{"DE":30.5264,"RA":288.8536,"AM":5.8800,"t":"S"},{"DE":-19.0450,"RA":298.0500,"AM":5.8800,"t":"S"},{"DE":24.8004,"RA":300.4363,"AM":5.8800,"t":"S"},{"DE":71.4318,"RA":316.5974,"AM":5.8800,"t":"S"},{"DE":-14.3997,"RA":325.7683,"AM":5.8800,"t":"S"},{"DE":57.2202,"RA":334.1106,"AM":5.8800,"t":"S"},{"DE":39.7797,"RA":338.1099,"AM":5.8800,"t":"S"},{"DE":-1.5743,"RA":338.5121,"AM":5.8800,"t":"S"},{"DE":-30.6589,"RA":340.0930,"AM":5.8800,"t":"S"},{"DE":-28.0886,"RA":347.4360,"AM":5.8800,"t":"S"},{"DE":30.9356,"RA":5.1017,"AM":5.8900,"t":"S"},{"DE":15.2317,"RA":9.1971,"AM":5.8900,"t":"S"},{"DE":-59.4546,"RA":10.1049,"AM":5.8900,"t":"S"},{"DE":37.2778,"RA":28.9770,"AM":5.8900,"t":"S"},{"DE":21.0586,"RA":29.8987,"AM":5.8900,"t":"S"},{"DE":3.0970,"RA":30.0382,"AM":5.8900,"t":"S"},{"DE":-17.6622,"RA":35.5208,"AM":5.8900,"t":"S"},{"DE":-20.0426,"RA":36.6467,"AM":5.8900,"t":"S"},{"DE":29.9318,"RA":37.2021,"AM":5.8900,"t":"S"},{"DE":25.1881,"RA":42.1912,"AM":5.8900,"t":"S"},{"DE":41.0329,"RA":44.9161,"AM":5.8900,"t":"S"},{"DE":64.0576,"RA":46.8292,"AM":5.8900,"t":"S"},{"DE":18.1940,"RA":60.2032,"AM":5.8900,"t":"S"},{"DE":17.3399,"RA":61.9976,"AM":5.8900,"t":"S"},{"DE":-2.4908,"RA":77.8299,"AM":5.8900,"t":"S"},{"DE":11.5211,"RA":89.2060,"AM":5.8900,"t":"S"},{"DE":1.8371,"RA":89.6018,"AM":5.8900,"t":"S"},{"DE":5.8622,"RA":114.1446,"AM":5.8900,"t":"S"},{"DE":-37.9429,"RA":116.1424,"AM":5.8900,"t":"S"},{"DE":-50.5095,"RA":117.5994,"AM":5.8900,"t":"S"},{"DE":57.7433,"RA":125.1085,"AM":5.8900,"t":"S"},{"DE":-52.1237,"RA":125.7299,"AM":5.8900,"t":"S"},{"DE":67.2974,"RA":127.4427,"AM":5.8900,"t":"S"},{"DE":4.7570,"RA":128.4312,"AM":5.8900,"t":"S"},{"DE":12.1100,"RA":131.7334,"AM":5.8900,"t":"S"},{"DE":-68.6839,"RA":135.2854,"AM":5.8900,"t":"S"},{"DE":32.2523,"RA":135.3505,"AM":5.8900,"t":"S"},{"DE":33.9081,"RA":155.7764,"AM":5.8900,"t":"S"},{"DE":-57.2563,"RA":159.5110,"AM":5.8900,"t":"S"},{"DE":43.2077,"RA":167.4105,"AM":5.8900,"t":"S"},{"DE":-66.9618,"RA":173.0833,"AM":5.8900,"t":"S"},{"DE":-63.2792,"RA":178.7501,"AM":5.8900,"t":"S"},{"DE":-69.1923,"RA":180.6572,"AM":5.8900,"t":"S"},{"DE":21.4592,"RA":181.0692,"AM":5.8900,"t":"S"},{"DE":-60.3762,"RA":193.4538,"AM":5.8900,"t":"S"},{"DE":-44.1520,"RA":193.7440,"AM":5.8900,"t":"S"},{"DE":5.1548,"RA":200.5404,"AM":5.8900,"t":"S"},{"DE":34.6644,"RA":207.7884,"AM":5.8900,"t":"S"},{"DE":-0.8455,"RA":213.4200,"AM":5.8900,"t":"S"},{"DE":-36.6347,"RA":222.1585,"AM":5.8900,"t":"S"},{"DE":-68.3092,"RA":231.5608,"AM":5.8900,"t":"S"},{"DE":28.1567,"RA":237.1434,"AM":5.8900,"t":"S"},{"DE":42.3746,"RA":242.9483,"AM":5.8900,"t":"S"},{"DE":-43.9121,"RA":245.6211,"AM":5.8900,"t":"S"},{"DE":-68.2961,"RA":250.3463,"AM":5.8900,"t":"S"},{"DE":1.2105,"RA":259.1322,"AM":5.8900,"t":"S"},{"DE":-50.0597,"RA":264.3638,"AM":5.8900,"t":"S"},{"DE":-24.3607,"RA":270.9685,"AM":5.8900,"t":"S"},{"DE":-0.9617,"RA":281.6191,"AM":5.8900,"t":"S"},{"DE":19.3287,"RA":282.2224,"AM":5.8900,"t":"S"},{"DE":38.2662,"RA":284.5079,"AM":5.8900,"t":"S"},{"DE":-68.7555,"RA":285.8736,"AM":5.8900,"t":"S"},{"DE":26.6172,"RA":292.8401,"AM":5.8900,"t":"S"},{"DE":-40.0346,"RA":293.5354,"AM":5.8900,"t":"S"},{"DE":54.9738,"RA":294.6715,"AM":5.8900,"t":"S"},{"DE":7.6132,"RA":296.4164,"AM":5.8900,"t":"S"},{"DE":56.0682,"RA":307.3629,"AM":5.8900,"t":"S"},{"DE":-81.2891,"RA":309.5775,"AM":5.8900,"t":"S"},{"DE":-16.0315,"RA":314.4194,"AM":5.8900,"t":"S"},{"DE":38.2375,"RA":319.8424,"AM":5.8900,"t":"S"},{"DE":85.3737,"RA":342.7623,"AM":5.8900,"t":"S"},{"DE":74.2313,"RA":348.6543,"AM":5.8900,"t":"S"},{"DE":-11.6807,"RA":355.2871,"AM":5.8900,"t":"S"},{"DE":7.2505,"RA":355.4862,"AM":5.8900,"t":"S"},{"DE":62.2877,"RA":1.0569,"AM":5.9000,"t":"S"},{"DE":-4.3518,"RA":10.1766,"AM":5.9000,"t":"S"},{"DE":-38.4217,"RA":11.0502,"AM":5.9000,"t":"S"},{"DE":-24.1367,"RA":12.3081,"AM":5.9000,"t":"S"},{"DE":37.2371,"RA":23.5692,"AM":5.9000,"t":"S"},{"DE":18.4605,"RA":23.7044,"AM":5.9000,"t":"S"},{"DE":-51.0921,"RA":35.7278,"AM":5.9000,"t":"S"},{"DE":22.0089,"RA":61.3344,"AM":5.9000,"t":"S"},{"DE":14.7410,"RA":67.0975,"AM":5.9000,"t":"S"},{"DE":-6.0572,"RA":78.2005,"AM":5.9000,"t":"S"},{"DE":31.7015,"RA":88.7458,"AM":5.9000,"t":"S"},{"DE":49.9245,"RA":89.8408,"AM":5.9000,"t":"S"},{"DE":42.9816,"RA":91.2641,"AM":5.9000,"t":"S"},{"DE":9.9566,"RA":104.1076,"AM":5.9000,"t":"S"},{"DE":-9.9475,"RA":108.5647,"AM":5.9000,"t":"S"},{"DE":2.7407,"RA":109.8432,"AM":5.9000,"t":"S"},{"DE":-34.1407,"RA":111.6769,"AM":5.9000,"t":"S"},{"DE":-8.8813,"RA":113.0240,"AM":5.9000,"t":"S"},{"DE":-22.5195,"RA":116.8023,"AM":5.9000,"t":"S"},{"DE":-37.2837,"RA":120.4064,"AM":5.9000,"t":"S"},{"DE":-48.9227,"RA":130.2722,"AM":5.9000,"t":"S"},{"DE":40.2015,"RA":134.1272,"AM":5.9000,"t":"S"},{"DE":-66.7019,"RA":142.1274,"AM":5.9000,"t":"S"},{"DE":31.2778,"RA":145.3963,"AM":5.9000,"t":"S"},{"DE":5.9586,"RA":148.4289,"AM":5.9000,"t":"S"},{"DE":32.3796,"RA":157.9641,"AM":5.9000,"t":"S"},{"DE":-50.7650,"RA":164.2827,"AM":5.9000,"t":"S"},{"DE":1.6504,"RA":169.7290,"AM":5.9000,"t":"S"},{"DE":14.2842,"RA":177.1613,"AM":5.9000,"t":"S"},{"DE":-0.7872,"RA":184.6680,"AM":5.9000,"t":"S"},{"DE":-50.6998,"RA":198.3473,"AM":5.9000,"t":"S"},{"DE":1.0506,"RA":209.1162,"AM":5.9000,"t":"S"},{"DE":18.2984,"RA":219.5583,"AM":5.9000,"t":"S"},{"DE":-38.2906,"RA":221.7712,"AM":5.9000,"t":"S"},{"DE":14.4463,"RA":224.0551,"AM":5.9000,"t":"S"},{"DE":18.9760,"RA":228.0178,"AM":5.9000,"t":"S"},{"DE":60.6702,"RA":231.9643,"AM":5.9000,"t":"S"},{"DE":-23.6063,"RA":241.5266,"AM":5.9000,"t":"S"},{"DE":-50.6304,"RA":261.8019,"AM":5.9000,"t":"S"},{"DE":-29.8169,"RA":276.9562,"AM":5.9000,"t":"S"},{"DE":69.3371,"RA":296.0767,"AM":5.9000,"t":"S"},{"DE":8.5577,"RA":300.2457,"AM":5.9000,"t":"S"},{"DE":36.4547,"RA":307.3350,"AM":5.9000,"t":"S"},{"DE":-40.5915,"RA":347.5405,"AM":5.9000,"t":"S"},{"DE":-22.4574,"RA":347.4796,"AM":5.9000,"t":"S"},{"DE":3.6854,"RA":27.1084,"AM":5.9100,"t":"S"},{"DE":-41.1668,"RA":33.6331,"AM":5.9100,"t":"S"},{"DE":-34.6500,"RA":38.2793,"AM":5.9100,"t":"S"},{"DE":38.7336,"RA":39.2382,"AM":5.9100,"t":"S"},{"DE":26.4624,"RA":45.4756,"AM":5.9100,"t":"S"},{"DE":27.0711,"RA":49.9825,"AM":5.9100,"t":"S"},{"DE":35.4617,"RA":53.1667,"AM":5.9100,"t":"S"},{"DE":6.8035,"RA":56.5390,"AM":5.9100,"t":"S"},{"DE":-29.3382,"RA":56.6143,"AM":5.9100,"t":"S"},{"DE":0.2279,"RA":57.1623,"AM":5.9100,"t":"S"},{"DE":56.5063,"RA":65.4659,"AM":5.9100,"t":"S"},{"DE":20.8214,"RA":65.5947,"AM":5.9100,"t":"S"},{"DE":64.2616,"RA":69.1009,"AM":5.9100,"t":"S"},{"DE":0.7221,"RA":75.4598,"AM":5.9100,"t":"S"},{"DE":13.8511,"RA":93.7853,"AM":5.9100,"t":"S"},{"DE":33.6810,"RA":104.2522,"AM":5.9100,"t":"S"},{"DE":-25.9426,"RA":108.0509,"AM":5.9100,"t":"S"},{"DE":7.1429,"RA":109.9485,"AM":5.9100,"t":"S"},{"DE":58.2482,"RA":122.5158,"AM":5.9100,"t":"S"},{"DE":6.6202,"RA":128.9624,"AM":5.9100,"t":"S"},{"DE":52.7116,"RA":129.8235,"AM":5.9100,"t":"S"},{"DE":-62.2731,"RA":142.1964,"AM":5.9100,"t":"S"},{"DE":-31.8718,"RA":142.8840,"AM":5.9100,"t":"S"},{"DE":-8.4082,"RA":152.5314,"AM":5.9100,"t":"S"},{"DE":-40.3461,"RA":153.4414,"AM":5.9100,"t":"S"},{"DE":-44.6185,"RA":158.1401,"AM":5.9100,"t":"S"},{"DE":69.8539,"RA":163.3798,"AM":5.9100,"t":"S"},{"DE":0.7369,"RA":163.9267,"AM":5.9100,"t":"S"},{"DE":6.1854,"RA":164.0061,"AM":5.9100,"t":"S"},{"DE":-62.9508,"RA":183.0916,"AM":5.9100,"t":"S"},{"DE":-56.3744,"RA":185.4893,"AM":5.9100,"t":"S"},{"DE":-1.5770,"RA":190.9085,"AM":5.9100,"t":"S"},{"DE":-54.9525,"RA":193.2675,"AM":5.9100,"t":"S"},{"DE":16.8486,"RA":197.4494,"AM":5.9100,"t":"S"},{"DE":38.4990,"RA":197.5134,"AM":5.9100,"t":"S"},{"DE":-66.2267,"RA":198.2032,"AM":5.9100,"t":"S"},{"DE":-58.6839,"RA":198.5505,"AM":5.9100,"t":"S"},{"DE":-46.4279,"RA":204.3478,"AM":5.9100,"t":"S"},{"DE":78.0644,"RA":205.6639,"AM":5.9100,"t":"S"},{"DE":28.6481,"RA":208.2929,"AM":5.9100,"t":"S"},{"DE":22.2601,"RA":218.1356,"AM":5.9100,"t":"S"},{"DE":-66.5936,"RA":222.1857,"AM":5.9100,"t":"S"},{"DE":-63.8098,"RA":223.1469,"AM":5.9100,"t":"S"},{"DE":4.5678,"RA":224.8463,"AM":5.9100,"t":"S"},{"DE":60.2045,"RA":225.3629,"AM":5.9100,"t":"S"},{"DE":-37.8630,"RA":241.1535,"AM":5.9100,"t":"S"},{"DE":-33.0111,"RA":243.5932,"AM":5.9100,"t":"S"},{"DE":13.2611,"RA":252.3944,"AM":5.9100,"t":"S"},{"DE":-57.9095,"RA":253.5016,"AM":5.9100,"t":"S"},{"DE":13.6053,"RA":255.9138,"AM":5.9100,"t":"S"},{"DE":-38.1526,"RA":255.9622,"AM":5.9100,"t":"S"},{"DE":-34.9898,"RA":259.7376,"AM":5.9100,"t":"S"},{"DE":-37.2208,"RA":260.7281,"AM":5.9100,"t":"S"},{"DE":1.3050,"RA":268.1477,"AM":5.9100,"t":"S"},{"DE":52.9880,"RA":281.6795,"AM":5.9100,"t":"S"},{"DE":-23.1738,"RA":284.0028,"AM":5.9100,"t":"S"},{"DE":13.9066,"RA":284.6955,"AM":5.9100,"t":"S"},{"DE":-45.1935,"RA":288.6648,"AM":5.9100,"t":"S"},{"DE":57.6451,"RA":290.0667,"AM":5.9100,"t":"S"},{"DE":-29.3094,"RA":291.2668,"AM":5.9100,"t":"S"},{"DE":-47.5574,"RA":297.5586,"AM":5.9100,"t":"S"},{"DE":47.9318,"RA":298.0299,"AM":5.9100,"t":"S"},{"DE":26.4788,"RA":303.0029,"AM":5.9100,"t":"S"},{"DE":66.8537,"RA":304.3788,"AM":5.9100,"t":"S"},{"DE":23.6805,"RA":309.6458,"AM":5.9100,"t":"S"},{"DE":56.4884,"RA":311.0919,"AM":5.9100,"t":"S"},{"DE":-21.5140,"RA":311.5416,"AM":5.9100,"t":"S"},{"DE":78.1264,"RA":316.3717,"AM":5.9100,"t":"S"},{"DE":41.9534,"RA":342.5907,"AM":5.9100,"t":"S"},{"DE":37.0768,"RA":343.7610,"AM":5.9100,"t":"S"},{"DE":43.5442,"RA":347.6135,"AM":5.9100,"t":"S"},{"DE":-1.2476,"RA":353.5376,"AM":5.9100,"t":"S"},{"DE":7.2999,"RA":12.0725,"AM":5.9200,"t":"S"},{"DE":61.0748,"RA":15.9042,"AM":5.9200,"t":"S"},{"DE":-6.9147,"RA":21.0854,"AM":5.9200,"t":"S"},{"DE":-64.3695,"RA":21.2720,"AM":5.9200,"t":"S"},{"DE":-26.2079,"RA":22.5954,"AM":5.9200,"t":"S"},{"DE":11.0434,"RA":27.7165,"AM":5.9200,"t":"S"},{"DE":-35.8436,"RA":42.5616,"AM":5.9200,"t":"S"},{"DE":81.4707,"RA":47.9284,"AM":5.9200,"t":"S"},{"DE":-44.4197,"RA":48.1072,"AM":5.9200,"t":"S"},{"DE":-31.7713,"RA":75.5950,"AM":5.9200,"t":"S"},{"DE":34.3918,"RA":81.7034,"AM":5.9200,"t":"S"},{"DE":-1.4703,"RA":83.5169,"AM":5.9200,"t":"S"},{"DE":19.7496,"RA":88.7362,"AM":5.9200,"t":"S"},{"DE":-10.0815,"RA":97.5470,"AM":5.9200,"t":"S"},{"DE":-27.7696,"RA":97.6929,"AM":5.9200,"t":"S"},{"DE":-31.7937,"RA":101.3457,"AM":5.9200,"t":"S"},{"DE":8.5872,"RA":101.6351,"AM":5.9200,"t":"S"},{"DE":-19.6609,"RA":115.0564,"AM":5.9200,"t":"S"},{"DE":24.0223,"RA":125.1339,"AM":5.9200,"t":"S"},{"DE":-7.5431,"RA":125.7254,"AM":5.9200,"t":"S"},{"DE":-38.8488,"RA":128.4101,"AM":5.9200,"t":"S"},{"DE":9.6556,"RA":129.2741,"AM":5.9200,"t":"S"},{"DE":-48.3591,"RA":133.1609,"AM":5.9200,"t":"S"},{"DE":-47.3384,"RA":138.3936,"AM":5.9200,"t":"S"},{"DE":-22.8639,"RA":143.3586,"AM":5.9200,"t":"S"},{"DE":-1.9589,"RA":162.1690,"AM":5.9200,"t":"S"},{"DE":83.4178,"RA":192.2783,"AM":5.9200,"t":"S"},{"DE":-69.9420,"RA":197.9642,"AM":5.9200,"t":"S"},{"DE":-13.2143,"RA":203.6685,"AM":5.9200,"t":"S"},{"DE":82.7524,"RA":205.5957,"AM":5.9200,"t":"S"},{"DE":38.5036,"RA":206.5795,"AM":5.9200,"t":"S"},{"DE":-50.2493,"RA":206.8651,"AM":5.9200,"t":"S"},{"DE":-50.3696,"RA":209.8228,"AM":5.9200,"t":"S"},{"DE":-77.1606,"RA":225.0472,"AM":5.9200,"t":"S"},{"DE":60.8233,"RA":248.1069,"AM":5.9200,"t":"S"},{"DE":26.9169,"RA":250.4029,"AM":5.9200,"t":"S"},{"DE":45.7725,"RA":299.8351,"AM":5.9200,"t":"S"},{"DE":49.1958,"RA":314.1079,"AM":5.9200,"t":"S"},{"DE":77.0123,"RA":318.9267,"AM":5.9200,"t":"S"},{"DE":-61.8866,"RA":328.7973,"AM":5.9200,"t":"S"},{"DE":-7.1944,"RA":335.8840,"AM":5.9200,"t":"S"},{"DE":14.5164,"RA":340.4894,"AM":5.9200,"t":"S"},{"DE":-44.4892,"RA":349.1658,"AM":5.9200,"t":"S"},{"DE":-22.5086,"RA":1.9454,"AM":5.9300,"t":"S"},{"DE":54.8950,"RA":8.2932,"AM":5.9300,"t":"S"},{"DE":-2.2511,"RA":17.9313,"AM":5.9300,"t":"S"},{"DE":-38.4370,"RA":43.3933,"AM":5.9300,"t":"S"},{"DE":-22.3763,"RA":43.3972,"AM":5.9300,"t":"S"},{"DE":10.8704,"RA":45.1839,"AM":5.9300,"t":"S"},{"DE":48.1770,"RA":48.3495,"AM":5.9300,"t":"S"},{"DE":-28.7971,"RA":49.5108,"AM":5.9300,"t":"S"},{"DE":-27.3175,"RA":51.5938,"AM":5.9300,"t":"S"},{"DE":6.1887,"RA":52.6893,"AM":5.9300,"t":"S"},{"DE":-46.8937,"RA":58.3888,"AM":5.9300,"t":"S"},{"DE":-30.4907,"RA":60.1694,"AM":5.9300,"t":"S"},{"DE":28.0305,"RA":77.4379,"AM":5.9300,"t":"S"},{"DE":15.3604,"RA":82.6090,"AM":5.9300,"t":"S"},{"DE":0.3378,"RA":85.2733,"AM":5.9300,"t":"S"},{"DE":56.1156,"RA":86.6266,"AM":5.9300,"t":"S"},{"DE":-57.1562,"RA":88.0841,"AM":5.9300,"t":"S"},{"DE":-45.0789,"RA":91.1672,"AM":5.9300,"t":"S"},{"DE":22.1903,"RA":92.3852,"AM":5.9300,"t":"S"},{"DE":9.9883,"RA":98.8233,"AM":5.9300,"t":"S"},{"DE":29.3371,"RA":105.8769,"AM":5.9300,"t":"S"},{"DE":52.1311,"RA":109.3905,"AM":5.9300,"t":"S"},{"DE":55.7551,"RA":114.1960,"AM":5.9300,"t":"S"},{"DE":48.7738,"RA":114.4744,"AM":5.9300,"t":"S"},{"DE":23.0185,"RA":115.2438,"AM":5.9300,"t":"S"},{"DE":65.4557,"RA":116.6669,"AM":5.9300,"t":"S"},{"DE":72.9463,"RA":138.9696,"AM":5.9300,"t":"S"},{"DE":-60.4209,"RA":150.5004,"AM":5.9300,"t":"S"},{"DE":-4.0740,"RA":155.8603,"AM":5.9300,"t":"S"},{"DE":-58.5763,"RA":156.2477,"AM":5.9300,"t":"S"},{"DE":-60.5170,"RA":163.8218,"AM":5.9300,"t":"S"},{"DE":-12.3567,"RA":171.7897,"AM":5.9300,"t":"S"},{"DE":-28.4771,"RA":178.9172,"AM":5.9300,"t":"S"},{"DE":-72.1852,"RA":194.1321,"AM":5.9300,"t":"S"},{"DE":-71.4757,"RA":195.7723,"AM":5.9300,"t":"S"},{"DE":-56.2134,"RA":210.8606,"AM":5.9300,"t":"S"},{"DE":-37.0029,"RA":214.8495,"AM":5.9300,"t":"S"},{"DE":13.5343,"RA":220.1766,"AM":5.9300,"t":"S"},{"DE":16.1191,"RA":234.1218,"AM":5.9300,"t":"S"},{"DE":-41.8191,"RA":236.0945,"AM":5.9300,"t":"S"},{"DE":52.9159,"RA":240.5232,"AM":5.9300,"t":"S"},{"DE":3.4545,"RA":242.2453,"AM":5.9300,"t":"S"},{"DE":6.3787,"RA":242.2967,"AM":5.9300,"t":"S"},{"DE":49.0382,"RA":244.7967,"AM":5.9300,"t":"S"},{"DE":-37.2174,"RA":249.7718,"AM":5.9300,"t":"S"},{"DE":-30.4037,"RA":257.1981,"AM":5.9300,"t":"S"},{"DE":-59.6946,"RA":259.8021,"AM":5.9300,"t":"S"},{"DE":-55.1697,"RA":262.1621,"AM":5.9300,"t":"S"},{"DE":-14.7258,"RA":266.9033,"AM":5.9300,"t":"S"},{"DE":-15.8125,"RA":269.0793,"AM":5.9300,"t":"S"},{"DE":-1.0030,"RA":277.9875,"AM":5.9300,"t":"S"},{"DE":-21.3977,"RA":279.4768,"AM":5.9300,"t":"S"},{"DE":32.8128,"RA":282.4413,"AM":5.9300,"t":"S"},{"DE":-51.0186,"RA":285.9898,"AM":5.9300,"t":"S"},{"DE":-15.6604,"RA":286.4216,"AM":5.9300,"t":"S"},{"DE":31.2835,"RA":287.9417,"AM":5.9300,"t":"S"},{"DE":32.4267,"RA":295.6858,"AM":5.9300,"t":"S"},{"DE":-38.5310,"RA":315.6131,"AM":5.9300,"t":"S"},{"DE":53.2859,"RA":315.9484,"AM":5.9300,"t":"S"},{"DE":36.6674,"RA":321.4459,"AM":5.9300,"t":"S"},{"DE":16.0406,"RA":332.9639,"AM":5.9300,"t":"S"},{"DE":41.5491,"RA":340.4001,"AM":5.9300,"t":"S"},{"DE":39.4653,"RA":341.0217,"AM":5.9300,"t":"S"},{"DE":-9.9741,"RA":357.5614,"AM":5.9300,"t":"S"},{"DE":-3.1555,"RA":358.2315,"AM":5.9300,"t":"S"},{"DE":-26.0223,"RA":3.4260,"AM":5.9400,"t":"S"},{"DE":59.9776,"RA":7.5830,"AM":5.9400,"t":"S"},{"DE":-0.5056,"RA":8.8868,"AM":5.9400,"t":"S"},{"DE":-42.6766,"RA":11.2378,"AM":5.9400,"t":"S"},{"DE":-36.5283,"RA":24.6145,"AM":5.9400,"t":"S"},{"DE":37.9529,"RA":27.1621,"AM":5.9400,"t":"S"},{"DE":-50.2061,"RA":27.7269,"AM":5.9400,"t":"S"},{"DE":-1.8254,"RA":32.8993,"AM":5.9400,"t":"S"},{"DE":68.8885,"RA":42.9948,"AM":5.9400,"t":"S"},{"DE":49.0709,"RA":50.4687,"AM":5.9400,"t":"S"},{"DE":13.3983,"RA":62.2565,"AM":5.9400,"t":"S"},{"DE":-61.2382,"RA":66.2723,"AM":5.9400,"t":"S"},{"DE":72.5286,"RA":68.3777,"AM":5.9400,"t":"S"},{"DE":31.1431,"RA":81.1605,"AM":5.9400,"t":"S"},{"DE":61.4812,"RA":99.4230,"AM":5.9400,"t":"S"},{"DE":-36.2303,"RA":102.9268,"AM":5.9400,"t":"S"},{"DE":34.0093,"RA":106.8433,"AM":5.9400,"t":"S"},{"DE":-36.5444,"RA":108.1076,"AM":5.9400,"t":"S"},{"DE":20.2576,"RA":111.7347,"AM":5.9400,"t":"S"},{"DE":-35.2433,"RA":117.3110,"AM":5.9400,"t":"S"},{"DE":18.3322,"RA":125.8410,"AM":5.9400,"t":"S"},{"DE":14.2108,"RA":127.1556,"AM":5.9400,"t":"S"},{"DE":35.3641,"RA":139.6080,"AM":5.9400,"t":"S"},{"DE":43.1732,"RA":172.6298,"AM":5.9400,"t":"S"},{"DE":-7.8275,"RA":173.1981,"AM":5.9400,"t":"S"},{"DE":-67.6204,"RA":174.4519,"AM":5.9400,"t":"S"},{"DE":-22.1757,"RA":185.0449,"AM":5.9400,"t":"S"},{"DE":8.2440,"RA":216.0036,"AM":5.9400,"t":"S"},{"DE":55.4748,"RA":236.6451,"AM":5.9400,"t":"S"},{"DE":-52.2837,"RA":254.1199,"AM":5.9400,"t":"S"},{"DE":-48.8734,"RA":257.9112,"AM":5.9400,"t":"S"},{"DE":34.6958,"RA":261.6923,"AM":5.9400,"t":"S"},{"DE":-15.5710,"RA":264.4009,"AM":5.9400,"t":"S"},{"DE":-40.7725,"RA":267.8856,"AM":5.9400,"t":"S"},{"DE":-36.0198,"RA":271.5988,"AM":5.9400,"t":"S"},{"DE":-18.5832,"RA":307.4746,"AM":5.9400,"t":"S"},{"DE":5.9582,"RA":316.3613,"AM":5.9400,"t":"S"},{"DE":62.4606,"RA":326.2220,"AM":5.9400,"t":"S"},{"DE":-76.1184,"RA":330.7657,"AM":5.9400,"t":"S"},{"DE":53.8459,"RA":340.0767,"AM":5.9400,"t":"S"},{"DE":-4.7115,"RA":345.3821,"AM":5.9400,"t":"S"},{"DE":41.3452,"RA":15.7261,"AM":5.9500,"t":"S"},{"DE":-37.8565,"RA":18.1892,"AM":5.9500,"t":"S"},{"DE":17.4338,"RA":23.9781,"AM":5.9500,"t":"S"},{"DE":67.8246,"RA":41.2070,"AM":5.9500,"t":"S"},{"DE":24.4644,"RA":53.6109,"AM":5.9500,"t":"S"},{"DE":43.9631,"RA":57.2838,"AM":5.9500,"t":"S"},{"DE":-6.4722,"RA":64.3301,"AM":5.9500,"t":"S"},{"DE":41.8081,"RA":65.0601,"AM":5.9500,"t":"S"},{"DE":-19.4589,"RA":67.1626,"AM":5.9500,"t":"S"},{"DE":-35.6535,"RA":67.6680,"AM":5.9500,"t":"S"},{"DE":39.3947,"RA":75.0764,"AM":5.9500,"t":"S"},{"DE":1.1682,"RA":86.6455,"AM":5.9500,"t":"S"},{"DE":-9.0419,"RA":88.0322,"AM":5.9500,"t":"S"},{"DE":-22.8400,"RA":89.0594,"AM":5.9500,"t":"S"},{"DE":-13.3210,"RA":99.1942,"AM":5.9500,"t":"S"},{"DE":-8.4068,"RA":105.0990,"AM":5.9500,"t":"S"},{"DE":-41.4264,"RA":108.7381,"AM":5.9500,"t":"S"},{"DE":-10.5836,"RA":108.9302,"AM":5.9500,"t":"S"},{"DE":-31.8484,"RA":112.2131,"AM":5.9500,"t":"S"},{"DE":-54.3994,"RA":112.6288,"AM":5.9500,"t":"S"},{"DE":3.6248,"RA":115.3965,"AM":5.9500,"t":"S"},{"DE":-12.6322,"RA":124.5998,"AM":5.9500,"t":"S"},{"DE":-64.6006,"RA":126.4650,"AM":5.9500,"t":"S"},{"DE":-26.8435,"RA":128.8696,"AM":5.9500,"t":"S"},{"DE":-16.7087,"RA":134.1422,"AM":5.9500,"t":"S"},{"DE":26.6291,"RA":137.1972,"AM":5.9500,"t":"S"},{"DE":33.8822,"RA":137.2129,"AM":5.9500,"t":"S"},{"DE":-13.5168,"RA":143.2324,"AM":5.9500,"t":"S"},{"DE":-37.1868,"RA":147.3671,"AM":5.9500,"t":"S"},{"DE":-51.1467,"RA":148.4588,"AM":5.9500,"t":"S"},{"DE":23.5031,"RA":154.1346,"AM":5.9500,"t":"S"},{"DE":67.4114,"RA":161.2668,"AM":5.9500,"t":"S"},{"DE":-3.0927,"RA":162.7725,"AM":5.9500,"t":"S"},{"DE":-61.8266,"RA":163.6233,"AM":5.9500,"t":"S"},{"DE":-0.0008,"RA":165.9025,"AM":5.9500,"t":"S"},{"DE":16.7969,"RA":173.6770,"AM":5.9500,"t":"S"},{"DE":-53.9686,"RA":175.1770,"AM":5.9500,"t":"S"},{"DE":33.1670,"RA":179.8231,"AM":5.9500,"t":"S"},{"DE":-60.9683,"RA":181.2385,"AM":5.9500,"t":"S"},{"DE":-65.7095,"RA":181.5961,"AM":5.9500,"t":"S"},{"DE":1.8979,"RA":182.4221,"AM":5.9500,"t":"S"},{"DE":-11.6106,"RA":186.2990,"AM":5.9500,"t":"S"},{"DE":39.2789,"RA":191.2478,"AM":5.9500,"t":"S"},{"DE":-10.3293,"RA":197.4387,"AM":5.9500,"t":"S"},{"DE":-82.6662,"RA":208.9124,"AM":5.9500,"t":"S"},{"DE":-59.9083,"RA":234.9859,"AM":5.9500,"t":"S"},{"DE":-76.0820,"RA":235.4779,"AM":5.9500,"t":"S"},{"DE":-19.3829,"RA":238.7515,"AM":5.9500,"t":"S"},{"DE":-67.9413,"RA":244.2727,"AM":5.9500,"t":"S"},{"DE":-43.0510,"RA":253.4268,"AM":5.9500,"t":"S"},{"DE":-35.9341,"RA":255.1541,"AM":5.9500,"t":"S"},{"DE":-32.4383,"RA":258.2440,"AM":5.9500,"t":"S"},{"DE":-38.5939,"RA":258.8999,"AM":5.9500,"t":"S"},{"DE":0.0667,"RA":269.2680,"AM":5.9500,"t":"S"},{"DE":-80.2327,"RA":277.3334,"AM":5.9500,"t":"S"},{"DE":-48.2991,"RA":286.7317,"AM":5.9500,"t":"S"},{"DE":-37.7017,"RA":300.0664,"AM":5.9500,"t":"S"},{"DE":41.0260,"RA":305.6887,"AM":5.9500,"t":"S"},{"DE":-14.4831,"RA":314.6743,"AM":5.9500,"t":"S"},{"DE":-27.1073,"RA":337.4417,"AM":5.9500,"t":"S"},{"DE":-15.2460,"RA":353.7057,"AM":5.9500,"t":"S"},{"DE":75.2929,"RA":354.7923,"AM":5.9500,"t":"S"},{"DE":66.7822,"RA":356.6530,"AM":5.9500,"t":"S"},{"DE":28.8424,"RA":357.4141,"AM":5.9500,"t":"S"},{"DE":-62.9566,"RA":359.3326,"AM":5.9500,"t":"S"},{"DE":-77.4269,"RA":5.3698,"AM":5.9600,"t":"S"},{"DE":51.9334,"RA":27.7380,"AM":5.9600,"t":"S"},{"DE":-0.3403,"RA":30.9507,"AM":5.9600,"t":"S"},{"DE":24.1678,"RA":33.1564,"AM":5.9600,"t":"S"},{"DE":-69.3364,"RA":51.4011,"AM":5.9600,"t":"S"},{"DE":75.9412,"RA":72.2095,"AM":5.9600,"t":"S"},{"DE":-18.1301,"RA":79.7103,"AM":5.9600,"t":"S"},{"DE":-6.5740,"RA":84.6582,"AM":5.9600,"t":"S"},{"DE":4.4234,"RA":87.5544,"AM":5.9600,"t":"S"},{"DE":19.8678,"RA":88.0975,"AM":5.9600,"t":"S"},{"DE":3.6024,"RA":104.7376,"AM":5.9600,"t":"S"},{"DE":17.7555,"RA":105.6064,"AM":5.9600,"t":"S"},{"DE":9.1384,"RA":105.8247,"AM":5.9600,"t":"S"},{"DE":-51.9683,"RA":106.8054,"AM":5.9600,"t":"S"},{"DE":-52.4992,"RA":108.8385,"AM":5.9600,"t":"S"},{"DE":-50.5904,"RA":121.1767,"AM":5.9600,"t":"S"},{"DE":22.6355,"RA":121.5767,"AM":5.9600,"t":"S"},{"DE":-57.9732,"RA":125.3004,"AM":5.9600,"t":"S"},{"DE":-14.9297,"RA":126.4816,"AM":5.9600,"t":"S"},{"DE":32.8020,"RA":129.5791,"AM":5.9600,"t":"S"},{"DE":45.3128,"RA":133.0490,"AM":5.9600,"t":"S"},{"DE":28.3308,"RA":133.1494,"AM":5.9600,"t":"S"},{"DE":46.8172,"RA":139.3799,"AM":5.9600,"t":"S"},{"DE":-36.0960,"RA":144.3684,"AM":5.9600,"t":"S"},{"DE":67.2722,"RA":144.8663,"AM":5.9600,"t":"S"},{"DE":-58.8169,"RA":159.7486,"AM":5.9600,"t":"S"},{"DE":-32.8313,"RA":173.6232,"AM":5.9600,"t":"S"},{"DE":-63.5058,"RA":187.9839,"AM":5.9600,"t":"S"},{"DE":-44.1432,"RA":204.2751,"AM":5.9600,"t":"S"},{"DE":-41.4010,"RA":205.7293,"AM":5.9600,"t":"S"},{"DE":-42.0675,"RA":205.9170,"AM":5.9600,"t":"S"},{"DE":-66.2689,"RA":210.2189,"AM":5.9600,"t":"S"},{"DE":-51.5047,"RA":212.3960,"AM":5.9600,"t":"S"},{"DE":0.8289,"RA":217.4605,"AM":5.9600,"t":"S"},{"DE":-48.0737,"RA":228.9736,"AM":5.9600,"t":"S"},{"DE":-53.1523,"RA":251.1656,"AM":5.9600,"t":"S"},{"DE":-20.3880,"RA":273.8040,"AM":5.9600,"t":"S"},{"DE":68.7558,"RA":273.8211,"AM":5.9600,"t":"S"},{"DE":-19.2457,"RA":285.7659,"AM":5.9600,"t":"S"},{"DE":13.5481,"RA":305.0008,"AM":5.9600,"t":"S"},{"DE":81.0913,"RA":307.3640,"AM":5.9600,"t":"S"},{"DE":44.9247,"RA":314.1449,"AM":5.9600,"t":"S"},{"DE":45.3746,"RA":324.0103,"AM":5.9600,"t":"S"},{"DE":-14.7494,"RA":326.0040,"AM":5.9600,"t":"S"},{"DE":14.7719,"RA":326.1305,"AM":5.9600,"t":"S"},{"DE":62.6980,"RA":329.7230,"AM":5.9600,"t":"S"},{"DE":-13.3050,"RA":334.7531,"AM":5.9600,"t":"S"},{"DE":-18.0754,"RA":349.8504,"AM":5.9600,"t":"S"},{"DE":47.6537,"RA":225.9487,"AM":5.9600,"t":"S"},{"DE":30.2862,"RA":230.7995,"AM":5.9600,"t":"S"},{"DE":66.3518,"RA":14.6293,"AM":5.9700,"t":"S"},{"DE":2.4457,"RA":17.6398,"AM":5.9700,"t":"S"},{"DE":16.1335,"RA":18.5318,"AM":5.9700,"t":"S"},{"DE":20.4690,"RA":20.8540,"AM":5.9700,"t":"S"},{"DE":30.0471,"RA":25.4135,"AM":5.9700,"t":"S"},{"DE":13.4767,"RA":30.6462,"AM":5.9700,"t":"S"},{"DE":8.3816,"RA":44.0574,"AM":5.9700,"t":"S"},{"DE":11.8726,"RA":47.6616,"AM":5.9700,"t":"S"},{"DE":39.2834,"RA":49.4406,"AM":5.9700,"t":"S"},{"DE":-5.6262,"RA":54.7547,"AM":5.9700,"t":"S"},{"DE":17.3271,"RA":58.2918,"AM":5.9700,"t":"S"},{"DE":19.0420,"RA":66.2380,"AM":5.9700,"t":"S"},{"DE":38.2802,"RA":70.4592,"AM":5.9700,"t":"S"},{"DE":27.8975,"RA":73.1963,"AM":5.9700,"t":"S"},{"DE":-12.4913,"RA":76.8540,"AM":5.9700,"t":"S"},{"DE":11.0350,"RA":84.2683,"AM":5.9700,"t":"S"},{"DE":-6.7962,"RA":85.7246,"AM":5.9700,"t":"S"},{"DE":-4.0946,"RA":87.1456,"AM":5.9700,"t":"S"},{"DE":2.0247,"RA":87.6251,"AM":5.9700,"t":"S"},{"DE":9.5094,"RA":89.1168,"AM":5.9700,"t":"S"},{"DE":-16.6180,"RA":94.0320,"AM":5.9700,"t":"S"},{"DE":-42.7698,"RA":126.2384,"AM":5.9700,"t":"S"},{"DE":57.4182,"RA":149.3066,"AM":5.9700,"t":"S"},{"DE":-41.6685,"RA":154.6177,"AM":5.9700,"t":"S"},{"DE":-79.7833,"RA":160.4649,"AM":5.9700,"t":"S"},{"DE":17.1231,"RA":195.2901,"AM":5.9700,"t":"S"},{"DE":-1.1925,"RA":201.5476,"AM":5.9700,"t":"S"},{"DE":25.7022,"RA":206.6805,"AM":5.9700,"t":"S"},{"DE":61.4893,"RA":207.4394,"AM":5.9700,"t":"S"},{"DE":-30.9185,"RA":226.6383,"AM":5.9700,"t":"S"},{"DE":53.9221,"RA":233.8175,"AM":5.9700,"t":"S"},{"DE":-14.8728,"RA":244.7517,"AM":5.9700,"t":"S"},{"DE":38.8114,"RA":259.5970,"AM":5.9700,"t":"S"},{"DE":6.3132,"RA":265.3847,"AM":5.9700,"t":"S"},{"DE":-57.5455,"RA":266.2327,"AM":5.9700,"t":"S"},{"DE":54.2866,"RA":272.6316,"AM":5.9700,"t":"S"},{"DE":-23.4291,"RA":295.0299,"AM":5.9700,"t":"S"},{"DE":-0.6782,"RA":302.0076,"AM":5.9700,"t":"S"},{"DE":43.4589,"RA":310.0132,"AM":5.9700,"t":"S"},{"DE":-36.4235,"RA":318.3290,"AM":5.9700,"t":"S"},{"DE":11.2034,"RA":319.7168,"AM":5.9700,"t":"S"},{"DE":80.5248,"RA":321.2059,"AM":5.9700,"t":"S"},{"DE":-33.9446,"RA":323.0607,"AM":5.9700,"t":"S"},{"DE":-26.8224,"RA":331.1532,"AM":5.9700,"t":"S"},{"DE":24.9506,"RA":333.0337,"AM":5.9700,"t":"S"},{"DE":-23.9911,"RA":338.9016,"AM":5.9700,"t":"S"},{"DE":-20.8707,"RA":345.6844,"AM":5.9700,"t":"S"},{"DE":21.1343,"RA":346.8696,"AM":5.9700,"t":"S"},{"DE":58.4367,"RA":1.5653,"AM":5.9800,"t":"S"},{"DE":6.7410,"RA":11.8485,"AM":5.9800,"t":"S"},{"DE":43.4577,"RA":21.5778,"AM":5.9800,"t":"S"},{"DE":16.4059,"RA":24.9201,"AM":5.9800,"t":"S"},{"DE":-14.5493,"RA":40.3922,"AM":5.9800,"t":"S"},{"DE":32.1840,"RA":49.1466,"AM":5.9800,"t":"S"},{"DE":-47.3751,"RA":52.6539,"AM":5.9800,"t":"S"},{"DE":54.9749,"RA":53.4128,"AM":5.9800,"t":"S"},{"DE":-8.7943,"RA":70.8948,"AM":5.9800,"t":"S"},{"DE":0.4672,"RA":73.7113,"AM":5.9800,"t":"S"},{"DE":-27.3689,"RA":79.8487,"AM":5.9800,"t":"S"},{"DE":29.2152,"RA":84.8263,"AM":5.9800,"t":"S"},{"DE":48.9594,"RA":90.4294,"AM":5.9800,"t":"S"},{"DE":-5.7750,"RA":111.4633,"AM":5.9800,"t":"S"},{"DE":-22.8592,"RA":111.9289,"AM":5.9800,"t":"S"},{"DE":-45.2158,"RA":119.7575,"AM":5.9800,"t":"S"},{"DE":-46.3317,"RA":127.4402,"AM":5.9800,"t":"S"},{"DE":42.0027,"RA":133.0418,"AM":5.9800,"t":"S"},{"DE":34.6335,"RA":138.8094,"AM":5.9800,"t":"S"},{"DE":-41.7152,"RA":152.6571,"AM":5.9800,"t":"S"},{"DE":-58.6667,"RA":158.1992,"AM":5.9800,"t":"S"},{"DE":-59.9192,"RA":162.0225,"AM":5.9800,"t":"S"},{"DE":-37.1902,"RA":175.8633,"AM":5.9800,"t":"S"},{"DE":-59.8605,"RA":196.8513,"AM":5.9800,"t":"S"},{"DE":34.9890,"RA":205.6809,"AM":5.9800,"t":"S"},{"DE":8.8949,"RA":210.3351,"AM":5.9800,"t":"S"},{"DE":-38.7925,"RA":227.5305,"AM":5.9800,"t":"S"},{"DE":31.7878,"RA":228.5252,"AM":5.9800,"t":"S"},{"DE":13.7891,"RA":237.0554,"AM":5.9800,"t":"S"},{"DE":-48.6478,"RA":255.1124,"AM":5.9800,"t":"S"},{"DE":-37.2276,"RA":256.5841,"AM":5.9800,"t":"S"},{"DE":-17.6091,"RA":257.0619,"AM":5.9800,"t":"S"},{"DE":-14.5841,"RA":258.8345,"AM":5.9800,"t":"S"},{"DE":-29.7246,"RA":261.9065,"AM":5.9800,"t":"S"},{"DE":-36.7783,"RA":262.2337,"AM":5.9800,"t":"S"},{"DE":-35.9014,"RA":271.2099,"AM":5.9800,"t":"S"},{"DE":33.4471,"RA":272.9380,"AM":5.9800,"t":"S"},{"DE":-66.6536,"RA":285.0148,"AM":5.9800,"t":"S"},{"DE":-68.4339,"RA":292.7956,"AM":5.9800,"t":"S"},{"DE":11.2732,"RA":294.2185,"AM":5.9800,"t":"S"},{"DE":13.8157,"RA":295.2730,"AM":5.9800,"t":"S"},{"DE":7.5162,"RA":315.0166,"AM":5.9800,"t":"S"},{"DE":35.5102,"RA":325.5045,"AM":5.9800,"t":"S"},{"DE":-4.2669,"RA":332.6406,"AM":5.9800,"t":"S"},{"DE":-57.4223,"RA":340.2037,"AM":5.9800,"t":"S"},{"DE":41.7737,"RA":349.5972,"AM":5.9800,"t":"S"},{"DE":74.0026,"RA":354.8382,"AM":5.9800,"t":"S"},{"DE":-8.8241,"RA":2.0731,"AM":5.9900,"t":"S"},{"DE":-25.5472,"RA":6.8113,"AM":5.9900,"t":"S"},{"DE":-60.2628,"RA":10.6741,"AM":5.9900,"t":"S"},{"DE":33.9509,"RA":14.5592,"AM":5.9900,"t":"S"},{"DE":52.5022,"RA":16.0099,"AM":5.9900,"t":"S"},{"DE":57.5163,"RA":34.5191,"AM":5.9900,"t":"S"},{"DE":-73.6458,"RA":35.7184,"AM":5.9900,"t":"S"},{"DE":-38.3837,"RA":40.5275,"AM":5.9900,"t":"S"},{"DE":-12.0991,"RA":58.8172,"AM":5.9900,"t":"S"},{"DE":18.7347,"RA":71.5701,"AM":5.9900,"t":"S"},{"DE":40.3126,"RA":71.6853,"AM":5.9900,"t":"S"},{"DE":34.3123,"RA":79.0756,"AM":5.9900,"t":"S"},{"DE":-8.4156,"RA":80.8271,"AM":5.9900,"t":"S"},{"DE":41.4620,"RA":82.7027,"AM":5.9900,"t":"S"},{"DE":-3.5647,"RA":84.8798,"AM":5.9900,"t":"S"},{"DE":0.9686,"RA":88.6835,"AM":5.9900,"t":"S"},{"DE":-18.4772,"RA":93.8238,"AM":5.9900,"t":"S"},{"DE":-4.9147,"RA":93.8736,"AM":5.9900,"t":"S"},{"DE":12.9828,"RA":99.9488,"AM":5.9900,"t":"S"},{"DE":-22.6742,"RA":108.3501,"AM":5.9900,"t":"S"},{"DE":0.1771,"RA":110.5145,"AM":5.9900,"t":"S"},{"DE":-37.5794,"RA":114.9916,"AM":5.9900,"t":"S"},{"DE":16.4553,"RA":120.3762,"AM":5.9900,"t":"S"},{"DE":-61.6489,"RA":141.0229,"AM":5.9900,"t":"S"},{"DE":-55.2138,"RA":145.4497,"AM":5.9900,"t":"S"},{"DE":-70.7203,"RA":163.4255,"AM":5.9900,"t":"S"},{"DE":36.0931,"RA":164.8866,"AM":5.9900,"t":"S"},{"DE":-64.5825,"RA":169.8195,"AM":5.9900,"t":"S"},{"DE":-56.1762,"RA":190.7883,"AM":5.9900,"t":"S"},{"DE":-39.6804,"RA":192.9872,"AM":5.9900,"t":"S"},{"DE":-3.3685,"RA":195.1498,"AM":5.9900,"t":"S"},{"DE":-53.1762,"RA":215.9525,"AM":5.9900,"t":"S"},{"DE":-38.8697,"RA":217.7952,"AM":5.9900,"t":"S"},{"DE":62.0471,"RA":230.6552,"AM":5.9900,"t":"S"},{"DE":77.5140,"RA":250.7757,"AM":5.9900,"t":"S"},{"DE":-28.5097,"RA":251.2508,"AM":5.9900,"t":"S"},{"DE":47.4167,"RA":253.3232,"AM":5.9900,"t":"S"},{"DE":-63.2697,"RA":253.8528,"AM":5.9900,"t":"S"},{"DE":23.7428,"RA":258.9228,"AM":5.9900,"t":"S"},{"DE":-56.9210,"RA":262.8470,"AM":5.9900,"t":"S"},{"DE":-28.7591,"RA":269.6627,"AM":5.9900,"t":"S"},{"DE":-3.0074,"RA":274.2213,"AM":5.9900,"t":"S"},{"DE":12.0297,"RA":275.6472,"AM":5.9900,"t":"S"},{"DE":-5.9129,"RA":282.4206,"AM":5.9900,"t":"S"},{"DE":33.9686,"RA":283.7188,"AM":5.9900,"t":"S"},{"DE":50.5251,"RA":295.4542,"AM":5.9900,"t":"S"},{"DE":18.5010,"RA":300.8183,"AM":5.9900,"t":"S"},{"DE":15.8382,"RA":309.7707,"AM":5.9900,"t":"S"},{"DE":-76.1806,"RA":310.5110,"AM":5.9900,"t":"S"},{"DE":-5.6266,"RA":312.8573,"AM":5.9900,"t":"S"},{"DE":75.9256,"RA":313.6846,"AM":5.9900,"t":"S"},{"DE":-9.3193,"RA":320.7344,"AM":5.9900,"t":"S"},{"DE":-47.2108,"RA":340.6537,"AM":5.9900,"t":"S"},{"DE":-29.5363,"RA":342.8373,"AM":5.9900,"t":"S"},{"DE":25.1673,"RA":351.9183,"AM":5.9900,"t":"S"},{"DE":-76.8696,"RA":354.5989,"AM":5.9900,"t":"S"},{"DE":9.6773,"RA":354.9793,"AM":5.9900,"t":"S"},{"DE":-44.7963,"RA":9.9664,"AM":6.0000,"t":"S"},{"DE":64.9015,"RA":30.7187,"AM":6.0000,"t":"S"},{"DE":-10.0522,"RA":32.8426,"AM":6.0000,"t":"S"},{"DE":0.2557,"RA":37.6883,"AM":6.0000,"t":"S"},{"DE":15.0346,"RA":38.2256,"AM":6.0000,"t":"S"},{"DE":-20.7153,"RA":64.5670,"AM":6.0000,"t":"S"},{"DE":20.9820,"RA":65.8849,"AM":6.0000,"t":"S"},{"DE":61.1698,"RA":76.6237,"AM":6.0000,"t":"S"},{"DE":15.8225,"RA":86.6896,"AM":6.0000,"t":"S"},{"DE":-39.2644,"RA":94.1483,"AM":6.0000,"t":"S"},{"DE":12.5702,"RA":95.6516,"AM":6.0000,"t":"S"},{"DE":22.6375,"RA":106.3265,"AM":6.0000,"t":"S"},{"DE":-16.2345,"RA":107.3890,"AM":6.0000,"t":"S"},{"DE":-26.9638,"RA":110.2288,"AM":6.0000,"t":"S"},{"DE":-46.2643,"RA":123.1283,"AM":6.0000,"t":"S"},{"DE":72.4072,"RA":125.1680,"AM":6.0000,"t":"S"},{"DE":-42.0898,"RA":132.5876,"AM":6.0000,"t":"S"},{"DE":48.3968,"RA":154.8618,"AM":6.0000,"t":"S"},{"DE":-65.7047,"RA":156.8556,"AM":6.0000,"t":"S"},{"DE":41.6010,"RA":156.8669,"AM":6.0000,"t":"S"},{"DE":81.7098,"RA":182.7503,"AM":6.0000,"t":"S"},{"DE":-41.7359,"RA":187.4912,"AM":6.0000,"t":"S"},{"DE":-18.2501,"RA":189.6859,"AM":6.0000,"t":"S"},{"DE":-11.6486,"RA":193.5778,"AM":6.0000,"t":"S"},{"DE":75.4725,"RA":194.6971,"AM":6.0000,"t":"S"},{"DE":21.1534,"RA":196.5885,"AM":6.0000,"t":"S"},{"DE":-55.8007,"RA":200.2014,"AM":6.0000,"t":"S"},{"DE":-57.6227,"RA":204.7040,"AM":6.0000,"t":"S"},{"DE":-56.7680,"RA":205.7338,"AM":6.0000,"t":"S"},{"DE":5.4972,"RA":207.6028,"AM":6.0000,"t":"S"},{"DE":-54.7047,"RA":209.1373,"AM":6.0000,"t":"S"},{"DE":26.6773,"RA":218.0843,"AM":6.0000,"t":"S"},{"DE":19.1528,"RA":223.3491,"AM":6.0000,"t":"S"},{"DE":16.0246,"RA":235.2462,"AM":6.0000,"t":"S"},{"DE":-47.0608,"RA":237.8810,"AM":6.0000,"t":"S"},{"DE":-32.0005,"RA":240.8932,"AM":6.0000,"t":"S"},{"DE":0.7026,"RA":256.3201,"AM":6.0000,"t":"S"},{"DE":17.3179,"RA":259.5206,"AM":6.0000,"t":"S"},{"DE":51.8182,"RA":265.3408,"AM":6.0000,"t":"S"},{"DE":-34.7527,"RA":268.4782,"AM":6.0000,"t":"S"},{"DE":52.1961,"RA":279.9701,"AM":6.0000,"t":"S"},{"DE":-16.2293,"RA":286.7172,"AM":6.0000,"t":"S"},{"DE":49.2623,"RA":293.4234,"AM":6.0000,"t":"S"},{"DE":25.3841,"RA":296.9522,"AM":6.0000,"t":"S"},{"DE":-10.8708,"RA":297.2592,"AM":6.0000,"t":"S"},{"DE":55.7980,"RA":319.3093,"AM":6.0000,"t":"S"},{"DE":-9.2759,"RA":326.5678,"AM":6.0000,"t":"S"},{"DE":6.7174,"RA":330.0330,"AM":6.0000,"t":"S"},{"DE":31.8400,"RA":336.9427,"AM":6.0000,"t":"S"},{"DE":-63.0312,"RA":8.1847,"AM":6.0000,"t":"S"},{"DE":2.4983,"RA":271.3649,"AM":6.0000,"t":"S"}];
var constellation_lines = [{"r0":298.8283,"d0":6.4068,"r1":297.6958,"d1":8.8683},{"r0":297.6958,"d0":8.8683,"r1":296.5649,"d1":10.6133},{"r0":297.6958,"d0":8.8683,"r1":291.3746,"d1":3.1148},{"r0":291.3746,"d0":3.1148,"r1":298.1182,"d1":1.0057},{"r0":302.8262,"d0":-0.8215,"r1":298.1182,"d1":1.0057},{"r0":291.3746,"d0":3.1148,"r1":286.3525,"d1":13.8635},{"r0":286.3525,"d0":13.8635,"r1":284.9057,"d1":15.0683},{"r0":291.3746,"d0":3.1148,"r1":286.5623,"d1":-4.8826},{"r0":2.0969,"d0":29.0904,"r1":9.8319,"d1":30.8610},{"r0":9.8319,"d0":30.8610,"r1":17.4329,"d1":35.6206},{"r0":30.9748,"d0":42.3297,"r1":17.4329,"d1":35.6206},{"r0":17.4329,"d0":35.6206,"r1":14.1883,"d1":38.4993},{"r0":14.1883,"d0":38.4993,"r1":12.4535,"d1":41.0789},{"r0":353.2427,"d0":-37.8183,"r1":14.6515,"d1":-29.3574},{"r0":14.6515,"d0":-29.3574,"r1":349.7060,"d1":-32.5320},{"r0":349.7060,"d0":-32.5320,"r1":353.2427,"d1":-37.8183},{"r0":271.6578,"d0":-50.0915,"r1":262.9604,"d1":-49.8761},{"r0":262.9604,"d0":-49.8761,"r1":254.6551,"d1":-55.9901},{"r0":254.6551,"d0":-55.9901,"r1":252.4464,"d1":-59.0414},{"r0":252.4464,"d0":-59.0414,"r1":262.7748,"d1":-60.6838},{"r0":262.7748,"d0":-60.6838,"r1":261.3486,"d1":-56.3777},{"r0":261.3486,"d0":-56.3777,"r1":261.3250,"d1":-55.5299},{"r0":261.3250,"d0":-55.5299,"r1":271.6578,"d1":-50.0915},{"r0":238.4564,"d0":-16.7293,"r1":233.8816,"d1":-14.7895},{"r0":233.8816,"d0":-14.7895,"r1":229.2517,"d1":-9.3829},{"r0":229.2517,"d0":-9.3829,"r1":222.7197,"d1":-16.0418},{"r0":222.7197,"d0":-16.0418,"r1":226.0176,"d1":-25.2820},{"r0":226.0176,"d0":-25.2820,"r1":233.8816,"d1":-14.7895},{"r0":33.2500,"d0":8.8467,"r1":37.0398,"d1":8.4601},{"r0":26.0172,"d0":-15.9375,"r1":10.8973,"d1":-17.9866},{"r0":10.8973,"d0":-17.9866,"r1":4.8570,"d1":-8.8239},{"r0":10.8973,"d0":-17.9866,"r1":17.1475,"d1":-10.1823},{"r0":17.1475,"d0":-10.1823,"r1":21.0058,"d1":-8.1833},{"r0":21.0058,"d0":-8.1833,"r1":27.8651,"d1":-10.3350},{"r0":27.8651,"d0":-10.3350,"r1":36.4875,"d1":-12.2905},{"r0":36.4875,"d0":-12.2905,"r1":39.8910,"d1":-11.8722},{"r0":39.8910,"d0":-11.8722,"r1":41.0306,"d1":-13.8587},{"r0":41.0306,"d0":-13.8587,"r1":38.0218,"d1":-15.2447},{"r0":38.0218,"d0":-15.2447,"r1":26.0172,"d1":-15.9375},{"r0":34.8366,"d0":-2.9776,"r1":39.8910,"d1":-11.8722},{"r0":34.8366,"d0":-2.9776,"r1":39.8707,"d1":0.3285},{"r0":39.8707,"d0":0.3285,"r1":40.8252,"d1":3.2358},{"r0":40.8252,"d0":3.2358,"r1":45.5699,"d1":4.0897},{"r0":45.5699,"d0":4.0897,"r1":44.9288,"d1":8.9074},{"r0":44.9288,"d0":8.9074,"r1":41.2356,"d1":10.1141},{"r0":41.2356,"d0":10.1141,"r1":37.0398,"d1":8.4601},{"r0":37.0398,"d0":8.4601,"r1":38.9686,"d1":5.5932},{"r0":38.9686,"d0":5.5932,"r1":40.8252,"d1":3.2358},{"r0":42.4959,"d0":27.2605,"r1":31.7933,"d1":23.4624},{"r0":31.7933,"d0":23.4624,"r1":28.6600,"d1":20.8080},{"r0":28.6600,"d0":20.8080,"r1":28.3825,"d1":19.2939},{"r0":281.7936,"d0":-4.7479,"r1":281.8706,"d1":-5.7051},{"r0":281.8706,"d0":-5.7051,"r1":283.6796,"d1":-15.6030},{"r0":283.6796,"d0":-15.6030,"r1":277.2994,"d1":-14.5658},{"r0":277.2994,"d0":-14.5658,"r1":278.8018,"d1":-8.2441},{"r0":278.8018,"d0":-8.2441,"r1":281.7936,"d1":-4.7479},{"r0":130.0256,"d0":-35.3084,"r1":130.8981,"d1":-33.1864},{"r0":130.8981,"d0":-33.1864,"r1":132.6331,"d1":-27.7098},{"r0":220.2873,"d0":13.7283,"r1":213.9154,"d1":19.1824},{"r0":213.9154,"d0":19.1824,"r1":221.2468,"d1":27.0742},{"r0":221.2468,"d0":27.0742,"r1":228.8756,"d1":33.3148},{"r0":228.8756,"d0":33.3148,"r1":225.4865,"d1":40.3906},{"r0":225.4865,"d0":40.3906,"r1":218.0195,"d1":38.3083},{"r0":218.0195,"d0":38.3083,"r1":217.9575,"d1":30.3714},{"r0":217.9575,"d0":30.3714,"r1":213.9154,"d1":19.1824},{"r0":213.9154,"d0":19.1824,"r1":208.6712,"d1":18.3977},{"r0":208.6712,"d0":18.3977,"r1":207.3693,"d1":15.7979},{"r0":67.7087,"d0":-44.9537,"r1":70.1406,"d1":-41.8638},{"r0":70.1406,"d0":-41.8638,"r1":70.5145,"d1":-37.1443},{"r0":124.6305,"d0":-76.9197,"r1":158.8675,"d1":-78.6078},{"r0":158.8675,"d0":-78.6078,"r1":184.5872,"d1":-79.3122},{"r0":131.6743,"d0":28.7599,"r1":130.8215,"d1":21.4685},{"r0":130.8215,"d0":21.4685,"r1":125.0161,"d1":27.2177},{"r0":130.8215,"d0":21.4685,"r1":131.1712,"d1":18.1543},{"r0":131.1712,"d0":18.1543,"r1":124.1288,"d1":9.1855},{"r0":131.1712,"d0":18.1543,"r1":134.6218,"d1":11.8577},{"r0":304.5136,"d0":-12.5449,"r1":305.2528,"d1":-14.7814},{"r0":305.2528,"d0":-14.7814,"r1":316.4868,"d1":-17.2329},{"r0":316.4868,"d0":-17.2329,"r1":320.5616,"d1":-16.8345},{"r0":320.5616,"d0":-16.8345,"r1":325.0227,"d1":-16.6623},{"r0":325.0227,"d0":-16.6623,"r1":326.7602,"d1":-16.1273},{"r0":320.5616,"d0":-16.8345,"r1":321.6668,"d1":-22.4113},{"r0":321.6668,"d0":-22.4113,"r1":316.4868,"d1":-17.2329},{"r0":305.2528,"d0":-14.7814,"r1":311.5239,"d1":-25.2709},{"r0":316.4868,"d0":-17.2329,"r1":312.9554,"d1":-26.9191},{"r0":138.3006,"d0":-69.7172,"r1":153.4344,"d1":-70.0379},{"r0":153.4344,"d0":-70.0379,"r1":160.7392,"d1":-64.3945},{"r0":160.7392,"d0":-64.3945,"r1":160.8846,"d1":-60.5666},{"r0":160.8846,"d0":-60.5666,"r1":167.1475,"d1":-58.9750},{"r0":167.1475,"d0":-58.9750,"r1":163.3734,"d1":-58.8532},{"r0":163.3734,"d0":-58.8532,"r1":156.9697,"d1":-58.7394},{"r0":156.9697,"d0":-58.7394,"r1":154.2708,"d1":-61.3323},{"r0":154.2708,"d0":-61.3323,"r1":139.2726,"d1":-59.2752},{"r0":130.1543,"d0":-59.7610,"r1":125.6285,"d1":-59.5095},{"r0":125.6285,"d0":-59.5095,"r1":95.9879,"d1":-52.6957},{"r0":137.7421,"d0":-58.9669,"r1":139.2726,"d1":-59.2752},{"r0":137.7421,"d0":-58.9669,"r1":130.1543,"d1":-59.7610},{"r0":95.9879,"d0":-52.6957,"r1":99.4403,"d1":-43.1959},{"r0":125.6285,"d0":-59.5095,"r1":120.8961,"d1":-40.0031},{"r0":28.5988,"d0":63.6701,"r1":21.4532,"d1":60.2353},{"r0":21.4532,"d0":60.2353,"r1":14.1771,"d1":60.7167},{"r0":14.1771,"d0":60.7167,"r1":10.1267,"d1":56.5373},{"r0":10.1267,"d0":56.5373,"r1":2.2933,"d1":59.1498},{"r0":219.9115,"d0":-60.8340,"r1":210.9559,"d1":-60.3730},{"r0":210.9559,"d0":-60.3730,"r1":204.9719,"d1":-53.4664},{"r0":204.9719,"d0":-53.4664,"r1":208.8850,"d1":-47.2884},{"r0":208.8850,"d0":-47.2884,"r1":209.6698,"d1":-44.8036},{"r0":209.6698,"d0":-44.8036,"r1":207.4041,"d1":-42.4737},{"r0":207.4041,"d0":-42.4737,"r1":207.3762,"d1":-41.6877},{"r0":207.3762,"d0":-41.6877,"r1":202.7611,"d1":-39.4073},{"r0":202.7611,"d0":-39.4073,"r1":200.1494,"d1":-36.7123},{"r0":207.3762,"d0":-41.6877,"r1":211.6709,"d1":-36.3700},{"r0":207.4041,"d0":-42.4737,"r1":218.8768,"d1":-42.1578},{"r0":218.8768,"d0":-42.1578,"r1":224.7904,"d1":-42.1042},{"r0":208.8850,"d0":-47.2884,"r1":190.3796,"d1":-48.9599},{"r0":190.3796,"d0":-48.9599,"r1":187.0100,"d1":-50.2306},{"r0":187.0100,"d0":-50.2306,"r1":182.0897,"d1":-50.7224},{"r0":182.0897,"d0":-50.7224,"r1":173.6903,"d1":-54.2641},{"r0":173.6903,"d0":-54.2641,"r1":173.9454,"d1":-63.0198},{"r0":332.7136,"d0":58.2013,"r1":342.4203,"d1":66.2004},{"r0":342.4203,"d0":66.2004,"r1":322.1649,"d1":70.5607},{"r0":322.1649,"d0":70.5607,"r1":319.6445,"d1":62.5856},{"r0":319.6445,"d0":62.5856,"r1":332.7136,"d1":58.2013},{"r0":342.4203,"d0":66.2004,"r1":354.8373,"d1":77.6323},{"r0":354.8373,"d0":77.6323,"r1":322.1649,"d1":70.5607},{"r0":197.4970,"d0":17.5294,"r1":197.9686,"d1":27.8782},{"r0":197.9686,"d0":27.8782,"r1":186.7345,"d1":28.2684},{"r0":188.4362,"d0":41.3575,"r1":194.0071,"d1":38.3184},{"r0":89.9303,"d0":37.2126,"r1":89.8822,"d1":44.9474},{"r0":89.8822,"d0":44.9474,"r1":79.1723,"d1":45.9980},{"r0":79.1723,"d0":45.9980,"r1":75.6195,"d1":41.0758},{"r0":75.6195,"d0":41.0758,"r1":74.2484,"d1":33.1661},{"r0":81.5730,"d0":28.6075,"r1":74.2484,"d1":33.1661},{"r0":81.5730,"d0":28.6075,"r1":89.9303,"d1":37.2126},{"r0":95.5285,"d0":-33.4364,"r1":94.1381,"d1":-35.1405},{"r0":94.1381,"d0":-35.1405,"r1":89.3842,"d1":-35.2833},{"r0":89.3842,"d0":-35.2833,"r1":87.7399,"d1":-35.7683},{"r0":87.7399,"d0":-35.7683,"r1":89.7867,"d1":-42.8151},{"r0":87.7399,"d0":-35.7683,"r1":84.9123,"d1":-34.0741},{"r0":84.9123,"d0":-34.0741,"r1":82.8031,"d1":-35.4705},{"r0":220.6274,"d0":-64.9751,"r1":230.8444,"d1":-59.3208},{"r0":220.6274,"d0":-64.9751,"r1":229.3788,"d1":-58.8012},{"r0":164.9437,"d0":-18.2988,"r1":167.9145,"d1":-22.8258},{"r0":167.9145,"d0":-22.8258,"r1":171.2205,"d1":-17.6840},{"r0":171.2205,"d0":-17.6840,"r1":169.8352,"d1":-14.7785},{"r0":169.8352,"d0":-14.7785,"r1":164.9437,"d1":-18.2988},{"r0":169.8352,"d0":-14.7785,"r1":171.1525,"d1":-10.8593},{"r0":171.1525,"d0":-10.8593,"r1":174.1705,"d1":-9.8022},{"r0":174.1705,"d0":-9.8022,"r1":179.0040,"d1":-17.1508},{"r0":179.0040,"d0":-17.1508,"r1":176.1907,"d1":-18.3507},{"r0":176.1907,"d0":-18.3507,"r1":171.2205,"d1":-17.6840},{"r0":280.9456,"d0":-38.3234,"r1":284.1687,"d1":-37.3432},{"r0":284.1687,"d0":-37.3432,"r1":284.6808,"d1":-37.1074},{"r0":284.6808,"d0":-37.1074,"r1":286.6046,"d1":-37.0634},{"r0":286.6046,"d0":-37.0634,"r1":287.3680,"d1":-37.9045},{"r0":287.3680,"d0":-37.9045,"r1":287.5073,"d1":-39.3408},{"r0":287.5073,"d0":-39.3408,"r1":287.0873,"d1":-40.4967},{"r0":287.0873,"d0":-40.4967,"r1":285.7786,"d1":-42.0951},{"r0":285.7786,"d0":-42.0951,"r1":284.0707,"d1":-42.7107},{"r0":280.9456,"d0":-38.3234,"r1":278.0889,"d1":-39.7040},{"r0":233.2324,"d0":31.3591,"r1":231.9573,"d1":29.1057},{"r0":231.9573,"d0":29.1057,"r1":233.6719,"d1":26.7147},{"r0":233.6719,"d0":26.7147,"r1":235.6857,"d1":26.2956},{"r0":235.6857,"d0":26.2956,"r1":237.3986,"d1":26.0684},{"r0":237.3986,"d0":26.0684,"r1":239.3969,"d1":26.8779},{"r0":239.3969,"d0":26.8779,"r1":240.3607,"d1":29.8511},{"r0":188.0176,"d0":-16.1960,"r1":187.4661,"d1":-16.5154},{"r0":187.4661,"d0":-16.5154,"r1":183.9516,"d1":-17.5419},{"r0":183.9516,"d0":-17.5419,"r1":182.5312,"d1":-22.6198},{"r0":182.5312,"d0":-22.6198,"r1":182.1034,"d1":-24.7289},{"r0":182.5312,"d0":-22.6198,"r1":188.5968,"d1":-23.3968},{"r0":188.5968,"d0":-23.3968,"r1":187.4661,"d1":-16.5154},{"r0":187.7914,"d0":-57.1132,"r1":186.6497,"d1":-63.0991},{"r0":191.9304,"d0":-59.6888,"r1":183.7864,"d1":-58.7489},{"r0":289.2756,"d0":53.3685,"r1":292.4265,"d1":51.7298},{"r0":292.4265,"d0":51.7298,"r1":296.2436,"d1":45.1308},{"r0":296.2436,"d0":45.1308,"r1":305.5571,"d1":40.2567},{"r0":305.5571,"d0":40.2567,"r1":310.3580,"d1":45.2803},{"r0":305.5571,"d0":40.2567,"r1":311.5527,"d1":33.9703},{"r0":311.5527,"d0":33.9703,"r1":318.2341,"d1":30.2269},{"r0":318.2341,"d0":30.2269,"r1":326.0357,"d1":28.7426},{"r0":305.5571,"d0":40.2567,"r1":299.0766,"d1":35.0834},{"r0":299.0766,"d0":35.0834,"r1":292.6803,"d1":27.9597},{"r0":308.3032,"d0":11.3033,"r1":309.3872,"d1":14.5951},{"r0":309.3872,"d0":14.5951,"r1":309.9095,"d1":15.9121},{"r0":309.9095,"d0":15.9121,"r1":311.6646,"d1":16.1243},{"r0":311.6646,"d0":16.1243,"r1":310.8647,"d1":15.0746},{"r0":310.8647,"d0":15.0746,"r1":309.3872,"d1":14.5951},{"r0":86.1933,"d0":-65.7355,"r1":88.5249,"d1":-63.0896},{"r0":88.5249,"d0":-63.0896,"r1":83.4063,"d1":-62.4898},{"r0":83.4063,"d0":-62.4898,"r1":86.1933,"d1":-65.7355},{"r0":83.4063,"d0":-62.4898,"r1":68.4990,"d1":-55.0450},{"r0":68.4990,"d0":-55.0450,"r1":64.0065,"d1":-51.4866},{"r0":268.3820,"d0":56.8726,"r1":269.1516,"d1":51.4889},{"r0":269.1516,"d0":51.4889,"r1":262.6082,"d1":52.3014},{"r0":262.6082,"d0":52.3014,"r1":263.0665,"d1":55.1730},{"r0":263.0665,"d0":55.1730,"r1":268.3820,"d1":56.8726},{"r0":268.3820,"d0":56.8726,"r1":288.1384,"d1":67.6615},{"r0":288.1384,"d0":67.6615,"r1":297.0428,"d1":70.2679},{"r0":297.0428,"d0":70.2679,"r1":288.8884,"d1":73.3555},{"r0":288.8884,"d0":73.3555,"r1":275.2610,"d1":72.7328},{"r0":275.2610,"d0":72.7328,"r1":257.1967,"d1":65.7147},{"r0":257.1967,"d0":65.7147,"r1":245.9979,"d1":61.5142},{"r0":245.9979,"d0":61.5142,"r1":240.4730,"d1":58.5653},{"r0":240.4730,"d0":58.5653,"r1":231.2324,"d1":58.9661},{"r0":231.2324,"d0":58.9661,"r1":211.0975,"d1":64.3758},{"r0":211.0975,"d0":64.3758,"r1":188.3709,"d1":69.7882},{"r0":188.3709,"d0":69.7882,"r1":172.8511,"d1":69.3311},{"r0":243.3697,"d0":-54.6305,"r1":244.9603,"d1":-50.1555},{"r0":244.9603,"d0":-50.1555,"r1":246.7960,"d1":-47.5548},{"r0":246.7960,"d0":-47.5548,"r1":240.8037,"d1":-49.2297},{"r0":240.8037,"d0":-49.2297,"r1":244.9603,"d1":-50.1555},{"r0":240.8037,"d0":-49.2297,"r1":243.3697,"d1":-54.6305},{"r0":24.4283,"d0":-57.2368,"r1":28.9885,"d1":-51.6089},{"r0":28.9885,"d0":-51.6089,"r1":34.1273,"d1":-51.5122},{"r0":34.1273,"d0":-51.5122,"r1":36.7463,"d1":-47.7038},{"r0":36.7463,"d0":-47.7038,"r1":39.9499,"d1":-42.8917},{"r0":39.9499,"d0":-42.8917,"r1":40.1667,"d1":-39.8554},{"r0":40.1667,"d0":-39.8554,"r1":44.5653,"d1":-40.3047},{"r0":44.5653,"d0":-40.3047,"r1":49.9792,"d1":-43.0698},{"r0":49.9792,"d0":-43.0698,"r1":57.1494,"d1":-37.6202},{"r0":57.1494,"d0":-37.6202,"r1":57.3636,"d1":-36.2002},{"r0":57.3636,"d0":-36.2002,"r1":64.4736,"d1":-33.7983},{"r0":64.4736,"d0":-33.7983,"r1":66.0092,"d1":-34.0168},{"r0":66.0092,"d0":-34.0168,"r1":68.8877,"d1":-30.5623},{"r0":68.8877,"d0":-30.5623,"r1":56.7121,"d1":-23.2497},{"r0":56.7121,"d0":-23.2497,"r1":53.4470,"d1":-21.6329},{"r0":53.4470,"d0":-21.6329,"r1":49.8792,"d1":-21.7579},{"r0":49.8792,"d0":-21.7579,"r1":45.5979,"d1":-23.6245},{"r0":45.5979,"d0":-23.6245,"r1":41.2757,"d1":-18.5726},{"r0":41.2757,"d0":-18.5726,"r1":44.1069,"d1":-8.8981},{"r0":44.1069,"d0":-8.8981,"r1":48.9584,"d1":-8.8197},{"r0":48.9584,"d0":-8.8197,"r1":53.2327,"d1":-9.4583},{"r0":53.2327,"d0":-9.4583,"r1":55.8121,"d1":-9.7634},{"r0":55.8121,"d0":-9.7634,"r1":69.0798,"d1":-3.3525},{"r0":69.0798,"d0":-3.3525,"r1":71.3756,"d1":-3.2547},{"r0":71.3756,"d0":-3.2547,"r1":73.2236,"d1":-5.4527},{"r0":73.2236,"d0":-5.4527,"r1":76.9624,"d1":-5.0864},{"r0":76.9624,"d0":-5.0864,"r1":77.2866,"d1":-8.7541},{"r0":77.2866,"d0":-8.7541,"r1":69.5451,"d1":-14.3040},{"r0":295.2622,"d0":17.4760,"r1":296.8469,"d1":18.5343},{"r0":296.8469,"d0":18.5343,"r1":295.0241,"d1":18.0139},{"r0":296.8469,"d0":18.5343,"r1":299.6893,"d1":19.4921},{"r0":299.6893,"d0":19.4921,"r1":301.2896,"d1":19.9911},{"r0":42.2725,"d0":-32.4059,"r1":48.0187,"d1":-28.9876},{"r0":99.4279,"d0":16.3993,"r1":106.0272,"d1":20.5703},{"r0":106.0272,"d0":20.5703,"r1":110.0307,"d1":21.9823},{"r0":110.0307,"d0":21.9823,"r1":109.5232,"d1":16.5404},{"r0":109.5232,"d0":16.5404,"r1":101.3224,"d1":12.8956},{"r0":110.0307,"d0":21.9823,"r1":113.9806,"d1":26.8957},{"r0":113.9806,"d0":26.8957,"r1":116.1119,"d1":24.3980},{"r0":113.9806,"d0":26.8957,"r1":116.3292,"d1":28.0262},{"r0":113.9806,"d0":26.8957,"r1":111.4317,"d1":27.7981},{"r0":111.4317,"d0":27.7981,"r1":107.7849,"d1":30.2452},{"r0":107.7849,"d0":30.2452,"r1":113.6495,"d1":31.8883},{"r0":107.7849,"d0":30.2452,"r1":103.1972,"d1":33.9613},{"r0":107.7849,"d0":30.2452,"r1":100.9830,"d1":25.1311},{"r0":100.9830,"d0":25.1311,"r1":97.2408,"d1":20.2121},{"r0":100.9830,"d0":25.1311,"r1":95.7401,"d1":22.5136},{"r0":95.7401,"d0":22.5136,"r1":93.7194,"d1":22.5068},{"r0":93.7194,"d0":22.5068,"r1":91.0301,"d1":23.2633},{"r0":52.2672,"d0":59.9403,"r1":59.3560,"d1":63.0723},{"r0":59.3560,"d0":63.0723,"r1":73.5125,"d1":66.3427},{"r0":52.2672,"d0":59.9403,"r1":57.5895,"d1":71.3323},{"r0":57.5895,"d0":71.3323,"r1":73.5125,"d1":66.3427},{"r0":57.5895,"d0":71.3323,"r1":80.6405,"d1":79.2311},{"r0":103.5475,"d0":-12.0386,"r1":105.9396,"d1":-15.6333},{"r0":105.9396,"d0":-15.6333,"r1":104.0343,"d1":-17.0542},{"r0":104.0343,"d0":-17.0542,"r1":101.2872,"d1":-16.7161},{"r0":101.2872,"d0":-16.7161,"r1":105.7561,"d1":-23.8333},{"r0":105.7561,"d0":-23.8333,"r1":107.0979,"d1":-26.3932},{"r0":107.0979,"d0":-26.3932,"r1":108.7027,"d1":-26.7727},{"r0":108.7027,"d0":-26.7727,"r1":111.0238,"d1":-29.3031},{"r0":104.6565,"d0":-28.9721,"r1":105.4298,"d1":-27.9348},{"r0":105.4298,"d0":-27.9348,"r1":107.0979,"d1":-26.3932},{"r0":105.4298,"d0":-27.9348,"r1":103.5543,"d1":-23.9283},{"r0":103.5543,"d0":-23.9283,"r1":99.1710,"d1":-19.2559},{"r0":99.1710,"d0":-19.2559,"r1":98.7641,"d1":-22.9648},{"r0":99.1710,"d0":-19.2559,"r1":95.6749,"d1":-17.9559},{"r0":99.1710,"d0":-19.2559,"r1":101.2872,"d1":-16.7161},{"r0":104.6565,"d0":-28.9721,"r1":102.4602,"d1":-32.5085},{"r0":95.0783,"d0":-30.0634,"r1":104.6565,"d1":-28.9721},{"r0":104.0343,"d0":-17.0542,"r1":103.5475,"d1":-12.0386},{"r0":206.8853,"d0":49.3133,"r1":200.9812,"d1":54.9254},{"r0":200.9812,"d0":54.9254,"r1":193.5071,"d1":55.9598},{"r0":193.5071,"d0":55.9598,"r1":183.8563,"d1":57.0326},{"r0":183.8563,"d0":57.0326,"r1":165.9323,"d1":61.7510},{"r0":165.9323,"d0":61.7510,"r1":165.4602,"d1":56.3824},{"r0":165.4602,"d0":56.3824,"r1":178.4575,"d1":53.6948},{"r0":178.4575,"d0":53.6948,"r1":183.8563,"d1":57.0326},{"r0":178.4575,"d0":53.6948,"r1":176.5127,"d1":47.7794},{"r0":176.5127,"d0":47.7794,"r1":167.4159,"d1":44.4985},{"r0":167.4159,"d0":44.4985,"r1":154.2743,"d1":42.9144},{"r0":167.4159,"d0":44.4985,"r1":155.5823,"d1":41.4995},{"r0":165.4602,"d0":56.3824,"r1":148.0265,"d1":54.0643},{"r0":148.0265,"d0":54.0643,"r1":143.2157,"d1":51.6773},{"r0":143.2157,"d0":51.6773,"r1":135.9064,"d1":47.1565},{"r0":143.2157,"d0":51.6773,"r1":134.8024,"d1":48.0418},{"r0":148.0265,"d0":54.0643,"r1":147.7480,"d1":59.0387},{"r0":147.7480,"d0":59.0387,"r1":127.5665,"d1":60.7182},{"r0":127.5665,"d0":60.7182,"r1":142.8818,"d1":63.0619},{"r0":142.8818,"d0":63.0619,"r1":165.9323,"d1":61.7510},{"r0":346.7198,"d0":-43.5204,"r1":337.3174,"d1":-43.4956},{"r0":337.3174,"d0":-43.4956,"r1":332.0581,"d1":-46.9610},{"r0":332.0581,"d0":-46.9610,"r1":340.6667,"d1":-46.8846},{"r0":340.6667,"d0":-46.8846,"r1":347.5896,"d1":-45.2467},{"r0":347.5896,"d0":-45.2467,"r1":346.7198,"d1":-43.5204},{"r0":340.6667,"d0":-46.8846,"r1":345.2202,"d1":-52.7541},{"r0":340.6667,"d0":-46.8846,"r1":342.1386,"d1":-51.3169},{"r0":332.0581,"d0":-46.9610,"r1":331.5287,"d1":-39.5434},{"r0":331.5287,"d0":-39.5434,"r1":328.4821,"d1":-37.3649},{"r0":264.8662,"d0":46.0063,"r1":269.0633,"d1":37.2505},{"r0":269.0633,"d0":37.2505,"r1":260.9206,"d1":37.1459},{"r0":260.9206,"d0":37.1459,"r1":259.4178,"d1":37.2915},{"r0":259.4178,"d0":37.2915,"r1":258.7618,"d1":36.8092},{"r0":258.7618,"d0":36.8092,"r1":250.7240,"d1":38.9223},{"r0":250.7240,"d0":38.9223,"r1":248.5258,"d1":42.4370},{"r0":248.5258,"d0":42.4370,"r1":244.9352,"d1":46.3134},{"r0":244.9352,"d0":46.3134,"r1":238.1685,"d1":42.4515},{"r0":250.7240,"d0":38.9223,"r1":250.3217,"d1":31.6027},{"r0":250.3217,"d0":31.6027,"r1":247.5550,"d1":21.4896},{"r0":247.5550,"d0":21.4896,"r1":245.4801,"d1":19.1531},{"r0":250.3217,"d0":31.6027,"r1":255.0724,"d1":30.9264},{"r0":255.0724,"d0":30.9264,"r1":262.6846,"d1":26.1106},{"r0":262.6846,"d0":26.1106,"r1":258.7580,"d1":24.8392},{"r0":266.6148,"d0":27.7207,"r1":269.4412,"d1":29.2479},{"r0":269.4412,"d0":29.2479,"r1":271.8856,"d1":28.7625},{"r0":255.0724,"d0":30.9264,"r1":258.7618,"d1":36.8092},{"r0":266.6148,"d0":27.7207,"r1":262.6846,"d1":26.1106},{"r0":63.5004,"d0":-42.2944,"r1":40.1650,"d1":-54.5499},{"r0":40.1650,"d0":-54.5499,"r1":45.9036,"d1":-59.7378},{"r0":130.8062,"d0":3.3987,"r1":129.6893,"d1":3.3414},{"r0":129.6893,"d0":3.3414,"r1":129.4140,"d1":5.7038},{"r0":129.4140,"d0":5.7038,"r1":131.6938,"d1":6.4188},{"r0":131.6938,"d0":6.4188,"r1":132.1082,"d1":5.8378},{"r0":132.1082,"d0":5.8378,"r1":130.8062,"d1":3.3987},{"r0":132.1082,"d0":5.8378,"r1":133.8485,"d1":5.9456},{"r0":133.8485,"d0":5.9456,"r1":138.5911,"d1":2.3143},{"r0":138.5911,"d0":2.3143,"r1":142.9955,"d1":-1.1847},{"r0":142.9955,"d0":-1.1847,"r1":142.2871,"d1":-2.7690},{"r0":142.2871,"d0":-2.7690,"r1":141.8969,"d1":-8.6586},{"r0":141.8969,"d0":-8.6586,"r1":147.8696,"d1":-14.8466},{"r0":147.8696,"d0":-14.8466,"r1":152.6470,"d1":-12.3541},{"r0":152.6470,"d0":-12.3541,"r1":156.5226,"d1":-16.8363},{"r0":156.5226,"d0":-16.8363,"r1":162.4062,"d1":-16.1936},{"r0":162.4062,"d0":-16.1936,"r1":173.2506,"d1":-31.8576},{"r0":173.2506,"d0":-31.8576,"r1":178.2272,"d1":-33.9081},{"r0":178.2272,"d0":-33.9081,"r1":197.2636,"d1":-23.1181},{"r0":197.2636,"d0":-23.1181,"r1":199.7304,"d1":-23.1715},{"r0":6.4187,"d0":-77.2542,"r1":56.8094,"d1":-74.2390},{"r0":56.8094,"d0":-74.2390,"r1":39.8970,"d1":-68.2669},{"r0":39.8970,"d0":-68.2669,"r1":35.4375,"d1":-68.6594},{"r0":35.4375,"d0":-68.6594,"r1":29.6918,"d1":-61.5699},{"r0":319.9664,"d0":-53.4494,"r1":309.3917,"d1":-47.2915},{"r0":309.3917,"d0":-47.2915,"r1":313.7025,"d1":-58.4542},{"r0":313.7025,"d0":-58.4542,"r1":319.9664,"d1":-53.4494},{"r0":333.9924,"d0":37.7487,"r1":337.6219,"d1":43.1234},{"r0":337.6219,"d0":43.1234,"r1":337.3826,"d1":47.7069},{"r0":337.3826,"d0":47.7069,"r1":336.1291,"d1":49.4764},{"r0":336.1291,"d0":49.4764,"r1":335.8901,"d1":52.2290},{"r0":335.8901,"d0":52.2290,"r1":337.8227,"d1":50.2825},{"r0":337.8227,"d0":50.2825,"r1":337.3826,"d1":47.7069},{"r0":93.7139,"d0":-6.2748,"r1":97.2045,"d1":-7.0331},{"r0":97.2045,"d0":-7.0331,"r1":107.9661,"d1":-0.4928},{"r0":107.9661,"d0":-0.4928,"r1":95.9420,"d1":4.5929},{"r0":95.9420,"d0":4.5929,"r1":92.2413,"d1":2.4997},{"r0":107.9661,"d0":-0.4928,"r1":122.1485,"d1":-2.9838},{"r0":122.1485,"d0":-2.9838,"r1":115.3118,"d1":-9.5511},{"r0":91.5388,"d0":-14.9353,"r1":89.1012,"d1":-14.1677},{"r0":89.1012,"d0":-14.1677,"r1":86.7389,"d1":-14.8219},{"r0":86.7389,"d0":-14.8219,"r1":83.1826,"d1":-17.8223},{"r0":83.1826,"d0":-17.8223,"r1":78.2329,"d1":-16.2055},{"r0":83.1826,"d0":-17.8223,"r1":87.8304,"d1":-20.8791},{"r0":87.8304,"d0":-20.8791,"r1":86.1159,"d1":-22.4484},{"r0":86.1159,"d0":-22.4484,"r1":82.0613,"d1":-20.7594},{"r0":82.0613,"d0":-20.7594,"r1":76.3653,"d1":-22.3710},{"r0":83.1826,"d0":-17.8223,"r1":82.0613,"d1":-20.7594},{"r0":78.2329,"d0":-16.2055,"r1":79.8939,"d1":-13.1768},{"r0":78.2329,"d0":-16.2055,"r1":78.3078,"d1":-12.9413},{"r0":76.3653,"d0":-22.3710,"r1":78.2329,"d1":-16.2055},{"r0":78.3078,"d0":-12.9413,"r1":78.0746,"d1":-11.8692},{"r0":79.8939,"d0":-13.1768,"r1":79.9959,"d1":-12.3156},{"r0":177.2649,"d0":14.5721,"r1":168.5600,"d1":15.4296},{"r0":168.5600,"d0":15.4296,"r1":152.0930,"d1":11.9672},{"r0":152.0930,"d0":11.9672,"r1":151.8331,"d1":16.7627},{"r0":151.8331,"d0":16.7627,"r1":154.9931,"d1":19.8415},{"r0":154.9931,"d0":19.8415,"r1":168.5271,"d1":20.5237},{"r0":168.5271,"d0":20.5237,"r1":177.2649,"d1":14.5721},{"r0":154.9931,"d0":19.8415,"r1":154.1726,"d1":23.4173},{"r0":154.1726,"d0":23.4173,"r1":148.1910,"d1":26.0070},{"r0":148.1910,"d0":26.0070,"r1":146.4628,"d1":23.7743},{"r0":168.5271,"d0":20.5237,"r1":168.5600,"d1":15.4296},{"r0":237.7397,"d0":-33.6272,"r1":241.8175,"d1":-36.7557},{"r0":241.8175,"d0":-36.7557,"r1":240.0305,"d1":-38.3967},{"r0":240.0305,"d0":-38.3967,"r1":237.7397,"d1":-33.6272},{"r0":240.0305,"d0":-38.3967,"r1":233.7852,"d1":-41.1668},{"r0":233.7852,"d0":-41.1668,"r1":230.3430,"d1":-40.6475},{"r0":230.3430,"d0":-40.6475,"r1":230.4516,"d1":-36.2614},{"r0":230.3430,"d0":-40.6475,"r1":224.6331,"d1":-43.1340},{"r0":233.7852,"d0":-41.1668,"r1":234.5135,"d1":-42.5673},{"r0":234.5135,"d0":-42.5673,"r1":228.0714,"d1":-52.0992},{"r0":228.0714,"d0":-52.0992,"r1":220.4823,"d1":-47.3882},{"r0":228.0714,"d0":-52.0992,"r1":219.4718,"d1":-49.4258},{"r0":220.4823,"d0":-47.3882,"r1":216.5450,"d1":-45.3793},{"r0":220.4823,"d0":-47.3882,"r1":224.6331,"d1":-43.1340},{"r0":140.2639,"d0":34.3926,"r1":139.7110,"d1":36.8026},{"r0":139.7110,"d0":36.8026,"r1":136.6324,"d1":38.4522},{"r0":136.6324,"d0":38.4522,"r1":135.1603,"d1":41.7829},{"r0":135.1603,"d0":41.7829,"r1":125.7088,"d1":43.1881},{"r0":125.7088,"d0":43.1881,"r1":111.6786,"d1":49.2115},{"r0":111.6786,"d0":49.2115,"r1":104.3192,"d1":58.4228},{"r0":104.3192,"d0":58.4228,"r1":94.9058,"d1":59.0110},{"r0":279.2346,"d0":38.7837,"r1":281.1931,"d1":37.6051},{"r0":281.1931,"d0":37.6051,"r1":282.5200,"d1":33.3627},{"r0":282.5200,"d0":33.3627,"r1":284.7359,"d1":32.6896},{"r0":284.7359,"d0":32.6896,"r1":283.6262,"d1":36.8986},{"r0":283.6262,"d0":36.8986,"r1":281.1931,"d1":37.6051},{"r0":156.7879,"d0":-31.0678,"r1":149.7179,"d1":-35.8910},{"r0":319.4845,"d0":-32.1725,"r1":315.3228,"d1":-32.2578},{"r0":315.3228,"d0":-32.2578,"r1":312.4920,"d1":-33.7797},{"r0":191.5702,"d0":-68.1081,"r1":176.4021,"d1":-66.7288},{"r0":176.4021,"d0":-66.7288,"r1":188.1170,"d1":-72.1330},{"r0":188.1170,"d0":-72.1330,"r1":189.2961,"d1":-69.1356},{"r0":189.2961,"d0":-69.1356,"r1":191.5702,"d1":-68.1081},{"r0":325.3688,"d0":-77.3900,"r1":341.5154,"d1":-81.3816},{"r0":341.5154,"d0":-81.3816,"r1":216.7320,"d1":-83.6679},{"r0":216.7320,"d0":-83.6679,"r1":325.3688,"d1":-77.3900},{"r0":221.9655,"d0":-79.0448,"r1":248.3641,"d1":-78.8971},{"r0":248.3641,"d0":-78.8971,"r1":250.7719,"d1":-77.5174},{"r0":263.7336,"d0":12.5600,"r1":265.8681,"d1":4.5673},{"r0":257.5945,"d0":-15.7249,"r1":265.8681,"d1":4.5673},{"r0":263.7336,"d0":12.5600,"r1":254.4171,"d1":9.3750},{"r0":254.4171,"d0":9.3750,"r1":244.5804,"d1":-4.6925},{"r0":244.5804,"d0":-4.6925,"r1":249.2897,"d1":-10.5671},{"r0":249.2897,"d0":-10.5671,"r1":257.5945,"d1":-15.7249},{"r0":257.5945,"d0":-15.7249,"r1":262.8540,"d1":-23.9626},{"r0":85.1897,"d0":-1.9426,"r1":84.0534,"d1":-1.2019},{"r0":84.0534,"d0":-1.2019,"r1":83.0017,"d1":-0.2991},{"r0":90.8640,"d0":19.6906,"r1":92.9850,"d1":14.2088},{"r0":92.9850,"d0":14.2088,"r1":91.8930,"d1":14.7685},{"r0":91.8930,"d0":14.7685,"r1":88.5958,"d1":20.2762},{"r0":92.9850,"d0":14.2088,"r1":90.5958,"d1":9.6473},{"r0":90.5958,"d0":9.6473,"r1":88.7929,"d1":7.4071},{"r0":88.7929,"d0":7.4071,"r1":85.1897,"d1":-1.9426},{"r0":85.1897,"d0":-1.9426,"r1":86.9391,"d1":-9.6696},{"r0":86.9391,"d0":-9.6696,"r1":78.6345,"d1":-8.2016},{"r0":78.6345,"d0":-8.2016,"r1":83.0017,"d1":-0.2991},{"r0":83.0017,"d0":-0.2991,"r1":81.2828,"d1":6.3497},{"r0":81.2828,"d0":6.3497,"r1":83.7845,"d1":9.9342},{"r0":83.7845,"d0":9.9342,"r1":88.7929,"d1":7.4071},{"r0":81.2828,"d0":6.3497,"r1":72.4600,"d1":6.9613},{"r0":72.4600,"d0":6.9613,"r1":72.8015,"d1":5.6051},{"r0":72.8015,"d0":5.6051,"r1":73.3449,"d1":2.5082},{"r0":73.3449,"d0":2.5082,"r1":74.6371,"d1":1.7140},{"r0":72.4600,"d0":6.9613,"r1":72.6530,"d1":8.9002},{"r0":72.6530,"d0":8.9002,"r1":73.7239,"d1":10.1508},{"r0":91.8930,"d0":14.7685,"r1":90.5958,"d1":9.6473},{"r0":306.4119,"d0":-56.7351,"r1":321.6106,"d1":-65.3662},{"r0":321.6106,"d0":-65.3662,"r1":311.2397,"d1":-66.2032},{"r0":311.2397,"d0":-66.2032,"r1":302.1774,"d1":-66.1821},{"r0":302.1774,"d0":-66.1821,"r1":306.4119,"d1":-56.7351},{"r0":302.1774,"d0":-66.1821,"r1":300.1477,"d1":-72.9105},{"r0":300.1477,"d0":-72.9105,"r1":280.7589,"d1":-71.4281},{"r0":280.7589,"d0":-71.4281,"r1":284.2377,"d1":-67.2335},{"r0":284.2377,"d0":-67.2335,"r1":302.1774,"d1":-66.1821},{"r0":284.2377,"d0":-67.2335,"r1":283.0543,"d1":-62.1876},{"r0":283.0543,"d0":-62.1876,"r1":275.8068,"d1":-61.4939},{"r0":275.8068,"d0":-61.4939,"r1":272.1450,"d1":-63.6686},{"r0":272.1450,"d0":-63.6686,"r1":283.0543,"d1":-62.1876},{"r0":272.1450,"d0":-63.6686,"r1":266.4333,"d1":-64.7239},{"r0":3.3090,"d0":15.1836,"r1":346.1902,"d1":15.2053},{"r0":345.9435,"d0":28.0828,"r1":340.7506,"d1":30.2212},{"r0":340.7506,"d0":30.2212,"r1":332.3068,"d1":33.1723},{"r0":345.9435,"d0":28.0828,"r1":342.5008,"d1":24.6016},{"r0":342.5008,"d0":24.6016,"r1":341.6328,"d1":23.5657},{"r0":341.6328,"d0":23.5657,"r1":331.7527,"d1":25.3451},{"r0":331.7527,"d0":25.3451,"r1":326.1614,"d1":25.6450},{"r0":346.1902,"d0":15.2053,"r1":341.6732,"d1":12.1729},{"r0":341.6732,"d0":12.1729,"r1":340.3655,"d1":10.8314},{"r0":340.3655,"d0":10.8314,"r1":332.5499,"d1":6.1979},{"r0":332.5499,"d0":6.1979,"r1":326.0465,"d1":9.8750},{"r0":2.0969,"d0":29.0904,"r1":345.9435,"d1":28.0828},{"r0":2.0969,"d0":29.0904,"r1":3.3090,"d1":15.1836},{"r0":345.9435,"d0":28.0828,"r1":346.1902,"d1":15.2053},{"r0":102.0479,"d0":-61.9414,"r1":87.4568,"d1":-56.1667},{"r0":87.4568,"d0":-56.1667,"r1":86.8212,"d1":-51.0665},{"r0":56.0797,"d0":32.2882,"r1":58.5330,"d1":31.8836},{"r0":58.5330,"d0":31.8836,"r1":59.7412,"d1":35.7910},{"r0":59.7412,"d0":35.7910,"r1":59.4635,"d1":40.0102},{"r0":59.4635,"d0":40.0102,"r1":55.7312,"d1":47.7876},{"r0":55.7312,"d0":47.7876,"r1":51.0807,"d1":49.8612},{"r0":51.0807,"d0":49.8612,"r1":46.1991,"d1":53.5064},{"r0":46.1991,"d0":53.5064,"r1":42.6742,"d1":55.8955},{"r0":51.0807,"d0":49.8612,"r1":47.0422,"d1":40.9556},{"r0":47.0422,"d0":40.9556,"r1":46.2940,"d1":38.8403},{"r0":46.2940,"d0":38.8403,"r1":42.6459,"d1":38.3186},{"r0":317.5854,"d0":10.1316,"r1":318.6201,"d1":10.0070},{"r0":318.6201,"d0":10.0070,"r1":320.7234,"d1":6.8111},{"r0":320.7234,"d0":6.8111,"r1":318.9560,"d1":5.2478},{"r0":318.9560,"d0":5.2478,"r1":317.5854,"d1":10.1316},{"r0":114.8255,"d0":5.2250,"r1":111.7877,"d1":8.2893},{"r0":163.3279,"d0":34.2149,"r1":156.9709,"d1":36.7072},{"r0":156.9709,"d0":36.7072,"r1":151.8573,"d1":35.2447},{"r0":151.8573,"d0":35.2447,"r1":143.5558,"d1":36.3976},{"r0":151.8573,"d0":35.2447,"r1":163.3279,"d1":34.2149},{"r0":292.1764,"d0":24.6649,"r1":300.2752,"d1":27.7536},{"r0":37.9462,"d0":89.2641,"r1":263.0538,"d1":86.5865},{"r0":263.0538,"d0":86.5865,"r1":251.4924,"d1":82.0373},{"r0":251.4924,"d0":82.0373,"r1":236.0145,"d1":77.7945},{"r0":236.0145,"d0":77.7945,"r1":244.3769,"d1":75.7553},{"r0":244.3769,"d0":75.7553,"r1":230.1822,"d1":71.8340},{"r0":230.1822,"d0":71.8340,"r1":222.6766,"d1":74.1555},{"r0":222.6766,"d0":74.1555,"r1":236.0145,"d1":77.7945},{"r0":17.0961,"d0":-55.2458,"r1":16.5211,"d1":-46.7184},{"r0":16.5211,"d0":-46.7184,"r1":6.5507,"d1":-43.6798},{"r0":6.5507,"d0":-43.6798,"r1":17.0961,"d1":-55.2458},{"r0":16.5211,"d0":-46.7184,"r1":22.8128,"d1":-49.0727},{"r0":22.8128,"d0":-49.0727,"r1":28.4115,"d1":-46.3027},{"r0":28.4115,"d0":-46.3027,"r1":16.5211,"d1":-46.7184},{"r0":16.5211,"d0":-46.7184,"r1":22.0914,"d1":-43.3182},{"r0":22.0914,"d0":-43.3182,"r1":6.5507,"d1":-43.6798},{"r0":6.5507,"d0":-43.6798,"r1":6.5708,"d1":-42.3060},{"r0":6.5708,"d0":-42.3060,"r1":2.3525,"d1":-45.7474},{"r0":2.3525,"d0":-45.7474,"r1":6.5507,"d1":-43.6798},{"r0":15.7046,"d0":31.8043,"r1":18.4373,"d1":24.5837},{"r0":15.7046,"d0":31.8043,"r1":19.8666,"d1":27.2641},{"r0":19.8666,"d0":27.2641,"r1":18.4373,"d1":24.5837},{"r0":18.4373,"d0":24.5837,"r1":22.8709,"d1":15.3458},{"r0":22.8709,"d0":15.3458,"r1":26.3485,"d1":9.1577},{"r0":26.3485,"d0":9.1577,"r1":30.5118,"d1":2.7638},{"r0":30.5118,"d0":2.7638,"r1":28.3890,"d1":3.1875},{"r0":28.3890,"d0":3.1875,"r1":25.3579,"d1":5.4876},{"r0":25.3579,"d0":5.4876,"r1":22.5463,"d1":6.1438},{"r0":22.5463,"d0":6.1438,"r1":15.7359,"d1":7.8901},{"r0":15.7359,"d0":7.8901,"r1":12.0725,"d1":7.2999},{"r0":12.0725,"d0":7.2999,"r1":5.1494,"d1":8.1903},{"r0":5.1494,"d0":8.1903,"r1":359.8279,"d1":6.8633},{"r0":359.8279,"d0":6.8633,"r1":354.9877,"d1":5.6263},{"r0":354.9877,"d0":5.6263,"r1":355.5117,"d1":1.7800},{"r0":355.5117,"d0":1.7800,"r1":351.7331,"d1":1.2556},{"r0":351.7331,"d0":1.2556,"r1":349.2914,"d1":3.2823},{"r0":349.2914,"d0":3.2823,"r1":351.9921,"d1":6.3790},{"r0":351.9921,"d0":6.3790,"r1":354.9877,"d1":5.6263},{"r0":344.4126,"d0":-29.6222,"r1":340.1639,"d1":-27.0436},{"r0":340.1639,"d0":-27.0436,"r1":330.2093,"d1":-28.4537},{"r0":330.2093,"d0":-28.4537,"r1":326.9340,"d1":-30.8983},{"r0":326.9340,"d0":-30.8983,"r1":332.5364,"d1":-32.5484},{"r0":332.5364,"d0":-32.5484,"r1":337.8764,"d1":-32.3461},{"r0":337.8764,"d0":-32.3461,"r1":343.9871,"d1":-32.5396},{"r0":115.4551,"d0":-72.6061,"r1":107.1868,"d1":-70.4989},{"r0":107.1868,"d0":-70.4989,"r1":121.9826,"d1":-68.6171},{"r0":121.9826,"d0":-68.6171,"r1":115.4551,"d1":-72.6061},{"r0":121.9826,"d0":-68.6171,"r1":109.2076,"d1":-67.9572},{"r0":121.9826,"d0":-68.6171,"r1":126.4343,"d1":-66.1369},{"r0":126.4343,"d0":-66.1369,"r1":135.6117,"d1":-66.3961},{"r0":135.6117,"d0":-66.3961,"r1":121.9826,"d1":-68.6171},{"r0":121.8861,"d0":-24.3043,"r1":117.2570,"d1":-24.9122},{"r0":117.2570,"d0":-24.9122,"r1":109.2857,"d1":-37.0975},{"r0":109.2857,"d0":-37.0975,"r1":99.4403,"d1":-43.1959},{"r0":99.4403,"d0":-43.1959,"r1":102.4840,"d1":-50.6146},{"r0":102.4840,"d0":-50.6146,"r1":112.3077,"d1":-43.3014},{"r0":112.3077,"d0":-43.3014,"r1":120.8961,"d1":-40.0031},{"r0":120.8961,"d0":-40.0031,"r1":121.8861,"d1":-24.3043},{"r0":63.6061,"d0":-62.4739,"r1":64.1211,"d1":-59.3022},{"r0":64.1211,"d0":-59.3022,"r1":59.6864,"d1":-61.4002},{"r0":59.6864,"d0":-61.4002,"r1":56.0489,"d1":-64.8069},{"r0":56.0489,"d0":-64.8069,"r1":63.6061,"d1":-62.4739},{"r0":275.2485,"d0":-29.8281,"r1":276.9927,"d1":-25.4217},{"r0":274.4069,"d0":-36.7617,"r1":276.0430,"d1":-34.3846},{"r0":276.0430,"d0":-34.3846,"r1":271.4520,"d1":-30.4241},{"r0":271.4520,"d0":-30.4241,"r1":266.8901,"d1":-27.8308},{"r0":271.4520,"d0":-30.4241,"r1":275.2485,"d1":-29.8281},{"r0":275.2485,"d0":-29.8281,"r1":276.0430,"d1":-34.3846},{"r0":276.0430,"d0":-34.3846,"r1":285.6530,"d1":-29.8801},{"r0":285.6530,"d0":-29.8801,"r1":281.4141,"d1":-26.9908},{"r0":281.4141,"d0":-26.9908,"r1":275.2485,"d1":-29.8281},{"r0":281.4141,"d0":-26.9908,"r1":276.9927,"d1":-25.4217},{"r0":276.9927,"d0":-25.4217,"r1":273.4409,"d1":-21.0588},{"r0":285.6530,"d0":-29.8801,"r1":286.7351,"d1":-27.6704},{"r0":286.7351,"d0":-27.6704,"r1":283.8163,"d1":-26.2967},{"r0":283.8163,"d0":-26.2967,"r1":281.4141,"d1":-26.9908},{"r0":283.8163,"d0":-26.2967,"r1":284.4325,"d1":-21.1067},{"r0":284.4325,"d0":-21.1067,"r1":286.1707,"d1":-21.7415},{"r0":286.1707,"d0":-21.7415,"r1":289.4087,"d1":-18.9529},{"r0":289.4087,"d0":-18.9529,"r1":290.4182,"d1":-17.8472},{"r0":286.7351,"d0":-27.6704,"r1":294.0069,"d1":-24.7191},{"r0":294.0069,"d0":-24.7191,"r1":300.6645,"d1":-27.7098},{"r0":300.6645,"d0":-27.7098,"r1":299.9341,"d1":-35.2763},{"r0":299.9341,"d0":-35.2763,"r1":298.8154,"d1":-41.8683},{"r0":298.8154,"d0":-41.8683,"r1":290.9715,"d1":-40.6159},{"r0":298.8154,"d0":-41.8683,"r1":290.8046,"d1":-44.7998},{"r0":263.4022,"d0":-37.1038,"r1":265.6220,"d1":-39.0300},{"r0":265.6220,"d0":-39.0300,"r1":266.8962,"d1":-40.1270},{"r0":266.8962,"d0":-40.1270,"r1":264.3297,"d1":-42.9978},{"r0":264.3297,"d0":-42.9978,"r1":258.0383,"d1":-43.2392},{"r0":258.0383,"d0":-43.2392,"r1":253.4989,"d1":-42.3620},{"r0":253.4989,"d0":-42.3620,"r1":252.9676,"d1":-38.0474},{"r0":252.9676,"d0":-38.0474,"r1":252.5412,"d1":-34.2932},{"r0":252.5412,"d0":-34.2932,"r1":248.9706,"d1":-28.2160},{"r0":248.9706,"d0":-28.2160,"r1":247.3519,"d1":-26.4320},{"r0":247.3519,"d0":-26.4320,"r1":240.0834,"d1":-22.6217},{"r0":247.3519,"d0":-26.4320,"r1":239.7130,"d1":-26.1141},{"r0":247.3519,"d0":-26.4320,"r1":241.3593,"d1":-19.8055},{"r0":237.4050,"d0":-3.4302,"r1":237.7040,"d1":4.4777},{"r0":237.7040,"d0":4.4777,"r1":236.0670,"d1":6.4256},{"r0":236.0670,"d0":6.4256,"r1":233.7006,"d1":10.5389},{"r0":233.7006,"d0":10.5389,"r1":236.5469,"d1":15.4218},{"r0":236.5469,"d0":15.4218,"r1":239.1132,"d1":15.6616},{"r0":239.1132,"d0":15.6616,"r1":237.1849,"d1":18.1416},{"r0":237.1849,"d0":18.1416,"r1":236.5469,"d1":15.4218},{"r0":284.0549,"d0":4.2036,"r1":275.3275,"d1":-2.8988},{"r0":275.3275,"d0":-2.8988,"r1":265.3536,"d1":-12.8753},{"r0":265.3536,"d0":-12.8753,"r1":264.3967,"d1":-15.3986},{"r0":264.3967,"d0":-15.3986,"r1":260.2069,"d1":-12.8469},{"r0":157.5728,"d0":-0.6370,"r1":151.9845,"d1":-0.3716},{"r0":82.9698,"d0":-76.3410,"r1":70.7665,"d1":-70.9310},{"r0":81.5730,"d0":28.6075,"r1":70.5613,"d1":22.9569},{"r0":70.5613,"d0":22.9569,"r1":67.1541,"d1":19.1804},{"r0":68.9802,"d0":16.5093,"r1":84.4112,"d1":21.1425},{"r0":64.9483,"d0":15.6276,"r1":65.7337,"d1":17.5425},{"r0":64.9483,"d0":15.6276,"r1":60.1701,"d1":12.4903},{"r0":60.1701,"d0":12.4903,"r1":51.2033,"d1":9.0289},{"r0":68.9802,"d0":16.5093,"r1":67.1541,"d1":19.1804},{"r0":68.9802,"d0":16.5093,"r1":67.1656,"d1":15.8709},{"r0":67.1656,"d0":15.8709,"r1":64.9483,"d1":15.6276},{"r0":67.1541,"d0":19.1804,"r1":66.3724,"d1":17.9279},{"r0":66.3724,"d0":17.9279,"r1":65.7337,"d1":17.5425},{"r0":65.7337,"d0":17.5425,"r1":57.2906,"d1":24.0534},{"r0":277.2076,"d0":-49.0706,"r1":276.7434,"d1":-45.9685},{"r0":334.6256,"d0":-60.2596,"r1":349.3575,"d1":-58.2357},{"r0":349.3575,"d0":-58.2357,"r1":5.0121,"d1":-64.8748},{"r0":349.3575,"d0":-58.2357,"r1":7.8859,"d1":-62.9582},{"r0":34.3286,"d0":33.8472,"r1":32.3859,"d1":34.9873},{"r0":32.3859,"d0":34.9873,"r1":28.2704,"d1":29.5788},{"r0":28.2704,"d0":29.5788,"r1":34.3286,"d1":33.8472},{"r0":252.1662,"d0":-69.0277,"r1":229.7277,"d1":-68.6795},{"r0":229.7277,"d0":-68.6795,"r1":238.7862,"d1":-63.4307},{"r0":238.7862,"d0":-63.4307,"r1":252.1662,"d1":-69.0277},{"r0":322.8897,"d0":-5.5712,"r1":331.4460,"d1":-0.3199},{"r0":331.4460,"d0":-0.3199,"r1":335.4141,"d1":-1.3873},{"r0":335.4141,"d0":-1.3873,"r1":337.2080,"d1":-0.0200},{"r0":337.2080,"d0":-0.0200,"r1":338.8391,"d1":-0.1175},{"r0":338.8391,"d0":-0.1175,"r1":343.1536,"d1":-7.5796},{"r0":343.1536,"d0":-7.5796,"r1":348.9729,"d1":-9.0877},{"r0":348.9729,"d0":-9.0877,"r1":350.7426,"d1":-20.1006},{"r0":331.4460,"d0":-0.3199,"r1":334.2085,"d1":-7.7833},{"r0":334.2085,"d0":-7.7833,"r1":331.6093,"d1":-13.8697},{"r0":334.2085,"d0":-7.7833,"r1":337.6617,"d1":-10.6779},{"r0":337.6617,"d0":-10.6779,"r1":342.3979,"d1":-13.5926},{"r0":342.3979,"d0":-13.5926,"r1":343.6626,"d1":-15.8208},{"r0":343.6626,"d0":-15.8208,"r1":347.3616,"d1":-21.1724},{"r0":311.9190,"d0":-9.4958,"r1":322.8897,"d1":-5.5712},{"r0":176.4648,"d0":6.5294,"r1":184.6680,"d1":-0.7872},{"r0":184.6680,"d0":-0.7872,"r1":190.4152,"d1":-1.4494},{"r0":190.4152,"d0":-1.4494,"r1":201.2982,"d1":-11.1613},{"r0":201.2982,"d0":-11.1613,"r1":213.2239,"d1":-10.2737},{"r0":213.2239,"d0":-10.2737,"r1":214.0036,"d1":-6.0005},{"r0":214.0036,"d0":-6.0005,"r1":220.7651,"d1":-5.6582},{"r0":201.2982,"d0":-11.1613,"r1":203.6733,"d1":-0.5958},{"r0":203.6733,"d0":-0.5958,"r1":210.4116,"d1":1.5445},{"r0":210.4116,"d0":1.5445,"r1":221.5622,"d1":1.8929},{"r0":203.6733,"d0":-0.5958,"r1":193.9009,"d1":3.3975},{"r0":193.9009,"d0":3.3975,"r1":195.5442,"d1":10.9591},{"r0":193.9009,"d0":3.3975,"r1":190.4152,"d1":-1.4494},{"r0":122.3831,"d0":-47.3366,"r1":130.0733,"d1":-52.9219},{"r0":130.0733,"d0":-52.9219,"r1":131.1759,"d1":-54.7088},{"r0":131.1759,"d0":-54.7088,"r1":140.5284,"d1":-55.0107},{"r0":140.5284,"d0":-55.0107,"r1":149.2156,"d1":-54.5678},{"r0":149.2156,"d0":-54.5678,"r1":161.6923,"d1":-49.4203},{"r0":161.6923,"d0":-49.4203,"r1":159.3258,"d1":-48.2256},{"r0":159.3258,"d0":-48.2256,"r1":153.6841,"d1":-42.1219},{"r0":153.6841,"d0":-42.1219,"r1":142.6751,"d1":-40.4668},{"r0":142.6751,"d0":-40.4668,"r1":136.9990,"d1":-43.4326},{"r0":136.9990,"d0":-43.4326,"r1":122.3831,"d1":-47.3366}];
var allstars_index_name = {"names": ["M45", "IC2391", "NGC6231", "NGC3532", "M44", "M7", "NGC0869", "NGC0884", "NGC2516", "NGC2232", "NGC2362", "IC4665", "NGC3114", "M6", "IC2581", "M47", "M24", "M41", "IC2395", "M25", "IC4756", "NGC6633", "M39", "NGC2547", "NGC3293", "M35", "NGC6025", "M34", "NGC6871", "NGC3766", "NGC5138", "NGC2281", "NGC6087", "NGC6281", "NGC5662", "NGC6374", "M23", "M37", "NGC5460", "NGC6067", "NGC7686", "NGC0752", "NGC2477", "M48", "NGC6124", "M11", "NGC2169", "M50", "NGC5281", "M21", "M36", "NGC2301", "NGC3228", "NGC5316", "NGC6322", "NGC6605", "NGC1746", "M46", "NGC2669", "NGC7160", "NGC1545", "M93", "NGC2546", "NGC5617", "NGC6940", "NGC0457", "NGC1528", "NGC1647", "NGC1662", "M38", "NGC6242", "NGC7243", "NGC0129", "NGC0654", "NGC2354", "NGC2520", "NGC2539", "NGC5822", "NGC6604", "NGC1444", "NGC3572", "NGC6169", "M29", "NGC1027", "NGC1342", "NGC2129", "NGC2343", "NGC2423", "NGC6167", "NGC6709", "NGC7789", "NGC6811", "IC4651", "NGC1502", "NGC2439", "M67", "NGC4609", "M18", "M52", "NGC0225", "NGC1582", "NGC1807", "NGC1857", "NGC2571", "NGC7063", "NGC0663", "NGC2353", "NGC2335", "NGC2360", "NGC2910", "NGC4463", "NGC6134", "NGC6178", "NGC6208", "NGC6425", "NGC7082", "IC4996", "NGC2251", "NGC2409", "NGC2482", "NGC6819", "NGC2645", "IC2488", "M103", "NGC2384", "NGC2396", "NGC2567", "NGC3330", "NGC4103", "NGC4349", "NGC6200", "NGC6910", "NGC1893", "NGC2286", "NGC6716", "NGC6755", "NGC0957", "NGC1664", "NGC2483", "NGC2506", "NGC2533", "NGC3680", "NGC6520", "NGC6866", "NGC7039", "NGC1778", "NGC1817", "NGC2252", "NGC2345", "NGC3519", "NGC5606", "NGC7209", "NGC7234", "NGC2670", "NGC6664", "NGC6834", "NGC6939", "NGC0659", "NGC0744", "NGC2367", "NGC2414", "NGC2489", "NGC5823", "NGC6830", "NGC7510", "NGC2374", "NGC2395", "NGC6259", "NGC6546", "NGC6647", "NGC6883", "NGC0188", "NGC6152", "IC2714", "NGC0637", "NGC1907", "NGC3496", "NGC3590", "NGC6204", "NGC6249", "NGC6451", "NGC6469", "NGC1968", "NGC2420", "NGC2421", "NGC2453", "NGC2925", "NGC3960", "NGC6738", "NGC7062", "NGC2055", "IC2157", "NGC1245", "NGC1513", "NGC2324", "NGC2383", "NGC2627", "NGC4439", "NGC5925", "NGC7086", "NGC7261", "NGC2215", "NGC2194", "NGC2236", "NGC2331", "NGC6031", "NGC6192", "NGC6396", "NGC6645", "NGC7790", "NGC2158", "NGC2204", "NGC2659", "NGC4815", "NGC6568", "NGC2186", "NGC0189", "NGC0436", "NGC2660", "NGC3033", "NGC4052", "NGC5749", "NGC6400", "NGC6802", "M26", "NGC0956", "NGC2250", "NGC2299", "NGC4337", "NGC4852", "NGC6649", "NGC5999", "NGC6625", "IC1442", "NGC0146", "NGC2112", "NGC2254", "NGC5168", "NGC7031", "NGC2587", "NGC2658", "NGC6704", "NGC7245", "NGC2050", "NGC0381", "NGC2509", "NGC7142", "NGC1747", "NGC0133", "NGC2141", "NGC2243", "NGC4230", "NGC6683", "NGC7788", "NGC0559", "NGC2266", "NGC2451", "NGC6268", "NGC6791", "NGC0330", "NGC2042", "NGC1496", "NGC2311", "NGC2479", "NGC6507", "NGC7226", "IC4291", "NGC2355", "NGC2580", "NGC3105", "NGC7067", "NGC7128", "NGC7295", "NGC1848", "NGC0103", "NGC5715", "NGC6115", "NGC2972", "NGC1761", "NGC1984", "NGC2269", "NGC2304", "NGC6583", "NGC6216", "NGC1845", "NGC2432", "NGC2455", "NGC6253", "NGC1970", "NGC1974", "NGC2037", "NGC2015", "NGC1782", "NGC2309", "NGC1951", "NGC2011", "NGC2044", "NGC6404", "NGC6756", "NGC1767", "NGC1605", "NGC6005", "NGC2098", "NGC1735", "NGC1774", "NGC2259", "NGC5120", "NGC1967", "NGC2006", "NGC0376", "NGC2192", "NGC1787", "NGC2214", "NGC2025", "NGC1772", "NGC2027", "NGC0609", "NGC3255", "NGC2009", "NGC1860", "NGC6603", "NGC1913", "NGC2635", "NGC2065", "NGC2096", "NGC2102", "NGC1962", "NGC1704", "NGC1820", "NGC1922", "NGC2107", "NGC2093", "NGC2671", "NGC2033", "NGC2127", "NGC2117", "NGC0458", "NGC2051", "IC0166", "IC0361", "NGC1965", "NGC6631", "NGC0290", "NGC2010", "NGC0299", "NGC2172", "NGC0361", "NGC1902", "NGC2056", "NGC1220", "NGC1839", "NGC2368", "NGC2588", "NGC5288", "NGC6318", "NGC1966", "NGC2058", "NGC2319", "NGC1898", "NGC1804", "NGC1810", "NGC1971", "NGC2038", "IC1611", "NGC1885", "NGC1883", "NGC7044", "NGC1825", "NGC2021", "NGC0306", "NGC2091", "NGC2145", "NGC1844", "NGC1823", "NGC0411", "NGC2000", "NGC1894", "NGC2160", "NGC0265", "NGC1959", "NGC2057", "NGC2053", "NGC2109", "NGC1766", "NGC1836", "NGC0294", "NGC1718", "NGC0152", "NGC1859", "NGC1837", "NGC2029", "NGC1732", "IC1612", "NGC1882", "NGC2213", "NGC1793", "NGC1815", "IC1624", "NGC1795", "NGC2140", "NGC2111", "NGC1969", "NGC1847", "NGC1928", "NGC2088", "NGC2114", "NGC0256", "NGC1702", "NGC2849", "NGC1828", "NGC1775", "NGC1830", "NGC1764", "NGC0269", "NGC1193", "NGC2401", "NGC5764", "NGC1946", "NGC1972", "NGC0222", "NGC2046", "NGC2137", "NGC2062", "NGC1887", "NGC1813", "NGC1849", "NGC2036", "NGC1768", "NGC1890", "NGC2177", "NGC2059", "NGC1864", "NGC2166", "NGC0231", "NGC2028", "NGC1865", "NGC2116", "NGC1838", "NGC1878", "NGC2147", "NGC1921", "NGC7419", "NGC0176", "NGC1776", "NGC0602", "NGC1816", "NGC2095", "IC1311", "NGC1734", "NGC2066", "NGC1791", "NGC1822", "NGC2047", "NGC1861", "NGC1950", "NGC1905", "NGC2072", "NGC1826", "NGC2241", "NGC0422", "NGC1733", "NGC1862", "NGC1867", "NGC2118", "NGC1997", "NGC1942", "NGC1897", "IC1660", "NGC1749", "NGC1900", "NGC1933", "IC1626", "NGC1696", "IC1655", "NGC1842", "IC1662", "NGC1673", "NGC6882", "NGC6846", "NGC0220", "NGC1663", "IC1641", "NGC0292", "M31", "M33", "NGC5128", "M81", "M83", "M101", "NGC0055", "M104", "M110", "M32", "NGC6822", "NGC0300", "M94", "NGC6744", "M51", "NGC2403", "M82", "M106", "M64", "NGC1316", "M63", "M87", "M60", "NGC1269", "M77", "M86", "M66", "NGC3521", "M85", "NGC2903", "NGC0247", "NGC4631", "IC0127", "IC4820", "NGC0185", "NGC2841", "NGC6868", "M96", "NGC7793", "M65", "NGC1023", "M100", "NGC1553", "NGC2997", "M74", "NGC1097", "NGC3628", "NGC7331", "IC0010", "NGC0147", "M90", "NGC5195", "NGC3621", "M59", "NGC1399", "NGC1365", "NGC4449", "M61", "NGC5102", "M58", "NGC1407", "NGC1672", "NGC4125", "NGC1566", "M95", "NGC4494", "M89", "M105", "NGC1549", "NGC2683", "NGC4490", "NGC3923", "NGC3344", "NGC1232", "NGC2768", "M99", "M109", "M102", "NGC0891", "NGC1380", "NGC4214", "NGC1808", "NGC4753", "NGC1433", "NGC1313", "NGC1404", "IC1613", "NGC4216", "NGC4559", "NGC5068", "NGC2935", "NGC3109", "M108", "NGC4236", "NGC4450", "NGC4395", "NGC0134", "NGC0925", "NGC4414", "NGC3077", "M98", "NGC2784", "NGC2976", "NGC4278", "NGC4438", "NGC0908", "NGC1792", "NGC4473", "NGC4976", "NGC1617", "NGC6503", "NGC2681", "NGC3489", "NGC0772", "NGC1340", "NGC4546", "NGC3198", "NGC3377", "NGC3938", "NGC7424", "NGC3557", "NGC4274", "NGC5061", "NGC1300", "NGC2442", "NGC2613", "NGC4477", "NGC3640", "NGC1559", "NGC6684", "NGC5813", "IC5267", "NGC1052", "NGC5101", "NGC0584", "NGC1574", "NGC2775", "M84", "NGC5253", "NGC4664", "NGC5363", "NGC1350", "NGC4656 NED01", "NGC3486", "NGC1326", "NGC1512", "NGC3412", "NGC4536", "NGC5566", "NGC3359", "NGC7552", "NGC4314", "NGC1055", "NGC2146", "NGC1543", "NGC2985", "NGC3091", "NGC3147", "NGC3718", "NGC7582", "NGC1201", "NGC2207", "NGC6951", "NGC3893", "NGC1387", "NGC7144", "IC5332", "NGC0045", "NGC1084", "NGC4111", "NGC7049", "NGC4618", "NGC5170", "NGC5474", "NGC1947", "NGC4435", "NGC1964", "NGC4371", "NGC3223", "NGC4242", "NGC7479", "NGC3079", "IC2574", "NGC3193", "NGC5701", "IC5152", "NGC0986", "NGC1379", "NGC1533", "NGC1546", "NGC4651", "NGC0578", "NGC2986", "NGC3311", "NGC6902", "NGC1385", "NGC1400", "NGC3904", "NGC5576", "NGC1596", "NGC1961", "NGC3136", "NGC5161", "NGC5530", "NGC6340", "NGC1042", "NGC1317", "NGC3261", "NGC4388", "IC5328", "NGC1515", "NGC1569", "NGC3250", "NGC4772", "NGC6753", "NGC7083", "NGC4373", "NGC7090", "NGC3078", "NGC3319", "NGC3705", "NGC4503", "IC4889", "NGC1374", "NGC2655", "NGC3706", "NGC4350", "NGC4691", "NGC0672", "IC4662", "NGC4027", "NGC6861", "IC5250A", "NGC7041", "NGC4564", "NGC5085", "NGC0150", "NGC3646", "NGC5266", "NGC5365", "NGC6015", "NGC3189", "NGC0315", "NGC0660", "NGC4419", "NGC4168", "NGC4461", "NGC4568", "NGC2090", "NGC4036", "NGC5638", "NGC5713", "NGC5845", "NGC6861D", "NGC7184", "NGC4062", "NGC7192", "NGC5585", "NGC6810", "NGC1386", "NGC4638", "NGC7145", "NGC3059", "NGC0625", "NGC6943", "NGC2434", "NGC7531", "IC4797", "IC5325", "NGC6215", "NGC4603", "NGC4889", "NGC6907", "NGC6925", "NGC7796", "IC5240", "NGC0821", "NGC4219", "NGC4567", "NGC7329", "NGC7741", "NGC4138", "NGC4709", "IC0334", "NGC3256", "NGC5011", "NGC5419", "NGC1022", "NGC4298", "NGC5775", "NGC5962", "NGC6703", "NGC1353", "NGC3347", "NGC4106", "NGC4157", "NGC7744", "IC4765", "NGC7755", "NGC1079", "NGC7098", "NGC5483", "NGC7412", "NGC2366", "NGC7418", "NGC4874", "NGC1744", "NGC5121", "NGC7599", "NGC0520 NED01", "NGC0839", "NGC6958", "NGC2865", "NGC1426", "IC5273", "NGC0777", "NGC4478", "NGC6482", "NGC6893", "NGC5377", "NGC0410", "NGC4151", "NGC5903", "NGC7020", "NGC3596", "NGC1381", "NGC1389", "NGC3367", "NGC0474", "NGC5090", "NGC5898", "NGC3358", "NGC4767", "IC4329", "IC5105", "NGC4462", "NGC6876", "NGC7196", "IC4441", "NGC1325", "NGC3087", "NGC4262", "NGC6758", "IC4845", "NGC4416", "NGC0024", "NGC2427", "NGC3095", "NGC7096", "NGC0151", "NGC6872", "IC3896", "NGC3038", "NGC3254", "NGC4421", "NGC0337", "NGC4302", "NGC5064", "NGC6438", "NGC7079", "IC3253", "NGC0890", "NGC2500", "NGC3665", "NGC3941", "IC4721", "NGC0266", "NGC2782", "NGC4150", "IC4214", "NGC0514", "NGC2639", "NGC6207", "IC5052", "NGC0718", "NGC3432", "NGC6851", "NGC1487 NED02", "NGC2983", "NGC3277", "NGC4550", "NGC4645", "IC5181", "NGC2537", "NGC2776", "NGC3982", "NGC5806", "NGC2139", "NGC7097", "NGC1640", "NGC3258", "NGC4312", "NGC4379", "NGC4440", "NGC0404", "NGC0895", "NGC3271", "NGC1156", "NGC4189", "NGC4835", "NGC1058", "NGC6769", "NGC2310", "NGC6870", "NGC6887", "NGC3268", "NGC0470", "NGC3309", "NGC6166", "NGC6875", "IC4946", "NGC2787", "NGC3227", "NGC7232", "IC5186", "NGC2541", "NGC7410", "IC4327", "NGC1060", "NGC7029", "NGC0254", "NGC2188", "NGC2648", "NGC3842", "NGC5964", "NGC3001", "NGC4425", "NGC7155", "NGC1518", "NGC2815", "NGC4636", "NGC6782", "NGC7166", "IC1459", "NGC0467", "NGC5188", "NGC7392", "NGC7168", "NGC4454", "NGC7457", "NGC2272", "NGC2693", "NGC6909", "IC5179", "NGC3885", "NGC4947", "NGC3655", "NGC3955", "NGC4679", "NGC4650", "NGC7653", "NGC5193", "NGC7217", "NGC2217", "NGC4485", "NGC4793", "NGC5371", "NGC7421", "NGC6770", "NGC7817", "NGC3437", "NGC0955", "NGC3318", "NGC3318A", "NGC4116", "IC1727", "NGC0949", "NGC4452", "NGC7625", "NGC1241", "NGC4203", "NGC5156", "NGC6776", "NGC0676", "NGC4930", "NGC6699", "IC2166", "NGC2822", "NGC7690", "NGC1393", "NGC4304", "NGC4551", "NGC5494", "NGC5033", "NGC3738", "NGC6721", "NGC7007", "NGC2916", "NGC0016", "NGC2907", "NGC4528", "NGC4839", "NGC7252", "NGC7587", "NGC0784", "NGC4283", "NGC4458", "NGC0541", "NGC1161", "NGC1310", "NGC3285", "NGC4143", "NGC5087", "NGC5375", "NGC7213", "IC2537", "NGC4785", "NGC6923", "NGC0217", "NGC3395", "NGC3998", "NGC4789", "NGC6935", "NGC6942", "NGC1288", "NGC2551", "IC3370", "NGC0148", "NGC4383", "NGC4387", "NGC7221", "NGC0383", "NGC2344", "NGC5612", "NGC6962", "NGC7715", "NGC1482", "NGC2342", "NGC3310", "NGC4206", "NGC7174", "NGC3962", "NGC6845A", "IC0750", "IC5156", "NGC0337A", "NGC3185", "M49", "NGC2992", "NGC1184", "NGC3336", "NGC4476", "NGC5839", "NGC5302", "NGC0922", "NGC3557B", "NGC3564", "NGC4292", "NGC5084", "IC1558", "NGC5485", "NGC7124", "NGC7702", "IC4837", "NGC2487", "NGC2855", "NGC4936", "NGC4941", "IC4933", "NGC4407", "NGC7014", "NGC7771", "NGC5770", "NGC5832", "NGC2857", "NGC4698", "NGC3244", "IC4842", "NGC7070", "NGC0499", "NGC6854", "NGC7059", "NGC7764", "NGC4193", "NGC2798", "NGC4861", "NGC2663", "NGC7080", "NGC4169", "NGC4744", "NGC7469", "NGC4625", "NGC7154", "IC5131", "NGC3308", "NGC7126", "IC1788", "NGC5560", "NGC7125", "NGC7798", "NGC0959", "NGC2563", "NGC5264", "NGC5398", "NGC5574", "NGC6389", "NGC7070A", "NGC7248", "NGC1375", "NGC3516", "NGC0969", "NGC1380A", "NGC3169", "NGC6012", "NGC6878", "IC4852", "NGC4565", "NGC4627", "NGC5329", "NGC5656", "IC1970", "NGC0693", "NGC0881", "NGC4479", "NGC4622", "NGC4725", "NGC0835", "NGC2179", "NGC5953", "NGC6239", "NGC5507", "NGC1383", "NGC3100", "NGC4497", "NGC5859", "NGC1275", "NGC1796", "NGC5395", "NGC0252", "NGC1140", "NGC0706", "NGC3396", "NGC3788", "NGC3816", "NGC4647", "NGC7361", "NGC2336", "IC0749", "NGC4105", "NGC6771", "NGC4248", "NGC5623", "NGC0491", "NGC3257", "NGC5150", "NGC6500", "NGC3445", "NGC4491", "NGC5631", "NGC1705", "NGC2552", "NGC5016", "IC4813", "NGC3568", "NGC3687", "NGC4396", "NGC7250", "NGC0059", "NGC0568", "NGC6808", "IC5003", "NGC2535", "NGC2208", "NGC6305", "NGC6877", "NGC5861", "IC2233", "NGC0473", "NGC7320", "NGC2993", "NGC3648", "NGC3921", "NGC6359", "IC1029", "IC4836", "NGC6984", "NGC0842", "IC4299", "NGC0304", "NGC3861", "NGC4677", "NGC5237", "NGC2915", "NGC4357", "NGC6970", "NGC2959", "NGC7064", "IC4170 NED01", "NGC0163", "NGC1800", "NGC2685", "NGC3023", "NGC5347", "NGC0392", "NGC0613", "NGC0873", "NGC5592", "IC5020", "NGC0670", "NGC2619", "NGC4639", "NGC7156", "NGC0855", "NGC3656", "NGC4782", "NGC0788", "NGC3607", "NGC7673", "NGC1167", "NGC3305", "NGC7377", "IC2082 NED01", "IC2082 NED02", "NGC3353", "IC2584", "NGC4603D", "NGC4616", "NGC4783", "NGC6967", "NGC1050", "NGC1394", "NGC7072", "NGC7563", "NGC0935", "NGC6599", "NGC7233", "IC5110", "NGC1325A", "NGC4085", "NGC5258", "IC4219", "NGC4816", "NGC5077", "NGC1667", "NGC2146A", "NGC3512", "NGC3573", "NGC3994", "NGC4261", "NGC0906", "NGC2341", "NGC3821", "NGC3884", "IC1616", "NGC4431", "NGC6251", "NGC5464", "NGC4827", "NGC1382", "NGC3085", "NGC4051", "NGC1311", "NGC3273", "NGC3504", "NGC5633", "NGC6708", "NGC4373A", "NGC5774", "IC2587", "NGC7539", "IC1959", "IC4767", "NGC1199", "NGC5140", "NGC4436", "NGC5912", "IC4296", "NGC4301", "NGC4645B", "NGC5257", "NGC6964", "IC0302", "NGC0311", "NGC0326 NED01", "NGC0833", "NGC3125", "NGC3325", "NGC4635", "NGC4794", "NGC4853", "NGC6052 NED01", "NGC4952", "NGC6068", "NGC0575", "NGC3316", "NGC7185", "NGC2578", "NGC1358", "NGC2330", "NGC6702", "NGC0237", "NGC0262", "NGC2789", "NGC2861", "NGC2936", "NGC4575", "NGC6850", "NGC0165", "NGC6300", "NGC2544", "NGC3096", "NGC4895", "NGC5289", "NGC5298", "NGC7052", "NGC7056", "NGC0169", "NGC4134", "NGC5211", "NGC7328", "NGC1029", "NGC2893", "NGC3314A", "NGC5857", "NGC7314", "NGC0216", "NGC5273", "NGC5394", "IC4832", "NGC1125", "NGC1412", "NGC3971", "NGC7219", "IC4718", "NGC0934", "IC4770", "IC5353", "NGC0612", "NGC1536", "NGC4593", "NGC5004", "NGC7514", "NGC0586", "NGC2832", "NGC3958", "NGC4797", "NGC4819", "NGC3354", "M88", "NGC7570", "IC0343", "IC4943", "NGC3065", "NGC7677", "NGC7764A", "IC1231", "IC2554", "NGC3641", "NGC4163", "NGC4553", "NGC6328", "IC5262", "NGC4073", "NGC5899", "IC1269", "NGC0131", "NGC3550 NED02", "NGC7199", "NGC7674", "NGC1510", "NGC3340", "NGC4860", "NGC4190", "NGC1373", "NGC2486", "NGC2675", "NGC4131", "NGC6711", "NGC3032", "NGC7743", "IC3475", "NGC0708", "NGC0622", "NGC4194", "NGC5311", "NGC7135", "NGC7720 NED01", "IC2560", "NGC4566", "NGC4743", "NGC5793", "NGC0687", "NGC1602", "NGC3226", "NGC3250B", "NGC4911", "NGC0545", "NGC0547", "NGC1391", "NGC4173", "NGC3267", "NGC4152", "NGC5091", "NGC5135", "NGC6880", "NGC7335", "NGC2623", "NGC4694", "NGC5735", "NGC7208", "NGC4355", "NGC5846A", "NGC6240", "NGC5900", "NGC0513", "NGC1681", "NGC3073", "NGC5728", "NGC3390", "NGC5000", "IC4766", "NGC5026", "NGC5256", "NGC5256 NED01", "IC4717", "NGC3783", "NGC7179", "NGC7536", "IC0794", "IC4972", "NGC0289", "NGC0926", "NGC3187", "NGC5622", "IC1222", "NGC0195", "NGC4175", "NGC6221", "NGC6347", "NGC4495", "NGC0801", "NGC4966", "NGC7808", "NGC0770", "NGC4378", "NGC6695", "NGC7140", "IC3639", "IC4293", "NGC3035", "NGC4706", "NGC4807", "NGC4908", "NGC5495", "NGC6454", "NGC2110", "NGC3269", "NGC5357", "IC3358", "NGC0017", "NGC4869", "NGC5365A", "NGC6969", "NGC6860", "NGC7319", "NGC2273", "NGC3265", "NGC3355", "NGC4165", "NGC4507", "NGC7165", "NGC7343", "IC1256", "IC2951", "NGC3081", "NGC0317A", "NGC4881", "NGC5304", "NGC7592B", "IC0093", "NGC3896", "NGC4253", "M91", "NGC5052", "IC4051", "NGC0454 NED02", "NGC4104", "NGC4650A", "NGC5909", "NGC2534", "IC5049B", "IC5063", "NGC1129", "NGC4235", "NGC5643", "NGC5695", "NGC7317", "NGC0871", "NGC3377A", "NGC7172", "IC0903", "NGC6013", "NGC6902B", "IC2446", "NGC3258A", "NGC4174", "NGC6707", "NGC0099", "NGC5262", "NGC5963", "IC4839", "NGC1272", "NGC2937", "NGC7535", "IC4806", "NGC3284", "NGC5005", "NGC5214", "NGC6761", "NGC7077", "NGC1067", "NGC4865", "NGC5995", "NGC5674", "NGC1242", "NGC2799", "NGC5548", "NGC5757", "NGC6269", "NGC3786", "NGC6306", "NGC1474", "NGC3262", "NGC7590", "IC4045", "NGC1522", "NGC7279", "NGC4683", "NGC4939", "NGC0863", "NGC4738", "NGC4907", "NGC6937", "IC4088", "IC4200", "IC5104", "NGC1476", "NGC4990", "NGC5266A", "NGC0394", "NGC2911", "IC0843", "IC1254", "IC4951", "NGC0662", "NGC3840", "NGC4370", "IC3946", "IC1900", "NGC4898A", "NGC3844", "NGC4864", "NGC6926", "NGC7130", "IC4553", "IC4970", "NGC6217", "NGC1542", "IC0558", "NGC0591", "NGC7496", "NGC6982", "IC0842", "NGC1128 NED02", "NGC2536", "IC4838", "NGC0317B", "NGC4323", "NGC3393", "NGC4789A", "NGC3312", "NGC5427", "NGC5780", "NGC0253", "NGC0986A", "NGC3862", "NGC5249", "NGC6630", "IC1801", "IC3349", "IC4719", "NGC1297", "NGC4514", "IC4448", "NGC1614", "NGC2329", "NGC3288", "NGC4132", "IC3990", "IC4840", "NGC1320", "NGC1692", "NGC5291", "NGC5929", "IC4042", "NGC5477", "NGC7603", "NGC3281", "NGC4135", "NGC6890", "IC3959", "IC3973", "NGC4748", "NGC4850", "IC4713", "NGC3534", "NGC3642", "NGC3068", "NGC5283", "IC4995", "NGC4871", "NGC4906", "NGC1592", "IC0184", "NGC2691", "NGC4872", "NGC6068A", "NGC7214", "NGC0533", "NGC0424", "NGC2622", "NGC4385", "IC3943", "NGC3289", "NGC4873", "NGC1278", "NGC4867", "IC2637", "IC0632", "NGC1194", "NGC4876", "NGC5597", "IC0450", "IC0745", "IC2227", "IC3059", "IC5345", "NGC1273", "NGC4601", "NGC5004A", "NGC7310", "IC0904", "IC2443", "NGC4854", "NGC5252", "NGC6814", "NGC7672", "IC4516", "NGC4585", "NGC5985", "NGC3250C", "NGC3741", "NGC7768", "IC3303", "IC3393", "NGC2718", "IC0588", "NGC2968", "NGC4672", "IC0497", "IC1816", "IC3949", "IC5169", "NGC4883", "NGC5972", "IC4247", "NGC0985", "NGC6845B", "NGC4886", "NGC7609 NED01", "IC4130", "IC4687", "NGC5421", "NGC7236", "IC3955", "NGC2150", "NGC4156", "NGC4700", "NGC5968", "NGC6764", "NGC4898B", "NGC6274 NED01", "NGC7450", "NGC4137", "IC1574", "IC3991", "IC4974 NED01", "NGC7714", "NGC5506", "IC0751", "NGC3260", "IC0414", "NGC4945", "NGC1144", "IC3976", "IC5256", "NGC4735", "NGC7466", "NGC7730", "IC4810", "NGC4074", "NGC1229", "NGC3660", "NGC7647", "IC3960", "NGC4583", "NGC0490", "NGC3307", "NGC0526B", "NGC2989", "NGC7399", "NGC7349", "NGC7658B", "IC3363", "IC2073", "IC0839", "IC3457", "IC4249", "NGC4875", "NGC0397", "NGC0526A", "IC2429", "IC3947", "IC3998", "IC0633", "NGC6314", "IC4026", "IC4777", "IC4870", "IC4012", "IC2477", "IC3451", "NGC4922 NED02", "NGC5004B", "IC4032", "NGC7811", "NGC0617", "NGC2831", "NGC2961", "IC3957", "IC3963", "IC5358", "IC2032", "IC3056", "IC3388", "IC4218", "IC2049", "NGC0931", "IC2404", "IC4021", "NGC7287", "IC4040", "IC2744", "IC4041", "NGC2377", "NGC1028", "NGC4968", "IC0399", "IC4248", "IC1854", "NGC6851B", "NGC7432", "IC1575", "IC3355", "NGC0060", "NGC3534B", "IC1969", "IC3461", "IC4590", "NGC2484", "NGC5940", "NGC2604", "IC1198", "NGC4851", "NGC4895A", "IC3443", "NGC1019", "NGC0449", "NGC4949", "IC4892", "IC4396", "NGC4922 NED01", "NGC2656", "NGC3051", "NGC4792", "NGC6061", "NGC7436A", "NGC7592A", "NGC0918", "NGC4858", "NGC4894", "IC4011", "IC3222", "IC3441", "NGC0880", "IC3402", "IC3383", "NGC1685", "IC1182", "IC0123", "NGC1410", "IC4033", "IC4030", "IC3492", "IC3968", "IC0355", "IC3467", "IC3576", "IC5289 NED02", "NGC7408", "IC3386", "IC4044", "IC0277", "NGC0025", "NGC0879", "NGC5490", "IC4546", "IC4638", "NGC0426", "NGC5750", "NGC6998", "IC3445", "NGC4471", "IC3506", "IC4316", "NGC5804", "NGC1980", "NGC2264", "M42", "NGC1981", "NGC6530", "NGC2239", "M8", "NGC6250", "IC4703", "M16", "IC1805", "IC1848", "NGC3324", "NGC6164", "NGC6165", "NGC2175", "M17", "NGC6823", "IC5146", "NGC7380", "NGC2070", "NGC7293", "M27", "NGC3247", "NGC3242", "M78", "NGC7009", "NGC3918", "NGC6572", "NGC7662", "M1", "M20", "NGC7027", "M57", "NGC1955", "NGC2014", "M43", "NGC6543", "NGC3132", "NGC6818", "NGC1360", "NGC1763", "NGC2440", "IC0418", "NGC6826", "NGC2060", "NGC1535", "NGC6302", "NGC2392", "NGC1910", "NGC6210", "NGC2867", "NGC5315", "NGC1858", "M97", "NGC6997", "NGC1871", "M76", "NGC1931", "NGC2069", "NGC5882", "NGC1514", "IC4406", "IC2553", "IC2448", "IC2501", "NGC2080", "NGC2122", "NGC1873", "IC2165", "IC4997", "NGC1934", "NGC6790", "NGC6891", "IC3568", "IC4191", "NGC1948", "IC1297", "IC4593", "NGC3211", "NGC6644", "NGC7008", "IC2149", "IC4776", "NGC2438", "NGC2103", "NGC2083", "NGC2018", "NGC2078", "IC4634", "NGC0246", "NGC4361", "NGC6153", "NGC6884", "NGC7026", "NGC2035", "IC5148", "NGC5873", "NGC6563", "NGC6567", "IC2128", "NGC6905", "IC1266", "IC2621", "NGC2371", "NGC5307", "NGC6445", "NGC1923", "NGC1743", "IC2105", "IC5217", "NGC3699", "NGC6629", "IC2003", "NGC6369", "NGC6781", "NGC6803", "NGC6886", "NGC2040", "NGC2075", "IC2067", "IC5117", "NGC1501", "NGC5979", "NGC6309", "NGC6741", "NGC7129", "NGC1936", "NGC2022", "NGC2346", "NGC2792", "NGC2818", "NGC3195", "NGC6537", "NGC6565", "NGC1714", "IC1644", "NGC6072", "NGC1876", "NGC2077", "NGC1624", "NGC2899", "NGC2079", "NGC2261", "NGC0040", "IC0351", "IC4846", "NGC6751", "IC1747", "IC2145", "NGC1941", "NGC2086", "NGC2452", "NGC6804", "NGC6807", "NGC1914", "IC0466", "NGC2085", "IC4732", "NGC6833", "NGC7048", "NGC2048", "NGC7354", "NGC2030", "NGC1748", "NGC6337", "NGC6778", "NGC6894", "NGC1949", "IC1295", "IC4637", "IC4663", "NGC6879", "NGC1920", "NGC6439", "NGC6852", "NGC2610", "NGC6620", "NGC6772", "NGC1814", "NGC1874", "NGC1880", "NGC6026", "NGC6058", "NGC6578", "NGC6765", "NGC1895", "IC4673", "IC4699", "NGC4071", "NGC6842", "IC0289", "NGC7139", "NGC1745", "NGC6742", "NGC7094", "NGC7076", "IC0972", "NGC6881", "IC1454", "IC0142", "IC2116", "IC0430", "NGC0588", "IC0132", "NGC2242", "NGC0104", "M10", "NGC6397", "NGC5139", "M4", "M19", "NGC2808", "M14", "M13", "M5", "M12", "M71", "M22", "M2", "NGC6752", "M15", "M3", "M55", "M92", "NGC0362", "M28", "NGC5986", "M30", "NGC6235", "NGC1851", "M80", "NGC6541", "M62", "NGC6356", "NGC6284", "M54", "NGC4833", "M53", "M68", "NGC6441", "NGC0288", "M79", "NGC6584", "NGC3201", "M75", "NGC5286", "M69", "M56", "M9", "NGC5897", "IC4499", "NGC1261", "NGC6712", "M107", "NGC5927", "NGC6362", "NGC6352", "NGC2298", "NGC1850", "M72", "NGC6293", "NGC6304", "NGC6316", "M70", "NGC6569", "NGC6522", "NGC5824", "NGC6144", "NGC6139", "NGC6638", "NGC5466", "NGC1866", "NGC6652", "NGC6934", "NGC6760", "NGC1755", "NGC4372", "NGC6535", "NGC6229", "NGC6544", "NGC5053", "NGC6342", "NGC2419", "NGC5634", "NGC1856", "NGC6101", "NGC6440", "NGC2157", "NGC6642", "NGC6287", "NGC2164", "NGC6717", "NGC2041", "NGC1916", "NGC1854", "NGC7006", "NGC7492", "NGC0419", "NGC1835", "NGC6528", "NGC1978", "NGC2136", "NGC6401", "NGC5946", "NGC4147", "NGC2031", "NGC2002", "NGC2019", "NGC5694", "NGC1783", "NGC2210", "NGC1872", "NGC6355", "NGC1986", "NGC1711", "NGC1831", "NGC0121", "NGC1870", "NGC2203", "NGC6558", "NGC2003", "NGC1846", "NGC2156", "NGC2159", "NGC1841", "NGC1754", "NGC1868", "NGC2005", "NGC1466", "NGC1751", "NGC1953", "NGC0416", "NGC1926", "NGC2154", "NGC1939", "NGC1944", "NGC1903", "NGC1943", "NGC2173", "NGC1940", "NGC1852", "NGC2135", "NGC1698", "NGC2130", "NGC1695", "NGC1801", "NGC2105", "NGC0339", "NGC2249", "NGC1756", "NGC1651", "NGC2108", "NGC1917", "NGC2121", "NGC6749", "IC2146", "NGC2123", "NGC2155", "NGC1697", "NGC2257", "NGC2120", "NGC1629", "NGC2162", "NGC1777", "NGC1644", "NGC1693", "NGC2190", "NGC2161", "NGC1958", "NGC2153", "NGC1789", "NGC1938", "NGC1649", "NGC2209", "NGC2231", "NGC2193", "NGC2197", "IC2140", "NGC2181", "NGC2097", "NGC2138", "IC2134", "IC2148", "IC2161", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "NEPTUNE", "URANUS", "SIRIUS", "CANOPUS", "ARCTURUS", "RIGIL KENTAURUS", "VEGA", "CAPELLA", "RIGEL", "PROCYON", "ACHERNAR", "BETELGEUSE", "HADAR", "ALTAIR", "ACRUX", "ALDEBARAN", "SPICA", "ANTARES", "POLLUX", "FOMALHAUT", "BECRUX", "DENEB", "REGULUS", "ADHARA", "CASTOR", "GACRUX", "SHAULA", "BELLATRIX", "ALNATH", "MIAPLACIDUS", "ALNILAM", "ALNAIR", "ALNITAK", "ALIOTH", "MIRPHAK", "KAUS AUSTRALIS", "DUBHE", "WEZEN", "ALKAID", "AVIOR", "SARGAS", "MENKALINAN", "ATRIA", "ALHENA", "PEACOCK", "POLARIS", "MIRZAM", "ALPHARD", "HAMAL", "ALGIEBA", "DIPHDA", "NUNKI", "MENKENT", "ALPHERATZ", "MIRACH", "SAIPH", "KOCHAB", "RASALHAGUE", "ALGOL", "ALMAAK", "DENEBOLA", "CIH", "NAOS", "TUREIS", "ALPHEKKA", "MIZAR", "SADR", "SHEDIR", "ETAMIN", "MINTAKA", "CAPH", "DSCHUBBA", "MERAK", "IZAR", "ENIF", "ANKAA", "PHAD", "SCHEAT", "ALUDRA", "ALDERAMIN", "GIENAH", "MARKAB", "MENKAR", "ZOSMA", "GRAFFIAS", "ARNEB", "GIENAH GHURAB", "ZUBENESCHEMALI", "UNUKALHAI", "SHERATAN", "PHAKT", "KRAZ", "RUCHBAH", "MUFRID", "HASSALEH", "KAUS MERIDIONALIS", "TARAZED", "PORRIMA", "HATSYA", "ZUBENELGENUBI", "CEBALRAI", "CURSA", "KORNEPHOROS", "RASALGETHI", "RASTABAN", "NIHAL", "KAUS BOREALIS", "ALGENIB", "ALCYONE", "VINDEMIATRIX", "ACAMAR", "ALBALDAH", "GOMEISA", "COR CAROLI", "SADALSUUD", "MATAR", "ALGORAB", "SADALMELIK", "ZAURAK", "RAS ELASED AUSTRALIS", "NASH", "ALBIREO", "MEGREZ", "SHELIAK", "THUBAN", "ALSHAIN", "ALCOR", "82 G. ERI", "96 G. PSC", "268 G. CET", "P ERIDANI"], "index": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1483, 1484, 1485, 1486, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2141, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154, 2155, 2156, 2157, 2158, 2159, 2160, 2161, 2162, 2163, 2164, 2165, 2166, 2167, 2168, 2169, 2170, 2171, 2172, 2173, 2174, 2175, 2176, 2177, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2304, 2305, 2306, 2307, 2308, 2309, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2323, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332, 2333, 2335, 2336, 2337, 2338, 2339, 2340, 2341, 2342, 2343, 2344, 2345, 2346, 2347, 2349, 2350, 2351, 2352, 2353, 2355, 2356, 2357, 2359, 2360, 2361, 2362, 2363, 2364, 2366, 2370, 2371, 2372, 2374, 2375, 2377, 2378, 2379, 2381, 2382, 2383, 2386, 2387, 2388, 2390, 2392, 2393, 2394, 2395, 2397, 2398, 2399, 2401, 2406, 2407, 2411, 2412, 2414, 2415, 2416, 2417, 2418, 2420, 2422, 2426, 2427, 2433, 2434, 2442, 2443, 2444, 2445, 2449, 2452, 2454, 2455, 2456, 2458, 2459, 2475, 2528, 2585, 2639, 2659, 2807, 2970, 6035, 6299, 6393]};
</script>
<script>

var global_day_style = {
	cross 		: 'blue',
	constelations 	: 'yellow',
	bearing 	: 'green',
	star		: 'white',
	altaz		: 'red',
	target		: 'cyan',
	align		: 'magenta'
};

var global_show_obj = {
	'S': true,
	'Oc': true,
	'Gc': true,
	'Ca': true,
	'Ga':true,
	'Ne':true,
    	'P': true,
};

var global_night_style = {
	cross 		: 'red',
	constelations 	: '#880000',
	bearing 	: 'red',
	star		: 'red',
	altaz		: 'red',
	target		: '#AA0000',
	align		: '#AA0000'
};



var global_style = global_day_style;

var global_targets_list = [];
var global_prev_xy=null;
var global_target_index = -1;
var global_align_index = -1;
var global_expecting_select = null;
var global_camera_projection = true;
var global_expected_frame_rate_ms = 66;
var global_use_compass = false;
var global_dso_mag = parseInt(document.getElementById('dso_level_val').innerHTML);

var global_fov_index = 3;
var global_fov_values = [7,15,30,60,90,120,150]
var global_fov = global_fov_values[global_fov_index];
var global_mag = 4;
var gdata = {
	"lat" : 31.9,
	"lon" : 34.8,
	"compass_alpha" : 0,
	"alpha" : 0,
	"alpha_user_offset" : 0,
	"alpha_gyro" : 0,
	"alpha_diff" : 0,
	"beta" : 0,
	"gamma" : 0,
	"time" : Date.now(), //1614716453109
}

var global_align_matrix = [1,0,0,0,1,0,0,0,1];
var global_use_gyro = false;
var global_full_screen = false;

var global_status = "";


function showManual(v)
{
	document.getElementById('manual').style.display = v ? 'inline' : 'none';
}
function setDisplayByClass(cls,value)
{
	var el = document.getElementsByClassName(cls);
	for(var i=0;i<el.length;i++) {
		el[i].style.display = value;
	}
}

function smallScreen(v)
{
	var tiny = v ? 'inline' : 'none';
	var full = v ? 'none' : 'inline';
	setDisplayByClass('only_tiny',tiny);
	setDisplayByClass('only_full',full);
}


function showStatus(v)
{
	global_status += v+"<br/>"
	document.getElementById('status').innerHTML = global_status;
}

function showConfig(v)
{
	document.getElementById('config').style.display = v;
}
function toggleFS(fs)
{
	if(fs) {
		document.documentElement.requestFullscreen({navigationUI:'hide'});
	}
	else {
		document.exitFullscreen();
	}
}


function findTargetByName(name ='')
{
	var found = document.getElementById('find_status')
	var name = name.toUpperCase();
	var N=allstars_index_name.names.length;
	var found_index = -1;
	if(name != '') {
		for(var i=0;i<N;i++) {
			let candidate = allstars_index_name.names[i];
			if(candidate == name) {
				found_index = i;
				break;
			}
			else if(found_index != -2 && candidate.startsWith(name)) {
				if(found_index == -1) {
					found_index = i;
				}
				else {
					found_index = -2;
				}
			}
		}
	}
	if(found_index >= 0) {
		global_target_index = allstars_index_name.index[found_index];
		found.innerHTML = allstars[global_target_index].name;
	}
	else {
		global_target_index = -1;
		found.innerHTML = '';
	}
}
function incMAG()
{
	if(global_mag < 6)
		global_mag += 1;
	updateMAG()
}
function decMAG()
{
	if(global_mag > 1)
		global_mag -=1;
	updateMAG();
}
function updateMAG()
{
	document.getElementById("mag_val").innerHTML = global_mag + "";
}

function incFOV()
{
	if(global_fov_index + 1 < global_fov_values.length)
		global_fov_index++;
	updateFOV()
}
function decFOV()
{
	if(global_fov_index > 0)
		global_fov_index--;
	updateFOV();
}
function updateFOV()
{
	global_fov = global_fov_values[global_fov_index];
	document.getElementById("fov_val").innerHTML = global_fov + "&deg;";
}

function setUseGyro(val,message=null)
{
	global_use_gyro = val;
	if(message)
		var status = message;
	else
		var status= global_use_gyro ? "Aligned" : "Not Aligned";
	document.getElementById("alignment").innerHTML = status
}

function resetAll()
{
	global_expecting_select = null;
	findTargetByName();
	global_target_index = -1;
	document.getElementById('find_status').innerHTML = '';
	global_align_index = -1;
	setUseGyro(false);
}

function align()
{
	if(global_expecting_select == doNothing)
		return;
	/// realign in manual mode
	if(global_use_gyro && !global_use_compass) {
		// keep bearing
		gdata.alpha_user_offset = gdata.alpha_gyro + gdata.alpha_diff - gdata.alpha;
	}
	setUseGyro(false,"Select Star");
	global_align_index = -1;
	global_expecting_select = selectAlignWithTimer;
}

function normV(v)
{
	var len = Math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
	return [v[0]/len,v[1]/len,v[2]/len];
}

function matMul(A,B)
{
	var v1 = mvec(A,[B[0],B[3],B[6]]);
	var v2 = mvec(A,[B[1],B[4],B[7]]);
	var v3 = mvec(A,[B[2],B[5],B[8]]);
	return [v1[0],v2[0],v3[0],
		v1[1],v2[1],v3[1],
		v1[2],v2[2],v3[2]];
}

function matAdd(A,alpha,B,beta)
{
	var res = [];
	for(var i=0;i<9;i++) {
		res.push(A[i]*alpha + B[i]*beta);
	}
	return res;
}

function matEye()
{
	return [1,0,0, 0,1,0, 0,0,1];
}

function doNothing(index)
{
}

function selectAlignWithTimer(index,start_val=3)
{
	var cd = document.getElementById("countdown");
	global_align_index = index;
	global_expecting_select = doNothing;
	if(start_val <= 0) {
		cd.innerHTML="";
		selectAlign(index);
	}
	else {
		cd.innerHTML = start_val.toFixed(1) + "s";
		setTimeout(function() {
			selectAlignWithTimer(index,start_val - 0.1);
		},100);
	}
}

function selectAlign(index)
{
	var camRays =  getCameraRays();
	var st = allstars[index];
	var tr = rayFromPos(st.RA,st.DE);
	var fw = camRays[2];
	var left = camRays[1];
	var dAZ = Math.asin(crossProd(normV([tr[0],tr[1],0]),normV([fw[0],fw[1],0]))[2]);
	var dAlt = Math.asin(tr[2]) - Math.asin(fw[2]);
	// rotate around AZ axis
	var daz_mat =  [  Math.cos(dAZ), Math.sin(dAZ), 0,
			 -Math.sin(dAZ), Math.cos(dAZ), 0,
			 0,		 0,		1];
	// rotate around up/dwn - axis of the camera
	var u0 = left[0];
	var u1 = left[1];
	var u2 = left[2];
	var W = [ 0, -u2, u1,   u2, 0, -u0,  -u1, u0, 0 ]
	var dalt_mat = matAdd(matEye(),1,W,Math.sin(-dAlt));
	dalt_mat = matAdd(dalt_mat,1,matMul(W,W),2*Math.sin(-dAlt/2)*Math.sin(-dAlt/2));
	
	//global_align_matrix = daz_mat;
	global_align_matrix = matMul(daz_mat,dalt_mat); 
	
	setUseGyro(true);
	gdata.alpha_diff = (gdata.alpha + gdata.alpha_user_offset) - gdata.alpha_gyro;
	global_align_index = index;
	global_expecting_select = selectTaret;
}

/// rotation matrix is 
/// taken from https://www.w3.org/TR/2016/CR-orientation-event-20160818/#worked-example-2

var degtorad = Math.PI / 180; // Degree-to-Radian conversion


function getRotationMatrix( alpha, beta, gamma ) {

  var _x = beta  ? beta  * degtorad : 0; // beta value
  var _y = gamma ? gamma * degtorad : 0; // gamma value
  var _z = alpha ? alpha * degtorad : 0; // alpha value

  var cX = Math.cos( _x );
  var cY = Math.cos( _y );
  var cZ = Math.cos( _z );
  var sX = Math.sin( _x );
  var sY = Math.sin( _y );
  var sZ = Math.sin( _z );

  //
  // ZXY rotation matrix construction.
  //

  var m11 = cZ * cY - sZ * sX * sY;
  var m12 = - cX * sZ;
  var m13 = cY * sZ * sX + cZ * sY;

  var m21 = cY * sZ + cZ * sX * sY;
  var m22 = cZ * cX;
  var m23 = sZ * sY - cZ * cY * sX;

  var m31 = - cX * sY;
  var m32 = sX;
  var m33 = cX * cY;

  return [
    m11,    m12,    m13,
    m21,    m22,    m23,
    m31,    m32,    m33
  ];

};

function mvec(m,v)
{
	return [ m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
		 m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
		 m[6] * v[0] + m[7] * v[1] + m[8] * v[2] ];
}

function crossProd(a,b)
{
	return [ a[1]*b[2] - a[2]*b[1],
		 a[2]*b[0] - a[0]*b[2],
		 a[0]*b[1] - a[1]*b[0] ];
}

function getCameraRays()
{
	// zxy
	// after Mul comonents are [S,E,D]
	var alpha = global_use_gyro ? gdata.alpha_gyro + gdata.alpha_diff : gdata.alpha + gdata.alpha_user_offset;
	var M = getRotationMatrix(alpha,gdata.beta,gdata.gamma);
	//var top = mvec(M,[1,0,0]);
	//var lft = mvec(M,[0,1,0]);
	//var fwd = mvec(M,[0,0,-1]);
	
	

	var fwd = mvec(M,[0,1,0]);

	// make sure left  is horizontal

	var fwd_hlen = Math.sqrt(fwd[0]*fwd[0] + fwd[1]*fwd[1])
	var fwd_hor = [fwd[0]/fwd_hlen,fwd[1]/fwd_hlen,0.0];

	var lft = [-fwd_hor[1],fwd_hor[0],0.0]
	var top = crossProd(fwd,lft);

	if(global_use_gyro) {
		return [
			mvec(global_align_matrix,top),
			mvec(global_align_matrix,lft),
			mvec(global_align_matrix,fwd)
		];
	}
	else {
		return [top,lft,fwd];
	}
}

function rayFromPos(RAd,DEd)
{
	var deg2rad = Math.PI / 180;
	RA = RAd * deg2rad;
	DE = DEd * deg2rad;
	var jd = gdata.time * 1e-3 / 86400.0 + 2440587.5;
	var tu = jd - 2451545.0;
	var angle = Math.PI * 2 * (0.7790572732640+1.00273781191135448 * tu);
	var q = angle + gdata.lon*deg2rad;
	var H = q - RA;
	
	var f = deg2rad * gdata.lat;

	var az_y = Math.sin(H);
	var az_x = (Math.cos(H) * Math.sin(f) - Math.tan(DE) * Math.cos(f));
	var az = Math.atan2(az_y,az_x)
	var sinH = Math.sin(f) * Math.sin(DE) + Math.cos(f) * Math.cos(DE) * Math.cos(H);
	var hz = Math.asin(sinH)
	var ray_n = -Math.cos(az) * Math.cos(hz);
	var ray_e = -Math.sin(az) * Math.cos(hz);
	var ray_u = Math.sin(hz);
	return [ ray_e, ray_n, ray_u ];
}

function sprod(v1,v2)
{
	return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2];
}

function cameraBearing(RAd,DEd,cameraRays)
{
	var ray = rayFromPos(RAd,DEd);
	var top = cameraRays[0];
	var lft = cameraRays[1];
	var fwd = cameraRays[2];
	var x = -sprod(lft,ray);
	var y = sprod(top,ray);
	var z = sprod(fwd,ray);
	return {"x":x,"y":y,"z":z};
}

function getFOV()
{
	var ratio = canvas.width / canvas.height;
	var fov_td,fov_lr;
	if(ratio < 1) {
		fov_td = global_fov;
		fov_lr = fov_td * ratio;
	}
	else {
		fov_lr = global_fov;
		fov_td = fov_lr / ratio;
	}
	return {"lr":fov_lr,"td":fov_td};
}


function xyzTo2d(xyz,in_fov=true)
{
	var deg2rad = Math.PI / 180;
	var fov = getFOV();
	var fov_td = fov.td * deg2rad / 2;
	var fov_lr = fov.lr * deg2rad / 2;
	var x=xyz.x; var y=xyz.y;  var z=xyz.z;

	if(z<=0)
		return null;
	if(global_camera_projection) {
		var lim_x = Math.sin(fov_lr);
		var lim_y = Math.sin(fov_td);
	}
	else {
		x = Math.asin(x);
		y = Math.asin(y)
		var lim_x = fov_lr;
		var lim_y = fov_td;

	}
	if(in_fov) {
		if(x < -lim_x || x > lim_x)
			return null;
		if(y < -lim_y || y > lim_y)
			return null;
	}
	return { x:(x + lim_x) / (lim_x*2), y: 1 - (y + lim_y) / (lim_y * 2) };
}
function projectToCamera(RAd,DEd,cameraRays,in_fov=true)
{
	var xyz = cameraBearing(RAd,DEd,cameraRays)
	return xyzTo2d(xyz,in_fov);
}

function plotStar(star,camRays,highlight)
{
	var pos = projectToCamera(star.RA,star.DE,camRays);
	if(!pos)
		return null;
	context.beginPath();	
	var size = star.t == 'S' ? 6.5 - star.AM : 6 ;
	if(size < 1)
		size = 1;
	var color;
	if(highlight >= 2) {
		color = highlight == 3 ? global_style.target : global_style.align;
		size = 10;
	}
	else {
		color = global_style.star;
	}
	if(star.t == 'S')
		context.fillStyle = color;
	else
		context.fillStyle = 'black';
	var pix_x = pos.x * canvas.width;
	var pix_y = pos.y * canvas.height;
	result = { x: pix_x, y:pix_y , index:-1};
	if(highlight == 0)
		return result;
	if(star.t != 'Ca') {
		context.strokeStyle = color;
		context.lineWidth = 1;
		if(star.t == 'Ga') {
			context.ellipse(pix_x,pix_y,size*1.5,size/1.5,Math.PI/4,0,2*Math.PI,false);
			context.fill();
			context.stroke();
			context.beginPath();	
			context.arc(pix_x,pix_y,size/3,0,2*Math.PI,false);
			context.fillStyle = color;
			context.fill();
			context.stroke();
		}
		else if(star.t == 'Gc') {
			context.lineWidth = 2;
			context.setLineDash([1,3])
			context.arc(pix_x,pix_y,size,2*Math.PI,false);
			context.stroke();
			context.beginPath();	
			context.setLineDash([])
			context.fillStyle = color;
			context.arc(pix_x,pix_y,size/3,0,2*Math.PI,false);
			context.fill();
			context.stroke();
		}
		else if(star.t == 'Oc') {
			context.lineWidth = 2;
			context.setLineDash([1,3])
			context.arc(pix_x,pix_y,size,2*Math.PI,false);
			context.stroke();
			context.beginPath();	
			context.setLineDash([1,3])
			context.arc(pix_x,pix_y,size/3,0,2*Math.PI,false);
			context.fill();
			context.stroke();
			context.setLineDash([])
		}
		else if(star.t == 'Ne') {
			context.lineWidth = 1;
			context.moveTo(pix_x - size,pix_y - size);
			var f = 4;
			context.bezierCurveTo(pix_x + f*size,pix_y - size,pix_x -f*size,pix_y + size,pix_x+size,pix_y + size)
			context.stroke();
			context.beginPath();
			context.fillStyle=color;
			context.arc(pix_x,pix_y,size/3,0,2*Math.PI,false);
			context.fill();
			context.stroke();
		}
		else {
			context.arc(pix_x,pix_y,size,0,2*Math.PI,false);
			context.fill();
			context.stroke();
		}
	}
	if(star.name) {
		if(star.t == 'Ca') {
			color = global_style.constelations;
		}
		context.strokeStyle = color;
		context.fillStyle = color;
		if(star.t == 'Ca') {
			context.font = "4mm Sans"
			context.textBaseline = 'middle';
			context.textAlign = 'center';
			context.fillText(star.name,pix_x,pix_y)
		}
		else {
			let text = star.name;
			if(highlight > 1) {
				context.font = "6mm Sans";
				if(star.AM != -1 && highlight == 3)
					text+=", m=" + star.AM.toFixed(1);
			}
			else {
				context.font = "3mm Sans";
			}
			context.textBaseline = 'bottom';
			context.textAlign = 'start';
			context.fillText(text,pix_x + size + 1,pix_y - size - 1)
		}
	}
	return result;
}

function plotLines(camRays)
{
	if(!global_show_obj.Ca)
		return;
	for(var i=0;i<constellation_lines.length;i++) {
		line = constellation_lines[i];
		var p1 = projectToCamera(line.r0,line.d0,camRays,false);
		var p2 = projectToCamera(line.r1,line.d1,camRays,false);
		if(!p1 || !p2)
			continue;
		context.beginPath();	
		context.strokeStyle = global_style.constelations;
		context.lineWidth = 1;
		context.moveTo(p1.x*canvas.width,p1.y*canvas.height);
		context.lineTo(p2.x*canvas.width,p2.y*canvas.height);
		context.stroke();
	}
}


function plotCross()
{
	context.strokeStyle = global_style.cross;
	context.fillStyle = global_style.cross;
	context.lineWidth = 3;
	var dirs = [[1,0],[0,1],[-1,0],[0,-1]];
	var length = 50;
	var offset =10;
	for(var i=0;i<dirs.length;i++) {
		context.moveTo(canvas.width/2 + offset*dirs[i][0],canvas.height/2 + offset*dirs[i][1]);
		context.lineTo(canvas.width/2 + length*dirs[i][0],canvas.height/2 + length*dirs[i][1]);
	}
	context.stroke();
}

function plotBearing(xyz)
{
	context.beginPath();
	context.strokeStyle = global_style.bearing;
	context.fillStyle = global_style.bearing;
	context.lineWidth = 5;
	context.arc(canvas.width/2,canvas.height/2,10,0,2*Math.PI,false);
	context.moveTo(canvas.width/2,canvas.height/2);
	var dx = xyz.x;
	var dy = -xyz.y;
	var r = 1 / Math.sqrt(dx*dx+dy*dy);
	dx = dx*r;
	dy = dy*r;
	var length = 100;
	var pos = xyzTo2d(xyz);
	if(pos) {
		var px = canvas.width * (pos.x - 0.5); 
		var py = canvas.height * (pos.y - 0.5);
		var dist = Math.sqrt(px*px + py*py);
		if(dist < length)
			length = dist;
	}
	context.lineTo(canvas.width/2 + dx * length,canvas.height/2 + dy * length);
	var updn = (dy > 0 ? 'Down' : 'Up' ) + ' ' + Math.abs(Math.atan2(-xyz.y,xyz.z) / Math.PI * 180).toFixed(1) + '\u00b0';
	var left = (dx > 0 ? 'Right' : 'Left' ) + ' ' + Math.abs(Math.atan2(xyz.x,xyz.z) / Math.PI * 180).toFixed(1) + '\u00b0';
	context.stroke();
	context.lineWidth = 0;
	context.font = "6mm Serif";
	context.strokeStyle = global_style.bearing;
	context.fillStyle = global_style.bearing;
	context.textBaseline = 'middle';
	context.textAlign = 'end';
	context.fillText(updn,canvas.width - 5,canvas.height / 2)
	context.textAlign = 'center';
	context.textBaseline = 'bottom';
	context.fillText(left,canvas.width/2,canvas.height - 5)
}			


function logObject(thestar)
{
	if(thestar.name == 'Sirius' || thestar.name == 'Mars' || thestar.name == 'Jupiter' || thestar.name == 'Rigel') {
		document.getElementById('object_log').style.display='inline';
		if(1) {
			let ray = rayFromPos(thestar.RA,thestar.DE);
			let alt = Math.asin(ray[2]) / Math.PI * 180
				let az  = Math.atan2(ray[0],ray[1]) / Math.PI * 180;
			if(az < 0)
				az += 360;
			formatLatLon(thestar.name+"_alt",alt,'+','-');
			formatLatLon(thestar.name+"_az",az,'+','-');
		}
		else{
			let alt = thestar.RA / 15;
			let az  = thestar.DE;
			formatLatLon(thestar.name+"_alt",alt,'','-');
			formatLatLon(thestar.name+"_az",az,'+','-');
		}
	}
}

function getSolarSystemObject(p)
{
	var body = astrolib.bodies.indexOf(p);
	var r2d = 180 / Math.PI;
	var d2r = Math.PI / 180;
	var rLat = gdata.lat * d2r;
	var rLon = gdata.lon * d2r;
	var jd = astrolib.convertDateToJulianDate(new Date());
	var RaDec = astrolib.getBodyRaDec(jd,body,rLat,rLon,false);
	var RA = RaDec[2];
	var DEC = RaDec[1];
	return { "RA" : RA * r2d, "DE": DEC *r2d, "name": p, "AM" : -1 };
}



function plotStars()
{
	var start=Date.now();
	
	if(canvas.width != document.body.clientWidth || canvas.height != document.body.clientHeight) {
		canvas.width = document.body.clientWidth;
		canvas.height = document.body.clientHeight;
	}
	
	global_targets_list=[];
	gdata.time = Date.now();
	var camRays = getCameraRays();
	context.fillStyle = "black";
	context.fillRect(0, 0, canvas.width, canvas.height);
	context.fillStyle = global_style.star;

	for(var i=0;i<allstars.length;i++) {
		var st = allstars[i].t;
		
		if(st == 'P') {
		    let pos = getSolarSystemObject(allstars[i].name);
		    allstars[i].RA = pos.RA;
		    allstars[i].DE = pos.DE;
		}
		
		//logObject(allstars[i]);
		
		var mag = allstars[i].AM;
		if((st == 'S' && mag > global_mag) || (st != 'S' && mag > global_dso_mag) || !global_show_obj[st])
		{
			i=allstars_index[st] - 1;
			continue
		}
		var highlight = 1;
		if(i == global_target_index || i == global_align_index)
			highlight = 0;
		var  pos = plotStar(allstars[i],camRays,highlight);
		// select only stars if not aligned
		// if aligned select all but constellations
		if(pos && st!='Ca' && (st == 'S' || global_use_gyro)) {
			pos.index = i;
			global_targets_list.push(pos);
		}
	}
	if(global_align_index >= 0 && global_align_index != global_target_index) {
		plotStar(allstars[global_align_index],camRays,2);
	}
	if(global_target_index >= 0) {
		var star = allstars[global_target_index];
		var xyz = cameraBearing(star.RA,star.DE,camRays);
		plotBearing(xyz);
		plotStar(star,camRays,3);
	}
	else if(global_use_gyro) {
		plotCross();
	}
	plotLines(camRays);
	plotAltAz(camRays[2]);
	var passed = Date.now() - start;
	if(passed > global_expected_frame_rate_ms / 2) {
		setTimeout(plotStars,global_expected_frame_rate_ms);
	}
	else {
		setTimeout(plotStars,global_expected_frame_rate_ms-passed);
	}
}


function plotAltAz(fwd)
{
	var alt = Math.asin(fwd[2]) / Math.PI * 180;
	var az  = Math.atan2(fwd[0],fwd[1]) / Math.PI * 180;
	alt = 'Alt:' + alt.toFixed(1);
	if(az < 0)
		az = 360 + az;
	az  = 'Az:' + az.toFixed(1);
	context.font = "5mm Sans"
	context.textBaseline = 'bottom';
	context.textAlign = 'end';
	context.fillStyle = global_style.altaz;
	context.fillText(alt,canvas.width - 5,canvas.height - 5)
	context.textAlign = 'start';
	context.fillText(az,5,canvas.height - 5)
}

function selectTaret(index)
{
	findTargetByName();
	global_target_index = index;
	//global_expecting_select = null;
}

function selectionEvent(e)
{
	let x = e.clientX;
	let y = e.clientY;
	let min_dist = 1e100;
	let min_index = -1;
	for(var i=0;i<global_targets_list.length;i++) {
		let dx = global_targets_list[i].x - x;
		let dy = global_targets_list[i].y - y;
		let dist = dx*dx + dy*dy;
		if(min_dist > dist) {
			min_dist = dist;
			min_index = global_targets_list[i].index;
		}
	}
	if(global_expecting_select) {
		global_expecting_select(min_index);
	}
}

function formatLatLon(id,deg,pos,neg)
{
	var direction = deg >= 0 ? pos : neg;
	deg = Math.abs(deg);
	var ideg = Math.floor(deg);
	var min = 60*(deg - ideg);
	var imin = Math.floor(min);
	var sec = 60*(min - imin);
	var msg = direction + ideg + "\u00b0" + imin + "'" + sec.toFixed(1) + "''";
	document.getElementById(id).innerHTML = msg;
}

function showpos(position)
{
	var latlon = position.coords.latitude + "," + position.coords.longitude;
	gdata.lat = position.coords.latitude;
	gdata.lon = position.coords.longitude;
	formatLatLon("lat",gdata.lat,'N','S');
	formatLatLon("lon",gdata.lon,'E','W');
	document.getElementById("gps").style.display='none';
}

function requestGeolocation()
{
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showpos);
  }
}

function getLocation() {
  requestGeolocation();
  setTimeout(getLocation,600*1000)
}

function gyroListener(event)
{
	if(!(event.alpha === null)) {
		gdata.alpha_gyro = event.alpha;
		gdata.beta = event.beta;
		gdata.gamma = event.gamma;
		document.getElementById("orient").innerHTML = '';
	}
	else {
		document.getElementById("orient").innerHTML = 'No Gyro';
	}
	formatValue("ang_a",event.alpha);
	formatValue("ang_b",event.beta);
	formatValue("ang_g",event.gamma);
}

function deviceOrientationListenerIOS(event) {
	if(!(event.webkitCompassHeading === null)) {
		if(global_use_compass)
			gdata.alpha = event.webkitCompassHeading;
		gdata.compass_alpha = event.webkitCompassHeading;
	}
	else {
		noCompass();
	}
	formatValue("ang_c",event.webkitCompassHeading);
}

function deviceOrientationListener(event) {
	if(!(event.alpha === null)) {
		if(global_use_compass)
			gdata.alpha = event.alpha;
		gdata.compass_alpha = event.alpha;
	}
	else {
		noCompass();
	}
	formatValue("ang_c",event.alpha);
}


function noCompass()
{
	global_use_compass = false;
	document.getElementById("nocompass_button").style.display="inline";
	document.getElementById("compass_button").style.display="none";
	document.getElementById("hand_button").style.display="none";
}

function manualMode()
{
	global_use_compass = false;
	gdata.alpha_user_offset = gdata.alpha;
	gdata.alpha = 0;
	document.getElementById("compass_button").style.display="inline";
	document.getElementById("hand_button").style.display="none";
}

function compassMode()
{
	global_use_compass = true;
	gdata.alpha_user_offset = 0;
	gdata.alpha = gdata.compass_alpha;
	document.getElementById("compass_button").style.display="none";
	document.getElementById("hand_button").style.display="inline";
}

function manualDown(e)
{
	global_prev_xy = {"x":e.touches[0].clientX,"y":e.touches[0].clientY };
}

function manualMove(e)
{
	if(!global_prev_xy)
		return;
	
	var xy = {"x":e.touches[0].clientX,"y":e.touches[0].clientY };
	moveSky(global_prev_xy,xy);
	global_prev_xy = xy;
}
function manualUp(e)
{
	if(!global_prev_xy)
		return;
	var xy = {"x":e.touches[0].clientX,"y":e.touches[0].clientY };
	moveSky(global_prev_xy,xy);
	global_prev_xy = null;
}
function moveSky(prev,cur)
{
	if(global_use_compass)
		return;
	if(!prev || !cur)
		return;
	var fov =  getFOV().lr;
	var da = (cur.x - prev.x) / canvas.width * fov;;
	gdata.alpha_user_offset += da;
}

function dontPropMouseDown(lst)
{
	for(var i=0;i<lst.length;i++) {
		var elements = document.getElementsByClassName(lst[i]);
		for(var j=0;j<elements.length;j++) {
			elements[j].addEventListener('mousedown',function(e) {
				e.stopPropagation();
			});
		}
	}
}



function setupiOSOrientationEvents()
{
	if (window.DeviceOrientationEvent) {
		if(('ondeviceorientation' in window)) {
			window.addEventListener("deviceorientation", deviceOrientationListenerIOS);
			window.addEventListener("deviceorientation",gyroListener);
			compassMode();
		}
		else {
			unsupported();
		}
	} else {
		unsupported();
	}
	setUseGyro(false);
}


function setupOrientationEvents()
{
	if (window.DeviceOrientationEvent) {
		if(('ondeviceorientationabsolute' in window)) {
			window.addEventListener("deviceorientationabsolute", deviceOrientationListener);
			window.addEventListener("deviceorientation",gyroListener);
			compassMode();
		}
		else if(('ondeviceorientation' in window)) {
			window.addEventListener("deviceorientation",gyroListener);
			noCompass();
		}
		else {
			unsupported();
		}
	} else {
		unsupported();
	}
	setUseGyro(false);
}

function formatValue(uid,v)
{
	var msg='';
	if(v === undefined || v==null) {
		msg = 'No';
	}
	else {
		msg = v.toFixed(1);
	}
	document.getElementById(uid).innerHTML=msg;
}


function iOSOrientation()
{
	//Notification.requestPermission().then(response => {
	DeviceOrientationEvent.requestPermission().then(response => {
		if (response == 'granted') {
			document.getElementById("allow_orientation").style.display='none';
			setupiOSOrientationEvents();
		}
	})
	.catch(console.error)
}

function setupGyros()
{
	//if (typeof window.Notification.requestPermission === 'function') {
	if (typeof window.DeviceOrientationEvent.requestPermission === 'function') {
		document.getElementById("allow_orientation").style.display='inline';
	}
	else {
		setupOrientationEvents();
	}
}

function switchNightMode(is_night)
{
	global_style = is_night ? global_night_style : global_day_style;
}


function setDSOMag(val)
{
	global_dso_mag = parseInt(val);
	document.getElementById('dso_level_val').innerHTML = '' + global_dso_mag;
}

setupGyros();
// global drawing stuff
var canvas = document.getElementById('myCanvas');
canvas.width = document.body.clientWidth;
canvas.height = document.body.clientHeight;
var context = canvas.getContext('2d');
setTimeout(getLocation,500)
setTimeout(plotStars,1000)
document.body.addEventListener('mousedown',selectionEvent);
document.body.addEventListener('touchstart',manualDown);
document.body.addEventListener('touchend',manualUp);
document.body.addEventListener('touchcancel',manualUp);
document.body.addEventListener('touchmove',manualMove);
dontPropMouseDown(["ui_but","incdec_but","config_div","comp_but"]);
</script>


</body>
</html>
"""

cert_path = tempfile.gettempdir()+ '/cert.pem'

print("Saving sertificate to temporary ",cert_path)

try:
    hopper = hopper.encode('utf-8')
    with open(cert_path,"w") as f:
        f.write(pem)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_path)
finally:
    os.remove(cert_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            try:
                conn, addr = ssock.accept()
                inp = conn.read().decode()
                if inp[:6]=='GET / ':
                    conn.write(b'HTTP/1.0 200 Ok\r\n'
                               b'Connection: close\r\n'
                               b'Content-Type: text/html\r\n'
                               b'Content-Length: %d\r\n'
                               b'\r\n%s' % (len(hopper),hopper))
                    print("Served one SkyHopper page")
                else:
                    conn.write(b'HTTP/1.0 404 Not Found\r\n'
                               b'Connection: close\r\n'
                               b'Content-Length: 0\r\n'
                               b'\r\n')
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
            except KeyboardInterrupt:
                print("Done")
                break
            except:
                pass

