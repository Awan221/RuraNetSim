import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import RecentSimulationsWidget from '@/components/dashboard/widgets/RecentSimulationsWidget.vue';

// Création d'un routeur factice
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/simulations/1', component: { template: '<div>Détails de la simulation</div>' } },
    { path: '/simulation/new', component: { template: '<div>Nouvelle simulation</div>' } }
  ]
});

describe('RecentSimulationsWidget.vue', () => {
  // Données de test
  const mockSimulations = [
    {
      id: 1,
      name: 'Test Simulation 1',
      technology: '5G',
      terrain_type: 'URBAN',
      status: 'completed',
      coverage_percentage: 85,
      created_at: '2023-01-01T10:00:00Z'
    },
    {
      id: 2,
      name: 'Test Simulation 2',
      technology: '4G',
      terrain_type: 'RURAL',
      status: 'running',
      coverage_percentage: 65,
      created_at: '2023-01-02T10:00:00Z'
    },
    {
      id: 3,
      name: 'Test Simulation 3',
      technology: '3G',
      terrain_type: 'SUBURBAN',
      status: 'failed',
      coverage_percentage: 0,
      created_at: '2023-01-03T10:00:00Z'
    }
  ];

  it('affiche un message quand il n\'y a pas de simulations', () => {
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: []
      }
    });

    expect(wrapper.text()).toContain('Aucune simulation récente à afficher');
    expect(wrapper.find('i.fa-inbox').exists()).toBe(true);
  });

  it('affiche la liste des simulations récentes', async () => {
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: mockSimulations
      },
      global: {
        plugins: [router]
      }
    });

    // Vérifie que les simulations sont affichées
    const simulationItems = wrapper.findAll('.list-group-item');
    expect(simulationItems.length).toBe(3);

    // Vérifie que les noms des simulations sont affichés
    expect(wrapper.text()).toContain('Test Simulation 1');
    expect(wrapper.text()).toContain('Test Simulation 2');
    expect(wrapper.text()).toContain('Test Simulation 3');

    // Vérifie que les pourcentages de couverture sont affichés
    expect(wrapper.text()).toContain('85%');
    expect(wrapper.text()).toContain('65%');
    expect(wrapper.text()).toContain('0%');
  });

  it('affiche les statuts corrects', async () => {
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: mockSimulations
      },
      global: {
        plugins: [router]
      }
    });

    // Vérifie que les statuts sont correctement affichés
    expect(wrapper.text()).toContain('Terminé');
    expect(wrapper.text()).toContain('En cours');
    expect(wrapper.text()).toContain('Échoué');
  });

  it('trie les simulations par date décroissante', async () => {
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: [...mockSimulations].reverse() // Inverser l'ordre pour le test
      },
      global: {
        plugins: [router]
      }
    });

    // Récupère les IDs dans l'ordre d'affichage
    const displayedIds = wrapper.findAll('.list-group-item').map(item => {
      return item.find('h6').text();
    });

    // Vérifie que les simulations sont triées par date décroissante (3, 2, 1)
    expect(displayedIds[0]).toContain('Test Simulation 3');
    expect(displayedIds[1]).toContain('Test Simulation 2');
    expect(displayedIds[2]).toContain('Test Simulation 1');
  });

  it('limite le nombre de simulations affichées', async () => {
    // Crée plus de 5 simulations
    const manySimulations = Array.from({ length: 8 }, (_, i) => ({
      id: i + 1,
      name: `Test Simulation ${i + 1}`,
      technology: '5G',
      terrain_type: 'URBAN',
      status: 'completed',
      coverage_percentage: 80 + i,
      created_at: `2023-01-${String(i + 1).padStart(2, '0')}T10:00:00Z`
    }));

    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: manySimulations
      },
      global: {
        plugins: [router]
      }
    });

    // Vérifie que seulement 5 simulations sont affichées
    const simulationItems = wrapper.findAll('.list-group-item');
    expect(simulationItems.length).toBe(5);

    // Vérifie que les plus récentes sont affichées (les 5 dernières)
    expect(wrapper.text()).toContain('Test Simulation 8');
    expect(wrapper.text()).toContain('Test Simulation 7');
    expect(wrapper.text()).toContain('Test Simulation 6');
    expect(wrapper.text()).toContain('Test Simulation 5');
    expect(wrapper.text()).toContain('Test Simulation 4');
    expect(wrapper.text()).not.toContain('Test Simulation 3');
  });

  it('émet un événement de navigation lors du clic sur une simulation', async () => {
    const push = jest.fn();
    
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: [mockSimulations[0]]
      },
      global: {
        plugins: [router],
        mocks: {
          $router: {
            push
          }
        }
      }
    });

    // Simule un clic sur une simulation
    await wrapper.find('.list-group-item').trigger('click');
    
    // Vérifie que la navigation a été déclenchée
    expect(push).toHaveBeenCalledWith(`/simulations/${mockSimulations[0].id}`);
  });

  it('émet un événement de nouvelle simulation lors du clic sur le bouton', async () => {
    const push = jest.fn();
    
    const wrapper = mount(RecentSimulationsWidget, {
      props: {
        simulations: mockSimulations
      },
      global: {
        plugins: [router],
        mocks: {
          $router: {
            push
          }
        }
      }
    });

    // Simule un clic sur le bouton de nouvelle simulation
    await wrapper.find('button.btn-outline-primary').trigger('click');
    
    // Vérifie que la navigation a été déclenchée
    expect(push).toHaveBeenCalledWith('/simulation/new');
  });
});
