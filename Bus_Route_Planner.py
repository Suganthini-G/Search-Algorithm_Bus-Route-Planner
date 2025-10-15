"""
Sri Lanka Bus Route Planner - Streamlit Web App
Compare Search Algorithms: BFS, DFS, A*, Greedy
"""

import streamlit as st
import math
from collections import deque
from queue import PriorityQueue

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Sri Lanka Bus Route Planner",
    page_icon="🚌",
    layout="wide"
)

# ------------------------------
# CUSTOM STYLES
# ------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #efffcf;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .algo-info {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        color: #1e3a8a;
    }
    .route-step {
        background: #ecfdf5;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 3px solid #10b981;
        color: #065f46;
    }

    /* Sidebar button styling - base styles */
    section[data-testid="stSidebar"] button {
        height: 50px !important;
        width: 100% !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: 0.2s ease-in-out;
    }
    
    /* Find Route Button - Green (primary type) */
    section[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(135deg, #fda4af, #f43f5e) !important; /* pink to soft red */
    color: #ffffff !important;
    box-shadow: 0 2px 6px rgba(244,63,94,0.35) !important;
    }
    section[data-testid="stSidebar"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #fecdd3, #e11d48) !important; /* lighter hover */
        transform: scale(1.02);
    }
    
    /* Reset Button - Orange (secondary type) */
    section[data-testid="stSidebar"] button[kind="secondary"] {
    background: linear-gradient(135deg, #e5e7eb, #9ca3af) !important; /* light gray gradient */
    color: #111827 !important; /* dark text for contrast */
    box-shadow: 0 2px 6px rgba(156,163,175,0.35) !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #f3f4f6, #6b7280) !important; /* slightly brighter on hover */
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# CORE CLASSES
# ------------------------------
class BusStop:
    def __init__(self, name, x, y, lat, lon):
        self.name = name
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon

class BusRoute:
    def __init__(self, from_stop, to_stop, distance, time, fare, bus_no):
        self.from_stop = from_stop
        self.to_stop = to_stop
        self.distance = distance
        self.time = time
        self.fare = fare
        self.bus_no = bus_no

class BusRoutePlanner:
    def __init__(self):
        self.init_bus_stops()
        self.init_routes()

    def init_bus_stops(self):
        self.bus_stops = {
            'Fort': BusStop('Fort', 150, 300, 6.9344, 79.8428),
            'Pettah': BusStop('Pettah', 200, 280, 6.9387, 79.8550),
            'Maradana': BusStop('Maradana', 250, 270, 6.9297, 79.8606),
            'Kollupitiya': BusStop('Kollupitiya', 180, 350, 6.9147, 79.8500),
            'Bambalapitiya': BusStop('Bambalapitiya', 220, 370, 6.8942, 79.8553),
            'Wellawatte': BusStop('Wellawatte', 260, 390, 6.8774, 79.8573),
            'Dehiwala': BusStop('Dehiwala', 300, 410, 6.8559, 79.8642),
            'Mount Lavinia': BusStop('Mount Lavinia', 340, 430, 6.8382, 79.8637),
            'Moratuwa': BusStop('Moratuwa', 380, 450, 6.7730, 79.8816),
            'Kaduwela': BusStop('Kaduwela', 350, 230, 6.9333, 79.9833),
            'Malabe': BusStop('Malabe', 400, 250, 6.9097, 79.9536),
            'Maharagama': BusStop('Maharagama', 320, 350, 6.8484, 79.9267),
            'Nugegoda': BusStop('Nugegoda', 280, 330, 6.8649, 79.8997),
            'Rajagiriya': BusStop('Rajagiriya', 300, 290, 6.9089, 79.8867),
            'Negombo': BusStop('Negombo', 50, 150, 7.2083, 79.8358),
            'Katunayake': BusStop('Katunayake', 100, 200, 7.1697, 79.8844),
            'Ja-Ela': BusStop('Ja-Ela', 120, 220, 7.0742, 79.8919),
            'Kelaniya': BusStop('Kelaniya', 220, 240, 6.9553, 79.9219),
            'Kiribathgoda': BusStop('Kiribathgoda', 260, 220, 6.9789, 79.9292),
            'Gampaha': BusStop('Gampaha', 200, 180, 7.0911, 79.9956)
        }

    def init_routes(self):
        routes_data = [
            ('Negombo', 'Katunayake', 8, 15, 30, '240'),
            ('Katunayake', 'Ja-Ela', 6, 12, 25, '240'),
            ('Ja-Ela', 'Fort', 22, 45, 50, '240'),
            ('Negombo', 'Gampaha', 25, 50, 60, '903'),
            ('Gampaha', 'Kiribathgoda', 12, 25, 35, '903'),
            ('Kiribathgoda', 'Kelaniya', 8, 15, 25, '903'),
            ('Kelaniya', 'Pettah', 7, 18, 20, '235'),
            ('Fort', 'Pettah', 2, 8, 15, '138'),
            ('Pettah', 'Maradana', 3, 10, 15, '138'),
            ('Maradana', 'Rajagiriya', 6, 15, 25, '177'),
            ('Rajagiriya', 'Kaduwela', 8, 20, 30, '177'),
            ('Kaduwela', 'Malabe', 5, 12, 20, '177'),
            ('Fort', 'Kollupitiya', 3, 10, 18, '100'),
            ('Kollupitiya', 'Bambalapitiya', 2, 8, 15, '100'),
            ('Bambalapitiya', 'Wellawatte', 3, 10, 18, '100'),
            ('Wellawatte', 'Dehiwala', 3, 12, 20, '100'),
            ('Dehiwala', 'Mount Lavinia', 2, 8, 15, '100'),
            ('Mount Lavinia', 'Moratuwa', 5, 15, 25, '155'),
            ('Rajagiriya', 'Nugegoda', 4, 12, 20, '138'),
            ('Nugegoda', 'Maharagama', 3, 10, 18, '138'),
            ('Maharagama', 'Dehiwala', 4, 12, 20, '154'),
            ('Kelaniya', 'Kaduwela', 12, 30, 40, '245')
        ]
        self.routes = []
        for r in routes_data:
            self.routes.append(BusRoute(r[0], r[1], r[2], r[3], r[4], r[5]))
            self.routes.append(BusRoute(r[1], r[0], r[2], r[3], r[4], r[5]))

    def haversine_distance(self, stop1, stop2):
        R = 6371
        lat1 = math.radians(self.bus_stops[stop1].lat)
        lat2 = math.radians(self.bus_stops[stop2].lat)
        dlat = math.radians(self.bus_stops[stop2].lat - self.bus_stops[stop1].lat)
        dlon = math.radians(self.bus_stops[stop2].lon - self.bus_stops[stop1].lon)
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_neighbors(self, stop):
        return [(r.to_stop, r) for r in self.routes if r.from_stop == stop]

    def bfs_search(self, start, goal):
        queue = deque([[start]])
        visited = {start}
        exploration_order = [start]
        nodes_explored = 0
        while queue:
            path = queue.popleft()
            current = path[-1]
            nodes_explored += 1
            if current == goal:
                return {'path': path, 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}
            for neighbor, _ in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    exploration_order.append(neighbor)
                    queue.append(path + [neighbor])
        return {'path': [], 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}

    def dfs_search(self, start, goal):
        stack = [[start]]
        visited = {start}
        exploration_order = [start]
        nodes_explored = 0
        while stack:
            path = stack.pop()
            current = path[-1]
            nodes_explored += 1
            if current == goal:
                return {'path': path, 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}
            for neighbor, _ in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    exploration_order.append(neighbor)
                    stack.append(path + [neighbor])
        return {'path': [], 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}

    def astar_search(self, start, goal):
        pq = PriorityQueue()
        pq.put((0, 0, start, [start]))
        visited = set()
        exploration_order = [start]
        nodes_explored = 0
        counter = 1
        g_scores = {start: 0}
        while not pq.empty():
            f, _, current, path = pq.get()
            nodes_explored += 1
            if current == goal:
                return {'path': path, 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}
            if current in visited:
                continue
            visited.add(current)
            for neighbor, route in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                g = g_scores[current] + route.distance
                h = self.haversine_distance(neighbor, goal)
                f = g + h
                if neighbor not in g_scores or g < g_scores[neighbor]:
                    g_scores[neighbor] = g
                    if neighbor not in exploration_order:
                        exploration_order.append(neighbor)
                    pq.put((f, counter, neighbor, path + [neighbor]))
                    counter += 1
        return {'path': [], 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}

    def greedy_search(self, start, goal):
        pq = PriorityQueue()
        pq.put((0, 0, start, [start]))
        visited = set()
        exploration_order = [start]
        nodes_explored = 0
        counter = 1
        while not pq.empty():
            h, _, current, path = pq.get()
            nodes_explored += 1
            if current == goal:
                return {'path': path, 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}
            if current in visited:
                continue
            visited.add(current)
            for neighbor, _ in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                h_val = self.haversine_distance(neighbor, goal)
                if neighbor not in exploration_order:
                    exploration_order.append(neighbor)
                pq.put((h_val, counter, neighbor, path + [neighbor]))
                counter += 1
        return {'path': [], 'exploration_order': exploration_order, 'nodes_explored': nodes_explored}

    def calculate_route_stats(self, path):
        total_distance = total_time = total_fare = 0
        segments = []
        for i in range(len(path) - 1):
            for route in self.routes:
                if route.from_stop == path[i] and route.to_stop == path[i + 1]:
                    total_distance += route.distance
                    total_time += route.time
                    total_fare += route.fare
                    segments.append(route)
                    break
        return {
            'total_distance': total_distance,
            'total_time': total_time,
            'total_fare': total_fare,
            'segments': segments
        }

# ------------------------------
# STREAMLIT APP BODY
# ------------------------------
@st.cache_resource
def get_planner():
    return BusRoutePlanner()

planner = get_planner()

st.markdown('<div class="main-header">🚌 Sri Lanka Bus Route Planner</div>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("🗺️ Journey Details")
start_stop = st.sidebar.selectbox("Starting Point", list(planner.bus_stops.keys()),
                                  index=list(planner.bus_stops.keys()).index('Negombo'))
end_stop = st.sidebar.selectbox("Destination", list(planner.bus_stops.keys()),
                                index=list(planner.bus_stops.keys()).index('Moratuwa'))
algorithm = st.sidebar.selectbox("Search Algorithm", ["BFS", "DFS", "A*", "Greedy"], index=2)

# Buttons
search_button = st.sidebar.button("🔍 Find Route", use_container_width=True, key="find_btn", type="primary")
reset_button = st.sidebar.button("🔄 Reset", use_container_width=True, key="reset_btn", type="secondary")

if reset_button:
    st.session_state.clear()
    st.rerun()

# Main content
if search_button:
    if start_stop == end_stop:
        st.error("⚠️ Start and end stops must be different!")
    else:
        with st.spinner("Finding optimal route..."):
            if "BFS" in algorithm and "Greedy" not in algorithm:
                result = planner.bfs_search(start_stop, end_stop)
            elif "DFS" in algorithm:
                result = planner.dfs_search(start_stop, end_stop)
            elif "A*" in algorithm:
                result = planner.astar_search(start_stop, end_stop)
            else:
                result = planner.greedy_search(start_stop, end_stop)

            if not result['path']:
                st.error("❌ No route found between the selected stops!")
            else:
                stats = planner.calculate_route_stats(result['path'])
                result.update(stats)

                st.success(f"✅ Route found using {algorithm}!")

                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🔢 Nodes Explored", result['nodes_explored'])
                col2.metric("⏱️ Travel Time", f"{result['total_time']} min")
                col3.metric("📏 Distance", f"{result['total_distance']:.1f} km")
                col4.metric("💵 Total Fare", f"Rs. {result['total_fare']}")

                # Visualization
                st.markdown("---")
                st.subheader("🗺️ Route Visualization")
                svg_width, svg_height = 500, 500
                svg_content = f'<svg width="{svg_width}" height="{svg_height}" style="background: white; border: 2px solid #e5e7eb; border-radius: 8px;">'
                for route in planner.routes:
                    from_stop = planner.bus_stops[route.from_stop]
                    to_stop = planner.bus_stops[route.to_stop]
                    is_optimal = any(
                        route.from_stop == result['path'][i] and route.to_stop == result['path'][i+1]
                        for i in range(len(result['path']) - 1)
                    )
                    color = "#fcd34d" if is_optimal else "#e5e7eb"
                    width = "4" if is_optimal else "1"
                    svg_content += f'<line x1="{from_stop.x}" y1="{from_stop.y}" x2="{to_stop.x}" y2="{to_stop.y}" stroke="{color}" stroke-width="{width}" opacity="0.85" />'
                for name, stop in planner.bus_stops.items():
                    if name == start_stop:
                        color = "#16a34a"
                    elif name == end_stop:
                        color = "#dc2626"
                    elif name in result['path']:
                        color = "#fbbf24"
                    elif name in result['exploration_order']:
                        color = "#93c5fd"
                    else:
                        color = "#9ca3af"
                    svg_content += f'<circle cx="{stop.x}" cy="{stop.y}" r="8" fill="{color}" stroke="#1f2937" stroke-width="2" />'
                    svg_content += f'<text x="{stop.x}" y="{stop.y - 15}" text-anchor="middle" font-size="10" font-weight="bold" fill="#1f2937">{name}</text>'
                svg_content += '</svg>'
                st.markdown(svg_content, unsafe_allow_html=True)

                cols = st.columns(4)
                cols[0].markdown("🟢 Start")
                cols[1].markdown("🔴 End")
                cols[2].markdown("🟡 Optimal Path")
                cols[3].markdown("🔵 Explored")

                st.markdown("---")
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.subheader("📍 Route Path")
                    st.write(f"**Stops:** {' → '.join(result['path'])}")
                    st.write(f"**Transfers:** {len(result['path']) - 2}")
                    st.subheader("🚌 Journey Steps")
                    for i, seg in enumerate(result['segments'], 1):
                        st.markdown(f"""
                        <div class="route-step">
                            <strong>Step {i}: Bus {seg.bus_no}</strong><br>
                            {seg.from_stop} → {seg.to_stop}<br>
                            <small>⏱️ {seg.time} min | 📏 {seg.distance} km | 💵 Rs. {seg.fare}</small>
                        </div>
                        """, unsafe_allow_html=True)

                with col_right:
                    st.subheader("📊 Exploration Analysis")
                    st.write(f"**Algorithm:** {algorithm}")
                    st.write(f"**Total nodes explored:** {result['nodes_explored']}")
                    st.write(f"**Exploration order:** {' → '.join(result['exploration_order'][:10])}{'...' if len(result['exploration_order']) > 10 else ''}")
                    if "BFS" in algorithm and "Greedy" not in algorithm:
                        st.info("🔵 **BFS** explores level by level, guaranteeing the shortest path by number of stops.")
                    elif "DFS" in algorithm:
                        st.info("🟣 **DFS** goes deep first, faster but may not find the optimal path.")
                    elif "A*" in algorithm:
                        st.info("🟢 **A*** uses a heuristic (straight-line distance) to find the optimal path efficiently.")
                    else:
                        st.info("🟠 **Greedy** always moves toward the goal but may not find the optimal path.")
else:
    st.markdown("### 🎯 Algorithm Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="algo-info">
            <h4>🔵 Uninformed Search</h4>
            <p><strong>BFS (Breadth-First Search):</strong> Explores layer by layer. Guarantees shortest path by stops but may explore many nodes.</p>
            <p><strong>DFS (Depth-First Search):</strong> Goes deep first. Fast but may not find optimal path.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="algo-info">
            <h4>🟢 Informed Search</h4>
            <p><strong>A* Search:</strong> Uses distance heuristic to estimate cost to goal. Optimal and efficient - explores fewer nodes than uninformed searches.</p>
            <p><strong>Greedy Best-First:</strong> Always goes toward goal. Fast but may not be optimal path.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("### 🗺️ Popular Routes")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("🏖️ **Airport to Beach**")
        st.write("Negombo → Mount Lavinia")
    with c2:
        st.write("🏙️ **City Center Tour**")
        st.write("Fort → Bambalapitiya")
    with c3:
        st.write("🌆 **Suburb Connection**")
        st.write("Gampaha → Maharagama")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280;">
    <p>Search Algorithms | 258828H</p>
</div>
""", unsafe_allow_html=True)