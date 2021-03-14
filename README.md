# SkyHopper

[SkyHopper](https://artyom-beilis.github.io/skyhopper.html) is a web application that helps
to find objects across the night sky by hopping from a well know and easily identifiable 
stars to other fainer stars or DSO by measuring changes in angles of the cell phone
using built in gyroscope and gravity sensors. It is similar to Digital Setting Circles 
implemented in a smart phone.

The smart phone has to have gyro, gravity sensors and preferably compass.

It is a web based application that contains a single HTML page and JavaScript objects 
database that will continue to work even offline as long as it is cached by browser.

## Operation

You attach the cellphone onto the telescope such that the physical **top** part of the phone 
points towards viewing direction. Note it is different from typical sky observing apps
that simulate camera view of the sky. For this application the screen is parallel to the
viewing direction.

1. You align your telescope with ab easily identifiable star near the object you want to observe
2. You press `Align` button on the application
3. You press on the star you selected - now the application is aligned. "Aligned" message is shown and a cross that represents the direction your telescope is looking to is shown in the center of the screen.
4. You press on an object you want to observe and you get a line showing a direction you need to move the telescope and the changes in altitude and azimuth are shown at the right and bottom part of the screen
5. You move the telescope till these numbers are close to zero - at this point your telescope should point to the requested object
6. In order to move to next object - repeat the alignment process from the step 1 since the builtin cellphone gyros don't keep the accuracy for a long time/multiple movements

## Troubleshooting 

-   _I move the application but nothing moves?_

    Make sure your cellphone has working sensors. Does SkyMap like applications work for you?

-   _I move the application but only Altitude is modifing Azimuth is poining to Polaris/North?_

    Your browser may not support compass heading (for example Firefox) or you don't have such a sensor in the phone.
    You can adjust azimuth manually by swipping the screen till you get required azimuth and then align.

-   _I pointed my telescope to the star but the cell phone seems to point to a different direction?_

    The compass of the cell phone may be significantly misaligned you may to do following:

    1. Move your cell phone in compass calibration/waving pattern to increase compass accuracy
    2. Increase application's field of view by pressing `+` at the top left corner new `∠60°` default FOV.
    3. You may switch to manual azimuth mode by pressing "hand" icon at the left side and adjust the azimuth manually

-   _The screen becomes dim very fast and I don't have time to align/point the telescope?_

    Modify the "sleeping" settings for the cell phone. It is under "Settings -> Display" in Android

-   _I start moving the telescope to modify azimuth direction but according to the application it stopped moving, or going back - behaves strangly?_

    It seems that gyro lost accuracy. It happens. Try again. If it still happens all the time and you can't reach the target. Try one of following:

    1. Select a start that is closer on its azimuth to target object - altitude has much more accurate tracking.
    2. Correct altitude first and than search for the object on azimuth axis 

## Controls

- Left side, from top to bottom:

    - Field of view modify with `+`, `-` to adjust 
    - Maximal star magnitude to display/align on - adjust with `+`, `-` controls
    - Align button and status - pressing on it starts alignment process - you need to select a star you aligning on to.

- Right side, from top to bottom

    - `N` or `D` button switch to night/day mode. `↻` button - reset alignment
    - `✥` - switch to full screen mode
    - "pointing hand" - switch to manual mode,  "compass" switch to compass mode, "compass crossed with line" - no compass available use manual mode only

## Notes

It is experimental open source web application that would work only with well working sensors. No guarantee so. It is released under GPL license.

