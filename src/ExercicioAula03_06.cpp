// Este exemplo apresenta uma aplicação completa de OpenGL, que renderiza um triângulo e um quadrado na tela.
#include <iostream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

GLFWwindow* Window = nullptr;
GLuint Shader_programm1 = 0;
GLuint Vao_quadrado;
int WIDTH = 800;
int HEIGHT = 600;

void redimensionaCallback(GLFWwindow* window, int w, int h) {
    WIDTH = w;
    HEIGHT = h;
}

void inicializaOpenGL() {
    // Inicializa GLFW
    if (!glfwInit()) {
        std::cerr << "Falha ao inicializar o GLFW" << std::endl;
        exit(EXIT_FAILURE);
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // Obrigatório no macOS

    // Criação de uma janela
    Window = glfwCreateWindow(WIDTH, HEIGHT, "Exemplo - renderizacao de um triangulo", NULL, NULL);
    
    // Caso não seja possível criar a janela, a GLFW e a aplicação são terminadas
    if (!Window) {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetWindowSizeCallback(Window, redimensionaCallback);
    glfwMakeContextCurrent(Window);

    // inicializar o GLAD
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Falha ao inicializar o GLAD" << std::endl;
        exit(EXIT_FAILURE);
    }

    std::cout << "Placa de video: " << glGetString(GL_RENDERER) << std::endl;
    std::cout << "Versao do OpenGL: " << glGetString(GL_VERSION) << std::endl;
}

void inicializaQuadrado() {
    glGenVertexArrays(1, &Vao_quadrado);
    glBindVertexArray(Vao_quadrado);

    // VBO dos vértices - Quadrado centralizado
    float points[] = {
        // triângulo 1
         0.5f,  0.5f, 0.0f,  // vertice superior direito
         0.5f, -0.5f, 0.0f,  // vertice inferior direito
        -0.5f, -0.5f, 0.0f,  // vertice inferior esquerdo
        // triângulo 2
        -0.5f,  0.5f, 0.0f,  // vertice superior esquerdo
         0.5f,  0.5f, 0.0f,  // vertice superior direito
        -0.5f, -0.5f, 0.0f   // vertice inferior esquerdo
    };

    GLuint pvbo;
    glGenBuffers(1, &pvbo);
    glBindBuffer(GL_ARRAY_BUFFER, pvbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(points), points, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

    // Nota: O VBO de cores foi removido, pois o Fragment Shader fará o trabalho de cores
}


void inicializaShader1() {
    // Especificação do Vertex Shader
    const char* vertex_shader = 
        "#version 400\n"
        "layout(location = 0) in vec3 vertex_posicao;\n"
        "out vec3 posicao_local;\n" // Variável de saída para o Fragment Shader
        "void main () {\n"
        "    posicao_local = vertex_posicao;\n" // Repassa a coordenada original
        "    gl_Position = vec4(vertex_posicao, 1.0);\n"
        "}\n";

    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &vertex_shader, NULL);
    glCompileShader(vs);
    
    GLint success;
    char infoLog[512];
    glGetShaderiv(vs, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(vs, 512, NULL, infoLog);
        std::cerr << "Erro no vertex shader:\n" << infoLog << std::endl;
    }

    // Especificação do Fragment Shader (Lógica do Círculo)
    const char* fragment_shader = 
        "#version 400\n"
        "in vec3 posicao_local;\n"
        "out vec4 frag_colour;\n"
        "void main () {\n"
        "    // Aplica a equação da circunferência: x^2 + y^2\n"
        "    float dist_quadrada = (posicao_local.x * posicao_local.x) + (posicao_local.y * posicao_local.y);\n"
        "    \n"
        "    // Verifica se está dentro do raio de 0.4 (0.4^2 = 0.16)\n"
        "    if (dist_quadrada <= 0.16) {\n"
        "        frag_colour = vec4(1.0, 0.0, 0.0, 1.0); // Vermelho\n"
        "    } else {\n"
        "        frag_colour = vec4(0.0, 0.0, 1.0, 1.0); // Azul\n"
        "    }\n"
        "}\n";

    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &fragment_shader, NULL);
    glCompileShader(fs);
    
    glGetShaderiv(fs, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(fs, 512, NULL, infoLog);
        std::cerr << "Erro no fragment shader:\n" << infoLog << std::endl;
    }

    // Especificação do Shader Program
    Shader_programm1 = glCreateProgram();
    glAttachShader(Shader_programm1, vs);
    glAttachShader(Shader_programm1, fs);
    glLinkProgram(Shader_programm1);
    
    glGetProgramiv(Shader_programm1, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(Shader_programm1, 512, NULL, infoLog);
        std::cerr << "Erro na linkagem do shader:\n" << infoLog << std::endl;
    }

    glDeleteShader(vs);
    glDeleteShader(fs);
}

void inicializaRenderizacao() {
    while (!glfwWindowShouldClose(Window)) {
        glClear(GL_COLOR_BUFFER_BIT);
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glViewport(0, 0, WIDTH, HEIGHT);

        // Desenha apenas o quadrado usando a lógica matemática da circunferência no Fragment Shader
        glUseProgram(Shader_programm1);
        glBindVertexArray(Vao_quadrado);
        glDrawArrays(GL_TRIANGLES, 0, 6);

        glfwPollEvents();
        glfwSwapBuffers(Window);

        if (glfwGetKey(Window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            glfwSetWindowShouldClose(Window, true);
        }
    }
    
    glfwTerminate();
}

// Função principal
int main() {
    inicializaOpenGL();
    inicializaQuadrado();
    inicializaShader1();
    inicializaRenderizacao();
    
    return 0;
}