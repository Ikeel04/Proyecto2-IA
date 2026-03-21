import streamlit as st
import time
from maze import load_maze, find_positions
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar

st.title("🧩 Resolvedor de Laberintos")

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

    algo_option = st.selectbox("Algoritmo", ["BFS", "DFS", "A*"])
    
    if algo_option == "A*":
        heuristic_option = st.selectbox("Heurística", ["manhattan", "euclidean"])
    else:
        heuristic_option = None

    if st.button("Run"):
        start = starts[0]

        t0 = time.perf_counter()

        if algo_option == "BFS":
            path, nodes = bfs(maze, start, goals)

        elif algo_option == "DFS":
            path, nodes = dfs(maze, start, goals)

        else:
            path, nodes = astar(maze, start, goals, heuristic_option)

        t1 = time.perf_counter()

        if path:
            st.success(f"Solución encontrada ({algo_option})")
            st.write(f"📏 Largo del camino: {len(path)}")
        else:
            st.error("No hay solución")

        st.write(f"🔍 Nodos explorados: {nodes}")
        st.write(f"⏱️ Tiempo: {t1 - t0:.8f} segundos")