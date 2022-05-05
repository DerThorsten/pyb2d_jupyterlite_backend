import asyncio
from ipyevents import Event as IPyEvent


class Event(object):
    def get_future(self):
        raise NotImplemented()

    def _set_future_result(self):
        if not self._future.done():
            self._future.set_result(self)


class MouseDownEvent(Event):
    def __init__(self, widget, callback):
        super(MouseDownEvent, self).__init__()
        self._widget = widget
        self._callback = callback
        self._future = None
        self._widget.on_mouse_down(self.on_mouse_down)

    def on_mouse_down(self, x, y):
        self._callback(x, y)
        self._set_future_result()

    def get_future(self):
        self._future = asyncio.Future()
        return self._future


class MouseMoveEvent(Event):
    def __init__(self, widget, callback):
        super(MouseMoveEvent, self).__init__()
        self._widget = widget
        self._callback = callback
        self._widget.on_mouse_move(self.on_mouse_move)

    def on_mouse_move(self, x, y):
        self._callback(x, y)
        self._set_future_result()

    def get_future(self):
        self._future = asyncio.Future()
        return self._future


class MouseUpEvent(Event):
    def __init__(self, widget, callback):
        super(MouseUpEvent, self).__init__()
        self._widget = widget
        self._callback = callback
        self._widget.on_mouse_up(self.on_mouse_up)

    def on_mouse_up(self, x, y):
        self._callback(x, y)
        self._set_future_result()

    def get_future(self):
        self._future = asyncio.Future()
        return self._future


class DomEvent(Event):
    def __init__(self, widget, callback):
        super(DomEvent, self).__init__()

        self._widget = widget
        self._callback = callback

        self._d = IPyEvent(
            source=self._widget, watched_events=["keydown", "keyup", "wheel"]
        )
        self._d.on_dom_event(self.on_event)

    def on_event(self, event):
        self._callback(event)
        self._set_future_result()

    def get_future(self):
        self._future = asyncio.Future()

        return self._future


# d = IPyEvent(
#          source=self.multi_canvas, watched_events=["keydown", "keyup", "wheel"]
#      )

#      def handle_event(event):

#          scale = self.debug_draw.scale
#          etype = event["event"]
#          if etype == "wheel":
#              if event["deltaY"] > 0:
#                  self.debug_draw.scale = scale * 0.9
#              elif event["deltaY"] < 0:
#                  self.debug_draw.scale = scale * 1.1
#              # self.event_info.value = f"WHEEEL {event['deltaY']}"
#          elif etype == "keyup":
#              k = event["key"]
#              self.testbed.on_keyboard_up(k)
#          elif etype == "keydown":
#              k = event["key"]
#              self.testbed.on_keyboard_down(k)

#      d.on_dom_event(handle_event)
