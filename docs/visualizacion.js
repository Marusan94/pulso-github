// Configuración inicial
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Controles de órbita
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Luz ambiental
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

// Luz direccional
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(1, 1, 1);
scene.add(directionalLight);

// Cargar datos de GitHub
async function loadRepos() {
  try {
    const response = await fetch('https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc');
    const data = await response.json();
    return data.items;
  } catch (error) {
    console.error('Error al cargar repositorios:', error);
    return [];
  }
}

// Crear nodos para repositorios
function createNodes(repos) {
  const nodes = [];
  const colors = [0x5EEAD4, 0x4ADE80, 0x1D4ED8, 0xF59E0B, 0x7C3AED];
  const textureLoader = new THREE.TextureLoader();
  
  repos.slice(0, 50).forEach((repo, i) => {
    // Tamaño basado en estrellas
    const size = 5 + Math.log(repo.stargazers_count);
    const geometry = new THREE.SphereGeometry(size, 32, 32);
    
    // Material con textura (inspirado en tus videos)
    const material = new THREE.MeshPhongMaterial({
      color: colors[i % colors.length],
      shininess: 30,
      specular: 0xffffff,
      transparent: true,
      opacity: 0.9
    });
    
    // Cargar imagen de avatar del repositorio
    const avatarUrl = `https://avatars.githubusercontent.com/${repo.owner.login}`;
    textureLoader.load(avatarUrl, (texture) => {
      material.map = texture;
      material.needsUpdate = true;
    });
    
    const node = new THREE.Mesh(geometry, material);
    
    // Posicionamiento en esfera
    const phi = Math.acos(-1 + (2 * i) / repos.length);
    const theta = Math.sqrt(repos.length * Math.PI) * phi;
    node.position.set(
      100 * Math.cos(theta) * Math.sin(phi),
      100 * Math.sin(theta) * Math.sin(phi),
      100 * Math.cos(phi)
    );
    
    // Añadir información detallada del repositorio
    node.userData = {
      name: repo.full_name,
      stars: repo.stargazers_count,
      forks: repo.forks_count,
      language: repo.language,
      url: repo.html_url,
      description: repo.description,
      createdAt: repo.created_at,
      updatedAt: repo.updated_at
    };
    
    // Añadir efecto de brillo (inspirado en tus videos)
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: colors[i % colors.length],
      transparent: true,
      opacity: 0.3,
      blending: THREE.AdditiveBlending
    });
    const glow = new THREE.Mesh(geometry.clone().scale(1.1, 1.1, 1.1), glowMaterial);
    node.add(glow);
    
    scene.add(node);
    nodes.push(node);
  });
  
  return nodes;
}

// Crear conexiones entre nodos
function createConnections(nodes) {
  const connections = [];
  
  // Material para conexiones
  const lineMaterial = new THREE.LineBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.3
  });
  
  // Material para conexiones activas (inspirado en tus videos)
  const activeLineMaterial = new THREE.LineBasicMaterial({
    color: 0x5EEAD4,
    linewidth: 2,
    transparent: true,
    opacity: 0.8
  });
  
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      if (Math.random() > 0.7) { // 30% de probabilidad de conexión
        const points = [];
        points.push(nodes[i].position);
        points.push(nodes[j].position);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, lineMaterial);
        
        // Añadir animación de conexión (inspirado en tus videos)
        line.userData = {
          active: false,
          targetOpacity: 0.3,
          speed: 0.01 + Math.random() * 0.02
        };
        
        scene.add(line);
        connections.push(line);
      }
    }
  }
  
  // Animación de conexiones
  function animateConnections() {
    connections.forEach(line => {
      if (line.userData.active) {
        // Animación de conexión activa
        line.material = activeLineMaterial;
        line.material.opacity = 0.8 + Math.sin(Date.now() * 0.002) * 0.2;
      } else {
        // Animación de conexión normal
        line.material = lineMaterial;
        line.material.opacity = line.userData.targetOpacity + Math.sin(Date.now() * line.userData.speed) * 0.1;
      }
    });
  }
  
  return { connections, animateConnections };
}

