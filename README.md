# Thermal
Thermal is bringing back the thermal printer! A python program that runs 24/7 on a raspberry pi 4 which can interact with a thermal printer (https://www.adafruit.com/product/2751). 

# Important Notes
The code above is not complete, there is no guarantee that the code downloaded from above is in a working state. A programming knowledge will be needed to fill in the redacted code for security reasons including API keys and personal data. Most gaps should be filled with information provided in the tutorial series.

# To Come
The full source code ready to be downloaded with an instruction guide on wiring the physical components together and the software installation steps to get your own thermal up and running. A small series of tutorials that will help document the process of using python with the Adafruit collection of thermal printers. 

# Potential feature list
  - Web server using flask for phone interaction
  - Time events to trigger on specific days and at random intervals
  - Events:
      - Sudoku Generation
      - Jokes
      - Riddles
  - Plant watering reminder
  - FitBit Web API integration:
      - Morning message to include sleep information from night before
      - Fitness brief printable by request of the user
 
 # Android Companion Application
  An android app which can be downloaded to connect to the raspberry pi. 
    Features:
      - Trigger events manually
      - Change settings for thermal

# Todo List:
  - Convert to multi threading application to use Buttons/Flask/Timing events
  - Change to command structure to stack to properly execute commands in order from many different threads
  - Inlcude status api call to update android app on status of printing

# Thread Structure:
  1. Main Thread: The status of the application and the stack of commands
  2. Printing Thread: Handles all printing functions, allows for printing to continue un-disturberd 
  3. API Thread: The flask application which allows the android application to communicate with the thermal printer
  4. Button Thread: Handles physical button activity from the printer. 

  All threads will add commands to the stack on the main thread, the main thread will process the stack one by one on a FIFO basis updating the status to notify certain triggers. 

  (need to figure a way to communicate between the threads, perhaps another thread is needed to share the varaibles between the threads)