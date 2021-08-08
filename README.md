# Blender Timelapse Addon
Allows you to easily record a timelapse of your blender project without the need for external software. 

* Start and stop recording timelapses right in Blender
* Automatically resume timelapse sessions if needed
* One-click to create the timelapse clip in Blender's Video Editor


# How to use
The UI is located in the Properties -> Output -> Timelapse panel

The addon creates an image sequence for the timelapse, so they must be stored somewhere. Make sure you don't run out of space.
___
* Choose the output directory 
	* _The addon defaults to a directory called "screenshots" at where your .blend is located, it will create one if it doesn't exist_
* Specify the name of the output files and format
* Specify the period at which a frame in the timelapse is created
* Click **Start Timelapse**
___
Once a timelapse has been created, you can either import the image sequence into a software of your choice, or you can have the addon to create a clip for you inside Blender's Video Editor. 

To do so, simply click **Create Timelapse Clip**

# Limitations
Because the addon uses Blender's built in screenshot function, it will not capture anything other than the Blender window in which you've started the timelapse from. Therefore, it will not capture any other applications, nor will it capture any additional windows of Blender. 
