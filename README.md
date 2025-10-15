# 🚌 Sri Lanka Bus Route Planner

An interactive web application that demonstrates and compares different pathfinding algorithms (BFS, DFS, A*, Greedy) for planning bus routes across Sri Lanka's major cities.

## 🎯 Features

- **Multiple Search Algorithms**: Compare BFS, DFS, A*, and Greedy Best-First Search
- **Real-time Visualization**: Interactive SVG-based route map showing explored nodes and optimal paths
- **Comprehensive Metrics**: Track nodes explored, travel time, distance, and fare
- **20 Major Locations**: Covers key cities from Negombo to Moratuwa, including Colombo suburbs
- **Beautiful UI**: Modern gradient design with responsive layout

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sri-lanka-bus-route-planner.git
cd sri-lanka-bus-route-planner
```

2. Install dependencies:
```bash
pip install streamlit
```

3. Run the application:
```bash
streamlit run Bus_Route_Planner.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📖 How to Use

1. **Select Starting Point**: Choose your departure location from the dropdown
2. **Choose Destination**: Select where you want to go
3. **Pick Algorithm**: Select one of four search algorithms to compare performance
4. **Find Route**: Click the "Find Route" button to see the results
5. **Analyze**: Compare metrics, view the visualization, and see step-by-step journey details

## 🧠 Algorithms Explained

### Uninformed Search
- **BFS (Breadth-First Search)**: Explores level by level, guarantees shortest path by number of stops
- **DFS (Depth-First Search)**: Goes deep first, faster but may not find optimal path

### Informed Search
- **A* Search**: Uses haversine distance heuristic for optimal and efficient pathfinding
- **Greedy Best-First**: Always moves toward goal, fast but not always optimal

## 📊 Technical Details

- **Distance Calculation**: Haversine formula for accurate geographic distance
- **Route Data**: Real bus routes with actual bus numbers (e.g., 240, 903, 138)
- **Cost Metrics**: Distance (km), Time (minutes), Fare (LKR)
- **Visualization**: Custom SVG rendering with color-coded exploration states

## 🎨 UI Components

- Gradient color schemes for visual appeal
- Responsive metric cards
- Interactive route visualization
- Step-by-step journey breakdown
- Algorithm comparison information

## 📝 Project Structure

```
sri-lanka-bus-route-planner/
│
├── Bus_Route_Planner.py    # Main application file
└── README.md                # This file
```

---

⭐ If you find this project helpful, please consider giving it a star!
