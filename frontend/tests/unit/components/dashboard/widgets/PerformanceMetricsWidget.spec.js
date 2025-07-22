import { mount } from '@vue/test-utils';
import PerformanceMetricsWidget from '@/components/dashboard/widgets/PerformanceMetricsWidget.vue';

describe('PerformanceMetricsWidget.vue', () => {
  // Données de test
  const mockSimulations = [
    {
      id: 1,
      name: 'Test Simulation 1',
      technology: '5G',
      terrain_type: 'URBAN',
      status: 'completed',
      coverage_percentage: 85,
      avg_signal_strength: -75,
      created_at: '2023-01-01T10:00:00Z'
    },
    {
      id: 2,
      name: 'Test Simulation 2',
      technology: '4G',
      terrain_type: 'RURAL',
      status: 'completed',
      coverage_percentage: 65,
      avg_signal_strength: -85,
      created_at: '2023-01-02T10:00:00Z'
    }
  ];

  it('affiche un message quand il n\'y a pas de simulations', () => {
    const wrapper = mount(PerformanceMetricsWidget, {
      props: {
        simulations: []
      }
    });

    expect(wrapper.text()).toContain('Aucune donnée de simulation à afficher');
    expect(wrapper.find('i.fa-chart-bar').exists()).toBe(true);
  });

  it('affiche les métriques de performance quand il y a des simulations', async () => {
    const wrapper = mount(PerformanceMetricsWidget, {
      props: {
        simulations: mockSimulations
      }
    });

    // Vérifie que les métriques sont affichées
    expect(wrapper.text()).toContain('Couverture moyenne');
    expect(wrapper.text()).toContain('Simulations');
    expect(wrapper.text()).toContain('Signal moyen');
    expect(wrapper.text()).toContain('Taux de réussite');

    // Vérifie que le graphique est rendu
    expect(wrapper.find('canvas').exists()).toBe(true);
  });

  it('calcule correctement les métriques', async () => {
    const wrapper = mount(PerformanceMetricsWidget, {
      props: {
        simulations: mockSimulations
      }
    });

    // Vérifie que les métriques sont calculées correctement
    const metrics = wrapper.vm.metrics;
    
    // Couverture moyenne: (85 + 65) / 2 = 75
    expect(metrics.averageCoverage).toBe(75);
    
    // Nombre total de simulations
    expect(metrics.totalSimulations).toBe(2);
    
    // Signal moyen: (-75 + -85) / 2 = -80
    expect(metrics.avgSignalStrength).toBe(-80);
    
    // Taux de réussite: 100% car les deux simulations sont terminées avec couverture > 50%
    expect(metrics.successRate).toBe(100);
  });

  it('met à jour les métriques quand les simulations changent', async () => {
    const wrapper = mount(PerformanceMetricsWidget, {
      props: {
        simulations: [mockSimulations[0]]
      }
    });

    // Vérifie la métrique initiale
    expect(wrapper.vm.metrics.totalSimulations).toBe(1);

    // Met à jour les simulations
    await wrapper.setProps({
      simulations: [...mockSimulations]
    });

    // Vérifie que les métriques ont été mises à jour
    expect(wrapper.vm.metrics.totalSimulations).toBe(2);
  });

  it('affiche correctement les variations', async () => {
    const wrapper = mount(PerformanceMetricsWidget, {
      props: {
        simulations: mockSimulations
      }
    });

    // Vérifie que les icônes de variation sont présentes
    expect(wrapper.find('.fa-arrow-up').exists() || 
           wrapper.find('.fa-arrow-down').exists() || 
           wrapper.find('.fa-equals').exists()).toBe(true);
  });
});
