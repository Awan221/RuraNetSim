// État initial du module dashboard
const state = {
  activeWidgets: [],
  availableWidgets: [
    { id: 'coverage-map', name: 'Carte de couverture', icon: 'map-marked-alt', enabled: true },
    { id: 'performance-metrics', name: 'Métriques de performance', icon: 'chart-line', enabled: true },
    { id: 'recent-simulations', name: 'Dernières simulations', icon: 'history', enabled: true },
    { id: 'usage-statistics', name: 'Statistiques', icon: 'chart-pie', enabled: true }
  ],
  dashboardLayout: {
    lg: [
      { i: 'coverage-map', x: 0, y: 0, w: 6, h: 8 },
      { i: 'performance-metrics', x: 6, y: 0, w: 6, h: 8 },
      { i: 'recent-simulations', x: 0, y: 8, w: 6, h: 8 },
      { i: 'usage-statistics', x: 6, y: 8, w: 6, h: 8 }
    ],
    md: [
      { i: 'coverage-map', x: 0, y: 0, w: 6, h: 8 },
      { i: 'performance-metrics', x: 6, y: 0, w: 6, h: 8 },
      { i: 'recent-simulations', x: 0, y: 8, w: 6, h: 8 },
      { i: 'usage-statistics', x: 6, y: 8, w: 6, h: 8 }
    ],
    sm: [
      { i: 'coverage-map', x: 0, y: 0, w: 2, h: 8 },
      { i: 'performance-metrics', x: 2, y: 0, w: 2, h: 8 },
      { i: 'recent-simulations', x: 0, y: 8, w: 2, h: 8 },
      { i: 'usage-statistics', x: 2, y: 8, w: 2, h: 8 }
    ],
    xs: [
      { i: 'coverage-map', x: 0, y: 0, w: 1, h: 8 },
      { i: 'performance-metrics', x: 0, y: 8, w: 1, h: 8 },
      { i: 'recent-simulations', x: 0, y: 16, w: 1, h: 8 },
      { i: 'usage-statistics', x: 0, y: 24, w: 1, h: 8 }
    ]
  },
  filters: {
    period: '7days',
    technology: 'all',
    areaType: 'all'
  },
  loading: false,
  error: null
};

// Getters
const getters = {
  activeWidgets: state => state.activeWidgets,
  availableWidgets: state => state.availableWidgets,
  dashboardLayout: state => state.dashboardLayout,
  filters: state => state.filters,
  isLoading: state => state.loading,
  error: state => state.error
};

// Mutations
const mutations = {
  SET_ACTIVE_WIDGETS(state, widgets) {
    state.activeWidgets = widgets;
  },
  UPDATE_WIDGET_LAYOUT(state, { breakpoint, layout }) {
    state.dashboardLayout[breakpoint] = layout;
  },
  UPDATE_FILTERS(state, filters) {
    state.filters = { ...state.filters, ...filters };
  },
  TOGGLE_WIDGET(state, widgetId) {
    const widget = state.availableWidgets.find(w => w.id === widgetId);
    if (widget) {
      widget.enabled = !widget.enabled;
    }
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  // Initialiser le tableau de bord avec les paramètres sauvegardés
  INIT_DASHBOARD(state) {
    const savedLayout = localStorage.getItem('dashboardLayout');
    const savedFilters = localStorage.getItem('dashboardFilters');
    const savedWidgets = localStorage.getItem('enabledWidgets');

    if (savedLayout) {
      state.dashboardLayout = JSON.parse(savedLayout);
    }
    
    if (savedFilters) {
      state.filters = JSON.parse(savedFilters);
    }
    
    if (savedWidgets) {
      const enabledWidgets = JSON.parse(savedWidgets);
      state.availableWidgets = state.availableWidgets.map(widget => ({
        ...widget,
        enabled: enabledWidgets.includes(widget.id)
      }));
    }
    
    state.activeWidgets = state.availableWidgets
      .filter(widget => widget.enabled)
      .map(widget => widget.id);
  }
};

// Actions
const actions = {
  // Initialiser le tableau de bord
  initializeDashboard({ commit }) {
    commit('INIT_DASHBOARD');
  },
  
  // Mettre à jour la disposition des widgets
  updateWidgetLayout({ commit, state }, { breakpoint, layout }) {
    commit('UPDATE_WIDGET_LAYOUT', { breakpoint, layout });
    localStorage.setItem('dashboardLayout', JSON.stringify(state.dashboardLayout));
  },
  
  // Basculer l'état d'un widget (activé/désactivé)
  toggleWidget({ commit, state }, widgetId) {
    commit('TOGGLE_WIDGET', widgetId);
    
    // Mettre à jour la liste des widgets actifs
    const activeWidgets = state.availableWidgets
      .filter(widget => widget.enabled)
      .map(widget => widget.id);
      
    commit('SET_ACTIVE_WIDGETS', activeWidgets);
    
    // Sauvegarder la configuration
    const enabledWidgets = state.availableWidgets
      .filter(widget => widget.enabled)
      .map(widget => widget.id);
    
    localStorage.setItem('enabledWidgets', JSON.stringify(enabledWidgets));
  },
  
  // Mettre à jour les filtres
  updateFilters({ commit, state }, filters) {
    commit('UPDATE_FILTERS', filters);
    localStorage.setItem('dashboardFilters', JSON.stringify(state.filters));
  },
  
  // Réinitialiser la disposition par défaut
  resetLayout({ commit, state }) {
    const defaultLayout = {
      lg: [
        { i: 'coverage-map', x: 0, y: 0, w: 6, h: 8 },
        { i: 'performance-metrics', x: 6, y: 0, w: 6, h: 8 },
        { i: 'recent-simulations', x: 0, y: 8, w: 6, h: 8 },
        { i: 'usage-statistics', x: 6, y: 8, w: 6, h: 8 }
      ],
      md: [
        { i: 'coverage-map', x: 0, y: 0, w: 6, h: 8 },
        { i: 'performance-metrics', x: 6, y: 0, w: 6, h: 8 },
        { i: 'recent-simulations', x: 0, y: 8, w: 6, h: 8 },
        { i: 'usage-statistics', x: 6, y: 8, w: 6, h: 8 }
      ],
      sm: [
        { i: 'coverage-map', x: 0, y: 0, w: 2, h: 8 },
        { i: 'performance-metrics', x: 2, y: 0, w: 2, h: 8 },
        { i: 'recent-simulations', x: 0, y: 8, w: 2, h: 8 },
        { i: 'usage-statistics', x: 2, y: 8, w: 2, h: 8 }
      ],
      xs: [
        { i: 'coverage-map', x: 0, y: 0, w: 1, h: 8 },
        { i: 'performance-metrics', x: 0, y: 8, w: 1, h: 8 },
        { i: 'recent-simulations', x: 0, y: 16, w: 1, h: 8 },
        { i: 'usage-statistics', x: 0, y: 24, w: 1, h: 8 }
      ]
    };
    
    commit('SET_LAYOUT', defaultLayout);
    localStorage.setItem('dashboardLayout', JSON.stringify(defaultLayout));
  },
  
  // Réinitialiser les filtres
  resetFilters({ commit }) {
    const defaultFilters = {
      period: '7days',
      technology: 'all',
      areaType: 'all'
    };
    
    commit('UPDATE_FILTERS', defaultFilters);
    localStorage.setItem('dashboardFilters', JSON.stringify(defaultFilters));
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
