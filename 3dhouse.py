import glfw
from OpenGL.GL import *
from pyrr import matrix44, Vector3
from ObjLoader import *
import textureloader
import ShaderLoader
from Camera import Camera


def window_resize(window, width, height):
    glViewport(0, 0, width, height) #The first two parameters of glViewport set the location of the lower left corner of the window.
                                    #The third and fourth parameter set the width and height of the rendering window in pixels, which we have set equal to GLFW's window size.

cam = Camera()
keys = [False] * 1024




def key_callback(window, key, scancode, action, mode): #call back function
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False


def do_movement():
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.5)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.5)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.5)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.5)


def main():
    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1920, 1080
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "3D HOUSE", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    

    obj = ObjLoader()
    obj.load_model("resources/houseobj.obj")
    obj_shader = ShaderLoader.compile_shader("shaders/video_09_vert.vs", "shaders/video_09_monster.fs")
    obj_tex = textureloader.load_texture("resources/Lightmap.jpg")
    obj_texture_offset = len(obj.vertex_index) * 12

    obj_vao = glGenVertexArrays(1)
    glBindVertexArray(obj_vao)
    obj_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, obj_vbo)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)
    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(obj_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(90.0, aspect_ratio, 1.0, 100.0)
    obj_model = matrix44.create_from_translation(Vector3([0.0, 0.0, -5.0]))

    
   
    glUseProgram(obj_shader)
    obj_model_loc = glGetUniformLocation(obj_shader, "model")
    obj_view_loc = glGetUniformLocation(obj_shader, "view")
    obj_proj_loc = glGetUniformLocation(obj_shader, "proj")
    glUniformMatrix4fv(obj_model_loc, 1, GL_FALSE, obj_model)
    glUniformMatrix4fv(obj_proj_loc, 1, GL_FALSE, projection)
    glUseProgram(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()

        
        
        glBindVertexArray(obj_vao)
        glBindTexture(GL_TEXTURE_2D, obj_tex)
        glUseProgram(obj_shader)
        glUniformMatrix4fv(obj_view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        glUseProgram(0)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
