
import numpy as np
import time

import moderngl
import glfw

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  

class PygameRenderer():
    # pygame.display.set_icon(pygame.image.load('phanim/icon.png'))
    def __init__(self,resolution,fontSize,fullscreen):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Phanim")


        infoObject = pygame.display.Info()
        if resolution == None:
            self.resolution = (infoObject.current_w, infoObject.current_h)
        else:
            self.resolution = resolution
        self.surface = pygame.Surface(self.resolution,pygame.SRCALPHA)
        self.font = pygame.font.SysFont(None,1)
        if fullscreen:
            self.display = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.resolution,flags=pygame.SCALED,vsync=1)
        self.clock = pygame.time.Clock()
        self.isRunning = True
        
        
    def drawLine(self,color,start,stop,pixelWidth):
        pygame.draw.line(
            self.surface,
            color,
            start,
            stop,
            width=int(pixelWidth)
        )
    def running(self):
        return self.isRunning
    
    def drawCircle(self,color,center,radius,segments=1):
        pygame.draw.circle(self.surface,color,center,radius)

    def drawCursor(self):
        color,center,radius = self.cursor
        circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(circle, color, (radius, radius), radius)
        self.display.blit(circle,[center[0]-radius,center[1]-radius])
        
    def setCursor(self,color,center,radius):
        self.cursor = color,center,radius

    def drawPolygon(self,color,points):
        pygame.draw.polygon(self.surface, color, points)

    def reset(self,color):
        self.display.fill(color)
        self.surface.fill((0,0,0,0))
    
    def blit(self):
        self.display.blit(self.surface,(0,0))

    def getMousePos(self):
        return pygame.mouse.get_pos()

    def update(self,backgroundColor):
        self.blit()
        self.setCursor((100,100,100),self.getMousePos(),10)
        self.drawCursor()
        pygame.display.update()
        self.reset(backgroundColor)

    def getFrameDeltaTime(self):
        return self.clock.tick(60) / 1000

    def quit(self):
        pygame.quit()




class ModernGLRenderer:
    def __init__(self, resolution,fontsize, fullscreen):

        if not glfw.init():
            raise Exception("GLFW can't be initialized")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)

        self.resolution = resolution
        self.last_frame_time = time.time()
        # Get the primary monitor
        primary_monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(primary_monitor)

        if resolution == None:
            self.resolution = (video_mode.size.width, video_mode.size.height)
            print(self.resolution)


        if fullscreen:
            # Use the video mode's resolution for fullscreen
            self.resolution = (video_mode.size.width, video_mode.size.height)
            self.window = glfw.create_window(self.resolution[0], self.resolution[1], "ModernGL Renderer", primary_monitor, None)
        else:
            self.window = glfw.create_window(self.resolution[0], self.resolution[1], "ModernGL Renderer", None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created")

        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context()

        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            out vec4 f_color;
            uniform vec3 color;
            void main() {
                f_color = vec4(color, 1.0);
            }
            """
        )
        self.BUTTONDOWN = False
        self.BUTTONUP = False
        self.scroll = [0,0]
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

        self.aspect_ratio = self.resolution[0] / self.resolution[1]
        self.shapes_to_draw = []

    def convert_pixel_to_screen_coordinates(self,coordinate):
        return  [
            coordinate[0] / self.resolution[0] * 2 - 1,
            1 - coordinate[1] / self.resolution[1] * 2,
        ]


    def drawLine(self, color, start, end,width):

        color = color[0]/255, color[1]/255, color[2]/255
        start = self.convert_pixel_to_screen_coordinates(start)
        end = self.convert_pixel_to_screen_coordinates(end)

        # Calculate the direction of the line
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        len = np.sqrt(dx*dx + dy*dy)

        if len > 0:
            perp_dx = -dy / len
            perp_dy = dx / len
        else:
            return

        # Adjust the perpendicular vector components for aspect ratio
        perp_dy *= self.aspect_ratio

        # Calculate the vertices of the rectangle (thin quad) representing the line
        half_width = width / self.resolution[1] / 2  # Convert pixel width to NDC
        vertices = [
            start[0] + perp_dx * half_width, start[1] + perp_dy * half_width,
            end[0] + perp_dx * half_width, end[1] + perp_dy * half_width,
            end[0] - perp_dx * half_width, end[1] - perp_dy * half_width,
            start[0] - perp_dx * half_width, start[1] - perp_dy * half_width
        ]

        # Create buffer and vertex array as before
        vertices = np.array(vertices, dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert')

        # Store the vao, color, and render mode (TRIANGLE_FAN for the rectangle)
        self.shapes_to_draw.append((vao, tuple(color), moderngl.TRIANGLE_FAN))

    def getFrameDeltaTime(self):
        return self.delta_time

    def drawPolygon(self, color, vertices):
        color = color[0]/255, color[1]/255, color[2]/255
        # Assume vertices is a list of (x, y) tuples
        flat_vertices = [coord for vertex in vertices for coord in self.convert_pixel_to_screen_coordinates(vertex)]
        vertices = np.array(flat_vertices, dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert')
        self.shapes_to_draw.append((vao, tuple(color), moderngl.TRIANGLE_FAN))

    def drawCircle(self, color, center, radius, segments=100):
        color = color[0]/255, color[1]/255, color[2]/255
        center = self.convert_pixel_to_screen_coordinates(center)
        correctRadius = radius/self.resolution[0]*2
        angle_step = 2 * np.pi / segments
        vertices = []

        for i in range(segments):
            angle = i * angle_step
            x = center[0] + correctRadius * np.cos(angle)
            y = center[1] + correctRadius * np.sin(angle) * self.aspect_ratio
            vertices.extend([x, y])

        vertices = np.array(vertices, dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert')
        self.shapes_to_draw.append((vao, tuple(color), moderngl.TRIANGLE_FAN))

    def getMousePos(self):
        return glfw.get_cursor_pos(self.window)

    def mouse_button_callback(self, window, button, action, mods):
        self.BUTTONDOWN = False
        self.BUTTONUP = False
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.BUTTONDOWN = True
            elif action == glfw.RELEASE:
                self.BUTTONUP = True

    def scroll_callback(self, window, xoffset, yoffset):
        self.scroll = [xoffset,yoffset]

    def quit(self):
        glfw.terminate()

    def running(self):
        return not glfw.window_should_close(self.window)

    def update(self,color):
        color = color[0]/255, color[1]/255, color[2]/255
        # Calculate the time spent on the last frame
        self.delta_time = time.time() - self.last_frame_time

        # Update last_frame_time to the current time
        self.last_frame_time = time.time()

        # Rendering operations
        self.ctx.clear(*color, 1.0)
        for vao, color, mode in self.shapes_to_draw:
            self.prog['color'].value = color
            vao.render(mode)

        # Swap buffers
        glfw.swap_buffers(self.window)

        # Handle events
        glfw.poll_events()

        self.shapes_to_draw = []


if __name__ == "__main__":
    renderer = ModernGLRenderer((1920, 1080),0, fullscreen=True)

    while not glfw.window_should_close(renderer.window):
        for i in range(1000):
            renderer.drawLine(
                (np.random.random()*255,np.random.random()*255,np.random.random()*255),
                [np.random.random()*renderer.resolution[0],np.random.random()*renderer.resolution[1]],
                [np.random.random()*renderer.resolution[0],np.random.random()*renderer.resolution[1]],
                0.1,
            )
        renderer.update((0,0,0))



