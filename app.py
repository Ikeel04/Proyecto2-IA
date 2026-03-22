import streamlit as st
import time
from maze import load_maze, find_positions
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.greedy import greedy
from visualization import maze_to_colors

st.title("🧩 Resolvedor de Laberintos")

# 🧠 Inicializar estado
if "show_animation" not in st.session_state:
    st.session_state["show_animation"] = False

if "last_algo" not in st.session_state:
    st.session_state["last_algo"] = None

if "last_heuristic" not in st.session_state:
    st.session_state["last_heuristic"] = None

uploaded_file = st.file_uploader("Sube un laberinto (.txt)")

if uploaded_file:
    with open("temp_maze.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())

    maze = load_maze("temp_maze.txt")

    starts = find_positions(maze, '2')
    goals = find_positions(maze, '3')

    if not starts or not goals:
        st.error("El laberinto debe tener al menos un inicio (2) y una meta (3)")
        st.stop()

    st.write(f"Start: {starts}")
    st.write(f"Goal: {goals}")

    algo_option = st.selectbox("Algoritmo", ["BFS", "DFS", "A*", "Greedy"])

    if algo_option in ["A*", "Greedy"]:
        heuristic_option = st.selectbox("Heurística", ["manhattan", "euclidean"])
    else:
        heuristic_option = None

    # 🔄 Detectar cambio de configuración
    if (
        st.session_state["last_algo"] != algo_option
        or st.session_state["last_heuristic"] != heuristic_option
    ):
        st.session_state["show_animation"] = False

    # 💾 Actualizar valores actuales
    st.session_state["last_algo"] = algo_option
    st.session_state["last_heuristic"] = heuristic_option

    # 🔘 BOTÓN RUN
    if st.button("Run"):
        start = starts[0]

        t0 = time.perf_counter()

        if algo_option == "BFS":
            path, nodes, explored = bfs(maze, start, goals)

        elif algo_option == "DFS":
            path, nodes, explored = dfs(maze, start, goals)

        elif algo_option == "A*":
            path, nodes, explored = astar(maze, start, goals, heuristic_option)

        else:
            path, nodes, explored = greedy(maze, start, goals, heuristic_option)

        t1 = time.perf_counter()

        # 💾 Guardar resultados
        st.session_state["path"] = path
        st.session_state["nodes"] = nodes
        st.session_state["explored"] = explored
        st.session_state["algo"] = algo_option
        st.session_state["start"] = start
        st.session_state["goals"] = goals
        st.session_state["time"] = t1 - t0

        # 🔄 Reset animación
        st.session_state["show_animation"] = False

    # 📦 Mostrar resultados si existen
    if "path" in st.session_state:
        path = st.session_state["path"]
        nodes = st.session_state["nodes"]
        explored = st.session_state["explored"]
        algo_option = st.session_state["algo"]
        start = st.session_state["start"]
        goals = st.session_state["goals"]
        elapsed_time = st.session_state["time"]

        if path:
            st.success(f"Solución encontrada ({algo_option})")
            st.write(f"📏 Largo del camino: {len(path)}")

            placeholder = st.empty()

            # 🎬 Botón animación
            if st.button("Mostrar animación"):
                st.session_state["show_animation"] = True

            # 🧠 Mostrar según estado
            if st.session_state["show_animation"]:
                for i in range(0, len(explored), max(1, len(explored)//60)):
                    partial = explored[:i]
                    img = maze_to_colors(maze, partial, start, goals, scale=20)
                    placeholder.image(img, caption="Explorando...", width=500)
                    time.sleep(0.03)

                final_img = maze_to_colors(maze, path, start, goals, scale=20)
                placeholder.image(final_img, caption="Solución final", width=500)

            else:
                final_img = maze_to_colors(maze, path, start, goals, scale=20)
                placeholder.image(final_img, caption="Solución final", width=500)

        else:
            st.error("No hay solución")

        st.write(f"🔍 Nodos explorados: {nodes}")
        st.write(f"⏱️ Tiempo: {elapsed_time:.8f} segundos")