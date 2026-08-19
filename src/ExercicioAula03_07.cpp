// Este exemplo apresenta uma aplicação completa de OpenGL, que renderiza um triângulo e um quadrado na tela.
#include <iostream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <vector>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

GLuint Vao_circulo;
int numFatias = 40;

GLFWwindow* Window = nullptr;
GLuint Shader_programm1 = 0;
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

void inicializaCirculo() {
    glGenVertexArrays(1, &Vao_circulo);
    glBindVertexArray(Vao_circulo);

    std::vector<float> vertices;
    float raio = 0.5f;
    float anguloIncremento = (2.0f * M_PI) / numFatias;

    // Gerando os N triângulos
    for (int i = 0; i < numFatias; i++) {
        float anguloAtual = i * anguloIncremento;
        float proximoAngulo = (i + 1) * anguloIncremento;

        // 1. Vértice central (origem)
        vertices.push_back(0.0f);
        vertices.push_back(0.0f);
        vertices.push_back(0.0f);
        
        // 2. Vértice atual da borda
        vertices.push_back(raio * cos(anguloAtual));
        vertices.push_back(raio * sin(anguloAtual));
        vertices.push_back(0.0f);

        // 3. Próximo vértice da borda
        vertices.push_back(raio * cos(proximoAngulo));
        vertices.push_back(raio * sin(proximoAngulo));
        vertices.push_back(0.0f);
    }

    GLuint pvbo;
    glGenBuffers(1, &pvbo);
    glBindBuffer(GL_ARRAY_BUFFER, pvbo);
    // vertices.size() * sizeof(float) para vetor dinâmico
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);
    
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);
}


void inicializaShader() {
    // Especificação do Vertex Shader
    const char* vertex_shader = 
        "#version 400\n"
        "layout(location = 0) in vec3 vertex_posicao;\n"
        "void main () {\n"
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
        "out vec4 frag_colour;\n"
        "void main () {\n"
        "    frag_colour = vec4(0.2f, 0.8f, 0.2f, 1.0f); // Verde sólido\n"
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

        // Desenha apenas o círculo usando a lógica matemática da circunferência no Fragment Shader
        glUseProgram(Shader_programm1);
        glBindVertexArray(Vao_circulo);
        glDrawArrays(GL_TRIANGLES, 0, 3 * numFatias); // 3 vertices por fatia, totalizando 3 * numFatias vertices

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
    inicializaCirculo();
    inicializaShader();
    inicializaRenderizacao();
    
    return 0;
}