// Animación principal
async function init() {
  camera.position.z = 200;
  
  const repos = await loadRepos();
  const nodes = createNodes(repos);
  const { connections, animateConnections } = createConnections(nodes);
  
  // Añadir interactividad avanzada
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  let selectedNode = null;
  let infoPanel = null;
  
  // Crear panel de información
  function createInfoPanel(node) {
    if (infoPanel) scene.remove(infoPanel);
    
    const panelWidth = 300;
    const panelHeight = 200;
    const panelGeometry = new THREE.PlaneGeometry(panelWidth, panelHeight);
    const panelMaterial = new THREE.MeshBasicMaterial({
      color: 0x1a1a1a,
      transparent: true,
      opacity: 0.9,
      side: THREE.DoubleSide
    });
    
    infoPanel = new THREE.Mesh(panelGeometry, panelMaterial);
    infoPanel.position.set(node.position.x + panelWidth/2 + 20, node.position.y, node.position.z);
    
    // Añadir texto con información del repositorio
    const canvas = document.createElement('canvas');
    canvas.width = panelWidth * 2;
    canvas.height = panelHeight * 2;
    const context = canvas.getContext('2d');
    
    // Estilo del texto (inspirado en tus videos)
    context.fillStyle = '#ffffff';
    context.font = '16px Arial';
    context.textAlign = 'left';
    context.textBaseline = 'top';
    
    // Información del repositorio
    context.fillText(`Repositorio: ${node.userData.name}`, 20, 20);
    context.fillText(`Estrellas: ${node.userData.stars}`, 20, 50);
    context.fillText(`Bifurcaciones: ${node.userData.forks}`, 20, 80);
    context.fillText(`Lenguaje: ${node.userData.language || 'No especificado'}`, 20, 110);
    context.fillText(`Creado: ${new Date(node.userData.createdAt).toLocaleDateString()}`, 20, 140);
    context.fillText(`Actualizado: ${new Date(node.userData.updatedAt).toLocaleDateString()}`, 20, 170);
    
    const texture = new THREE.CanvasTexture(canvas);
    const textMaterial = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
    const textPlane = new THREE.Mesh(new THREE.PlaneGeometry(panelWidth, panelHeight), textMaterial);
    textPlane.position.set(0, 0, 0.1);
    
    infoPanel.add(textPlane);
    scene.add(infoPanel);
  }
  
  function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    
    // Resaltar conexiones relacionadas
    if (selectedNode) {
      connections.forEach(line => {
        line.userData.active = false;
      });
      
      const nodeIndex = nodes.indexOf(selectedNode);
      connections.forEach(line => {
        const points = line.geometry.attributes.position.array;
        const p1 = new THREE.Vector3(points[0], points[1], points[2]);
        const p2 = new THREE.Vector3(points[3], points[4], points[5]);
        
        if (p1.distanceTo(selectedNode.position) < 1 || p2.distanceTo(selectedNode.position) < 1) {
          line.userData.active = true;
        }
      });
    }
  }
  
  function onClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodes);
    
    if (intersects.length > 0) {
      const node = intersects[0].object;
      selectedNode = node;
      createInfoPanel(node);
      
      // Animar selección
      node.scale.set(1.2, 1.2, 1.2);
      nodes.forEach(n => {
        if (n !== node) n.scale.set(0.8, 0.8, 0.8);
      });
    } else {
      selectedNode = null;
      if (infoPanel) scene.remove(infoPanel);
      infoPanel = null;
      
      // Restaurar escala
      nodes.forEach(n => n.scale.set(1, 1, 1));
      connections.forEach(line => line.userData.active = false);
    }
  }
  
  window.addEventListener('mousemove', onMouseMove, false);
  window.addEventListener('click', onClick, false);
  
  // Animación
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    animateConnections();
    renderer.render(scene, camera);
  }
  
  animate();
}

// Manejar redimensionamiento
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Iniciar visualización
init();