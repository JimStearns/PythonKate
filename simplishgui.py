""" A quick and dirty effort to approximate the simple graphics functionality that package simplegui provides
    for CodeSculptor. Provides a simple-ish wrapper around "Tkinter", the most common graphics UI package for Python.
"""

import Tkinter as tk
# "Q: What is the advantage of defining Tkinter as tk?"
#
# A: "By using the more verbose import Tkinter as tk, you clarify exactly where every object is coming from.
# That helps when debugging or reading other people's code, and it prevents name collisions
# when two modules use the same names"
# (http://stackoverflow.com/questions/14838635/quit-mainloop-in-python)
#
# Q2: But wouldn't "Tkinter as Tk" (start with a cap) be more consistent?
# A2 (me, from reading PEP8 Python naming conventions)
#   Python module names should be all lower-case. Tkinter is a module, so by starting with a cap it
#   violates the convention. "as tk" restores the convention.

class SimplishTimer(object):
    """ Provide a simplegui-like timer, as in:
        simplegui.create_timer(TIMER_INTERVAL_MS, timer_handler)
    """

    def __init__(self, root_window, timer_interval_ms, method_to_call):
        self.root_window = root_window  # Need in order to be able to call after() method.
        self.interval_ms = timer_interval_ms
        self.timer_handler_method = method_to_call
        print("User timer handler set to {0}".format(self.timer_handler_method))
        self.running = False

    def start(self):
        print("Started Timer for method {0}".format(self.timer_handler_method))
        self.running = True
        self._internal_timer_handler()

    def stop(self):
        self.running = False

    def _internal_timer_handler(self):
        if self.running:
            #print("Running timer handler called, user method is {0}".format(self.timer_handler_method))
            self.timer_handler_method()
            self.root_window.after(self.interval_ms, self._internal_timer_handler)

