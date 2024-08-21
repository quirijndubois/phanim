Phanim also has built in recording functionality. Keep in mind that this will impact real-time performance significantly. Luckily recordings are independent from the real time frame rate. This is the same for simulations that use screen.dt. Recordings can be turned on by passing an argument to the Screen:

```python
s = Screen(record=True)
...
s.run()
```
or if you want more options:
```python
s = Screen(record=True,recording_output="recording.mp4",recording_fps=30)
...
s.run()
```