class SimplishFrame(tk.Frame):

    ##
    # Nested classes - classes only instantiated by SimplishFrame
    ##
    class SimplishCanvas(tk.Canvas):
        """A wrapper around Tkinter's Canvas to provide the draw_line, draw_circle methods of simplegui.
            SimplishCanvas.draw_line() --> Canvas.create_line()
            SimplishCanvas.draw_circle() --> Canvas.create_oval()
            SimplishCanvas.draw_text() --> Canvas.create_text()
        """

        def __init__(self, width, height, background="lightgray"):
            tk.Canvas.__init__(self, width=width, height=height, background=background)

        def draw_line(self, xyStart, xyEnd, lineWidth, lineColor):
            """
            Support calls like this: "canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2, "White")"
            """
            # For readability
            X = 0
            Y = 1
            self.create_line(xyStart[X], xyStart[Y], xyEnd[X], xyEnd[Y], width=lineWidth, fill=lineColor)

        def draw_circle(self, xyCenter, radius, borderWidth, borderColor, fillColor):
            """
            :param xyCenter:
            :param radius:
            :param borderWidth:
            :param borderColor:
            :param fillColor:
            :return: none
            """
            # For readability
            X = 0
            Y = 1
            # Tkinter uses oval to draw a circle (special case of oval)
            # and specifies the oval with upper-left and lower-right points.
            # Use center +/- radius to define these.
            # TODO: Could be off-by-one because oval will coincide with upper left of
            # box defined by (x0, y0), (x1, y1) but is just inside the on the lower right.
            x0 = xyCenter[X] - radius
            x1 = xyCenter[X] + radius
            y0 = xyCenter[Y] - radius
            y1 = xyCenter[Y] + radius
            #print("Circle center=({0}), R={1}".format(xyCenter, radius))
            #print("Drawing a circle in box ({0},{1}), ({2},{3}), border width/color={4}/{5}, fill={6}".format(
            #    x0, y0, x1, y1, borderWidth, borderColor, fillColor))
            self.create_oval(x0, y0, x1, y1, width=borderWidth, outline=borderColor, fill=fillColor)

        def draw_text(self, textString, xyLowerLeft, fontSize, fontColor):
            """
            Found definition of second and third parameters at
                http://www.codeskulptor.org/#examples-more-3a_canvas_and_drawing-structure.py
            Found discussion of Tkinter font (and how font size is specified) at:
                http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/fonts.html
            """
            # For readability
            X = 0
            Y = 1
            # TODO: Determine simplegui's default font. I chose Helvetica, just for grins
            self.create_text(xyLowerLeft[X], xyLowerLeft[Y], text=textString, anchor=tk.SW,
                             font=('Helvetica', fontSize), fill=fontColor)

    ##
    # Constructor
    ##
    def __init__(self, parent_window, frame_width, frame_height, background="lightgray"):
        self.parent_window = parent_window
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.background = background
        tk.Frame.__init__(self, parent_window, width=frame_width, height=frame_height)
        self.draw_handler_method = None
        self.keyup_handler_method = None
        self.keydown_handler_method = None

        # If set_draw_handler called, it will set up a timer. This is where it will be maintained.
        self.draw_handler_timer = None

    ##
    # Event handler setups
    ##
    def set_draw_handler(self, method_to_call):
        self.draw_handler_method = method_to_call

    def set_keydown_handler(self, method_to_call):
        self.keydown_handler_method = method_to_call

    def set_keyup_handler(self, method_to_call):
        self.keyup_handler_method = method_to_call


    ##
    # Draw handler machinery. Unlike key and other events, a timer must be set up for the draw handler
    #   so that the user's drawing method is called about 60 times per second.
    ##
    def _start_draw_handler(self):
        # Do nothing if set_draw_handler() not called.
        if not self.draw_handler_method:
            return

        self.draw_handler_canvas = SimplishFrame.SimplishCanvas(
            width=self.frame_width, height=self.frame_height, background=self.background)
        interval60fps = 1000 / 60   # Re-draw 60 times per second
        self.draw_handler_timer = SimplishTimer(self.parent_window, interval60fps, self._internal_draw_handler_method)
        self.draw_handler_timer.start()

    def _stop_draw_handler(self):
        if self.draw_handler_timer:
            self.draw_handler_timer.stop()

    def _internal_draw_handler_method(self):
        if not self.draw_handler_canvas:
            return

        # Clear the canvas
        self.draw_handler_canvas.delete(tk.ALL)

        # Call the draw method specified by the user of this library:
        self.draw_handler_method(self.draw_handler_canvas)

        # Tkinter's pack() lays out the widgets and makes them visible.
        self.draw_handler_canvas.pack()

    ##
    # Mainloop - starts up the UI and handles events
    ##
    def mainloop(self, n=0):
        """Start the GUI.

            Parameter "n=0" added because that's in the signature for mainloop in Frame.

            Note: this method doesn't return - stays in mainloop() until frame exited.
        """
        # - SimplishFrame inherits from tk.Frame.
        # - tk.Frame defines a mainloop() method.
        # - We want to call tk.Frame's implementation of mainloop.
        # - But first we want to start up the timer to call the
        self._start_draw_handler()

        # Having accomplished the purpose of overriding the superclass's implementation of this method,
        # now call Frame's mainloop.
        tk.Frame.mainloop(self)

class SimplishGui():
    ''' Web references
        SimpleGui's draw handler: http://stackoverflow.com/questions/20308086/draw-handler-for-python
        Canvas drawing in Tkinter: http://zetcode.com/gui/tkinter/drawing/
        Event handling (like keypresses): http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        Timer: http://stackoverflow.com/questions/2400262/code-a-timer-in-a-python-gui-in-tkinter

        Should allow setup like:
        # create frame
        frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
        frame.set_draw_handler(draw)
        frame.set_keydown_handler(keydown)
        frame.set_keyup_handler(keyup)

        # Create the timer to handle changes in ball position and velocity.
        timer = simplegui.create_timer(TIMER_INTERVAL_MS, timer_handler)

        # start frame
        #new_game()
        timer.start()
        frame.start()


        # Changes from simplegui
        1.  Instantiate the GUI
            pongGui = SimplishGui()

    '''

    def __init__(self, application_name="SimplishGui"):
        self.root_window = tk.Tk(className=application_name)

    def create_frame(self, title, frame_width, frame_height, background="lightgray"):
        self.root_window.title(title)
        self.root_window.geometry("{0}x{1}".format(frame_width, frame_height))
        frame = SimplishFrame(self.root_window, frame_width, frame_height, background=background)
        return frame

    def create_timer(self, timer_interval_ms, method_to_call):
        return SimplishTimer(self.root_window, timer_interval_ms, method_to_call)
