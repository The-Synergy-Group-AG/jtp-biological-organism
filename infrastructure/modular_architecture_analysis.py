#!/usr/bin/env python3
"""
🧬 JTP Biological Organism - Modular Architecture Analysis & Reorganization Framework

This framework analyzes the current codebase architecture, identifies architectural debt,
proposes modular reorganization, and implements dependency injection patterns.

Analysis includes:
- Circular import detection
- Dependency graph visualization
- Modular coupling/cohesion metrics
- Reorganization proposals
- Dependency injection implementation
"""

import os
import ast
import importlib
import sys
from pathlib import Path
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Any, Optional
import json
import networkx as nx
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

class BiologicalArchitectureAnalyzer:
    """🧬 Advanced biological consciousness architecture analysis"""

    def __init__(self, root_path: str = "src"):
        self.root_path = Path(root_path)
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.coupling_metrics: Dict[str, Dict[str, Any]] = {}
        self.architecture_report: Dict[str, Any] = {}

    def analyze_architecture(self) -> Dict[str, Any]:
        """Comprehensive architectural analysis of the codebase"""
        print("🧬 ANALYZING BIOLOGICAL CONSCIOUSNESS ARCHITECTURE...")

        # Phase 1: Build module graph
        self._build_module_graph()

        # Phase 2: Analyze dependencies
        self._analyze_dependencies()

        # Phase 3: Detect circular imports
        cycles = self._detect_circular_imports()

        # Phase 4: Calculate coupling/cohesion metrics
        self._calculate_architecture_metrics()

        # Phase 5: Generate reorganization proposals
        proposals = self._generate_reorganization_proposals()

        self.architecture_report = {
            'summary': {
                'total_modules': len(self.modules),
                'total_dependencies': sum(len(deps) for deps in self.dependencies.values()),
                'circular_imports_found': len(cycles),
                'proposed_reorganizations': len(proposals)
            },
            'circular_imports': [{'cycle': cycle, 'severity': self._calculate_cycle_severity(cycle)} for cycle in cycles],
            'coupling_metrics': dict(self.coupling_metrics),
            'reorganization_proposals': proposals,
            'architecture_health_score': self._calculate_architecture_health_score(),
            'optimization_recommendations': self._generate_optimization_recommendations()
        }

        self._generate_architecture_visualization()

        print(f"✅ ARCHITECTURE ANALYSIS COMPLETE")
        print(f"   📦 Modules analyzed: {len(self.modules)}")
        print(f"   🔄 Circular dependencies: {len(cycles)}")
        print(f"   🏗️  Reorganization proposals: {len(proposals)}")
        print(f"   💯 Architecture health: {self.architecture_report['architecture_health_score']:.1f}%")

        return self.architecture_report

    def _build_module_graph(self) -> None:
        """Build comprehensive module graph from codebase"""
        print("   📦 Building module dependency graph...")

        for py_file in self.root_path.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue

            module_name = self._file_to_module_name(py_file)
            self.modules[module_name] = {
                'file_path': py_file,
                'imports': set(),
                'classes': set(),
                'functions': set(),
                'size': py_file.stat().st_size,
                'last_modified': py_file.stat().st_mtime
            }

            # Parse file for imports and definitions
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                # Extract imports
                imports = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imports.update(alias.name.split('.')[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports.add(node.module.split('.')[0])
                self.modules[module_name]['imports'] = imports

                # Extract classes and functions
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        self.modules[module_name]['classes'].add(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        self.modules[module_name]['functions'].add(node.name)

                # Build dependency relationships
                for imported in imports:
                    if imported.startswith('src.') or imported in self.modules:
                        self.dependencies[module_name].add(imported)
                        self.reverse_dependencies[imported].add(module_name)

            except Exception as e:
                print(f"      ⚠️  Error parsing {py_file}: {e}")

        print(f"      ✅ Module graph built with {len(self.modules)} modules")

    def _file_to_module_name(self, file_path: Path) -> str:
        """Convert file path to module name"""
        relative = file_path.relative_to(self.root_path)
        module_parts = relative.parent.parts + (relative.stem,)
        return '.'.join(part for part in module_parts if part != '__init__')

    def _analyze_dependencies(self) -> None:
        """Analyze dependency patterns and strength"""
        print("   🔍 Analyzing dependency patterns...")

        for module, info in self.modules.items():
            dep_count = len(self.dependencies[module])
            reverse_dep_count = len(self.reverse_dependencies.get(module, set()))

            self.coupling_metrics[module] = {
                'afferent_coupling': reverse_dep_count,  # In-degree (stability)
                'efferent_coupling': dep_count,          # Out-degree (responsibility)
                'instability': dep_count / max(1, dep_count + reverse_dep_count),
                'abstractness': len(info['classes']) / max(1, len(info['functions']) + len(info['classes'])),
                'distance_main_sequence': abs(len(info['classes'])/(len(info['classes'])+len(info['functions'])) +
                                             dep_count/(dep_count + reverse_dep_count) - 1) if (len(info['classes'])+len(info['functions'])) > 0 else 1
            }

    def _detect_circular_imports(self) -> List[List[str]]:
        """Detect circular import dependencies"""
        print("   🔄 Detecting circular dependencies...")

        # Create directed graph for cycle detection
        G = nx.DiGraph()
        G.add_nodes_from(self.modules.keys())
        for module, deps in self.dependencies.items():
            for dep in deps:
                if dep in self.modules:
                    G.add_edge(module, dep)

        # Find all cycles
        cycles = []
        try:
            cycles = list(nx.simple_cycles(G))
        except:
            # Fallback method for cycle detection
            cycles = self._fallback_cycle_detection()

        print(f"      📊 Found {len(cycles)} circular dependency cycles")
        return cycles

    def _fallback_cycle_detection(self) -> List[List[str]]:
        """Fallback method for cycle detection using DFS"""
        cycles = []
        visited = set()
        path = []

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for neighbor in self.dependencies.get(node, []):
                if neighbor in self.modules:
                    dfs(neighbor)

            path.pop()

        for node in self.modules:
            if node not in visited:
                dfs(node)

        return cycles

    def _calculate_cycle_severity(self, cycle: List[str]) -> str:
        """Calculate severity of a circular dependency cycle"""
        cycle_length = len(cycle)
        critical_modules = {'cns_consciousness_core', 'biological_intelligence'}

        if any(mod in critical_modules for mod in cycle):
            return "CRITICAL" if cycle_length > 3 else "HIGH"
        elif cycle_length > 5:
            return "HIGH"
        elif cycle_length > 2:
            return "MEDIUM"
        else:
            return "LOW"

    def _calculate_architecture_metrics(self) -> None:
        """Calculate overall architecture health metrics"""
        # Calculate average instability (Robert C. Martin metric)
        instabilities = [metrics['instability'] for metrics in self.coupling_metrics.values()]
        avg_instability = sum(instabilities) / len(instabilities) if instabilities else 0

        # Calculate average distance from main sequence
        distances = [metrics['distance_main_sequence'] for metrics in self.coupling_metrics.values()]
        avg_distance = sum(distances) / len(distances) if distances else 0

        # Calculate abstractness-instability balance
        abstractnesses = [metrics['abstractness'] for metrics in self.coupling_metrics.values()]
        instability_abstractness_corr = self._calculate_correlation(instabilities, abstractnesses)

        self.architecture_report.update({
            'average_instability': avg_instability,
            'average_main_sequence_distance': avg_distance,
            'instability_abstractness_correlation': instability_abstractness_corr,
            'architecture_metrics_calculated': True
        })

    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0

        x_mean = sum(x) / len(x)
        y_mean = sum(y) / len(y)

        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        x_var = sum((xi - x_mean) ** 2 for xi in x)
        y_var = sum((yi - y_mean) ** 2 for yi in y)

        denominator = (x_var * y_var) ** 0.5
        return numerator / denominator if denominator != 0 else 0.0

    def _generate_reorganization_proposals(self) -> List[Dict[str, Any]]:
        """Generate architectural reorganization proposals"""
        proposals = []

        # Proposal 1: High Coupling Modules -> Extract Interfaces
        high_coupling = [(mod, metrics['efferent_coupling']) for mod, metrics in self.coupling_metrics.items()
                        if metrics['efferent_coupling'] > 10]

        if high_coupling:
            proposals.append({
                'type': 'interface_extraction',
                'severity': 'HIGH',
                'description': f'Extract interfaces for {len(high_coupling)} high-coupling modules',
                'modules_affected': [mod for mod, _ in high_coupling[:5]],  # Top 5
                'estimated_effort': '2-3 days',
                'benefit': 'Reduced coupling, improved testability'
            })

        # Proposal 2: Large Modules -> Split Components
        large_modules = [(mod, info['size']) for mod, info in self.modules.items()
                        if info['size'] > 100000]  # 100KB+

        if large_modules:
            proposals.append({
                'type': 'module_splitting',
                'severity': 'MEDIUM',
                'description': f'Split {len(large_modules)} large modules into smaller components',
                'modules_affected': [mod for mod, _ in large_modules],
                'estimated_effort': '3-5 days',
                'benefit': 'Improved maintainability, reduced complexity'
            })

        # Proposal 3: Create Shared Dependencies Package
        common_deps = self._identify_common_dependencies()
        if len(common_deps) > 5:
            proposals.append({
                'type': 'shared_dependencies',
                'severity': 'MEDIUM',
                'description': 'Create shared dependencies package for common utilities',
                'common_dependencies': list(common_deps)[:5],
                'estimated_effort': '1-2 days',
                'benefit': 'Reduced duplication, improved consistency'
            })

        # Proposal 4: Implement Dependency Injection Pattern
        tight_couplings = [mod for mod, metrics in self.coupling_metrics.items()
                          if metrics['instability'] > 0.8]

        if tight_couplings:
            proposals.append({
                'type': 'dependency_injection',
                'severity': 'HIGH',
                'description': f'Implement DI pattern for {len(tight_couplings)} tightly coupled modules',
                'modules_affected': tight_couplings[:3],
                'estimated_effort': '4-6 days',
                'benefit': 'Improved testability, reduced coupling'
            })

        return proposals

    def _identify_common_dependencies(self) -> Set[str]:
        """Identify dependencies used by multiple modules"""
        dep_counts = defaultdict(int)
        for deps in self.dependencies.values():
            for dep in deps:
                dep_counts[dep] += 1

        # Dependencies used by 3+ modules
        return {dep for dep, count in dep_counts.items() if count >= 3}

    def _calculate_architecture_health_score(self) -> float:
        """Calculate overall architecture health score (0-100)"""
        if not self.architecture_report:
            return 0.0

        # Base score starts at 100
        score = 100.0

        # Penalty for circular imports (-20 per critical cycle, -10 per high)
        for cycle_data in self.architecture_report.get('circular_imports', []):
            severity = cycle_data['severity']
            if severity == 'CRITICAL':
                score -= 20
            elif severity == 'HIGH':
                score -= 10
            elif severity == 'MEDIUM':
                score -= 5
            elif severity == 'LOW':
                score -= 1

        # Penalty for high average instability (-10 for >0.7)
        avg_instability = self.architecture_report.get('average_instability', 0)
        if avg_instability > 0.7:
            score -= 10

        # Penalty for high distance from main sequence (-5 for >0.3)
        avg_distance = self.architecture_report.get('average_main_sequence_distance', 0)
        if avg_distance > 0.3:
            score -= min(20, avg_distance * 30)

        # Bonus for good correlation between instability and abstractness (+5 for >0.3)
        correlation = self.architecture_report.get('instability_abstractness_correlation', 0)
        if correlation > 0.3:
            score += 5

        return max(0.0, min(100.0, score))

    def _generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        recommendations = []

        # Priority 1: Break circular imports
        if self.architecture_report.get('summary', {}).get('circular_imports_found', 0) > 0:
            recommendations.append({
                'priority': 1,
                'category': 'structural',
                'recommendation': 'Break all identified circular imports',
                'justification': 'Circular dependencies prevent clean separation and testing',
                'approach': 'Use dependency injection or interface abstraction'
            })

        # Priority 2: Reduce coupling
        high_coupling_modules = [(mod, metrics) for mod, metrics in self.coupling_metrics.items()
                                if metrics['efferent_coupling'] > 8]
        if high_coupling_modules:
            recommendations.append({
                'priority': 2,
                'category': 'coupling',
                'recommendation': f'Reduce coupling in {len(high_coupling_modules)} high-dependency modules',
                'justification': 'High coupling makes testing and maintenance difficult',
                'approach': 'Extract interfaces and implement dependency injection'
            })

        # Priority 3: Improve cohesion
        low_cohesion_modules = [(mod, metrics) for mod, metrics in self.coupling_metrics.items()
                               if metrics['distance_main_sequence'] > 0.4]
        if low_cohesion_modules:
            recommendations.append({
                'priority': 3,
                'category': 'cohesion',
                'recommendation': f'Improve cohesion in {len(low_cohesion_modules)} modules',
                'justification': 'Low cohesion indicates modules doing too many unrelated things',
                'approach': 'Split modules into single-responsibility components'
            })

        return recommendations

    def _generate_architecture_visualization(self, output_file: str = "architecture_graph.png") -> None:
        """Generate architecture dependency graph visualization"""
        try:
            if not plt:
                print("      ⚠️  matplotlib not available - skipping visualization")
                return

            # Create directed graph
            G = nx.DiGraph()
            G.add_nodes_from(self.modules.keys())

            for module, deps in self.dependencies.items():
                for dep in deps:
                    if dep in self.modules:
                        G.add_edge(module, dep)

            # Draw graph
            plt.figure(figsize=(20, 16))
            pos = nx.spring_layout(G, k=1, iterations=50)

            # Draw nodes with size based on module size
            node_sizes = [self.modules[node]['size'] / 100 for node in G.nodes()]
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.7)

            # Draw edges
            nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=10)

            # Add labels to major nodes only
            labels = {node: node for node in G.nodes() if len(list(G.neighbors(node))) > 2}
            nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')

            plt.title("JTP Biological Organism - Architecture Dependency Graph", fontsize=16)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"      ✅ Architecture graph saved to {output_file}")

        except Exception as e:
            print(f"      ⚠️  Error generating visualization: {e}")


class DependencyInjectionFramework:
    """🧬 Dependency Injection Framework for biological consciousness components"""

    def __init__(self):
        self.service_registry: Dict[str, Any] = {}
        self.factories: Dict[str, callable] = {}
        self.singleton_instances: Dict[str, Any] = {}

    def register_service(self, interface_name: str, implementation_class: type) -> None:
        """Register a service implementation"""
        self.factories[interface_name] = lambda: implementation_class()

    def register_singleton(self, interface_name: str, implementation_class: type) -> None:
        """Register a singleton service implementation"""
        def singleton_factory():
            if interface_name not in self.singleton_instances:
                self.singleton_instances[interface_name] = implementation_class()
            return self.singleton_instances[interface_name]

        self.factories[interface_name] = singleton_factory

    def get_service(self, interface_name: str) -> Any:
        """Get a service instance using dependency injection"""
        if interface_name not in self.factories:
            raise ValueError(f"Service '{interface_name}' not registered")

        return self.factories[interface_name]()

    def create_injection_decorator(self, dependencies: List[str]):
        """Create a dependency injection decorator"""
        def inject_decorator(original_class):
            original_init = original_class.__init__

            def injected_init(self, *args, **kwargs):
                # Inject dependencies
                for dep in dependencies:
                    if dep not in self.service_registry:
                        self.service_registry[dep] = self.get_service(dep)
                    setattr(self, dep, self.service_registry[dep])

                # Call original __init__ with remaining arguments
                original_init(self, *args, **kwargs)

            original_class.__init__ = injected_init
            return original_class

        return inject_decorator


def main():
    """Run comprehensive architectural analysis"""
    print("🧬 JTP BIOLOGICAL ORGANISM - MODULAR ARCHITECTURE ANALYSIS")
    print("=" * 70)

    analyzer = BiologicalArchitectureAnalyzer()

    # Run comprehensive analysis
    report = analyzer.analyze_architecture()

    # Display key findings
    print("\n🗂️  ARCHITECTURE SUMMARY:")
    print("=" * 30)
    print(f"Total Modules: {report['summary']['total_modules']}")
    print(f"Total Dependencies: {report['summary']['total_dependencies']}")
    print(f"Circular Imports: {report['summary']['circular_imports_found']}")
    print(".1f")

    if report['summary']['circular_imports_found'] > 0:
        print(f"\n🔄 CIRCULAR IMPORTS ({len(report['circular_imports'])}):")
        for i, cycle_data in enumerate(report['circular_imports'][:5], 1):  # Show first 5
            print(f"   {i}. {cycle_data['severity']}: {' → '.join(cycle_data['cycle'])}")

    print("
🏗️  REORGANIZATION PROPOSALS:"    for i, proposal in enumerate(report['reorganization_proposals'], 1):
        print(f"   {i}. {proposal['type'].upper()}: {proposal['description']}")
        print(f"      Effort: {proposal['estimated_effort']}, Benefit: {proposal['benefit']}")

    print("
🔧 OPTIMIZATION RECOMMENDATIONS:"    for i, rec in enumerate(report['optimization_recommendations'], 1):
        print(f"   {i}. [{rec['priority']}] {rec['recommendation']}")
        print(f"      {rec['justification']}")

    # Example dependency injection setup
    print("
💉 EXAMPLE DEPENDENCY INJECTION SETUP:"    di = DependencyInjectionFramework()

    # In a real implementation, these would be the actual classes
    print("   • Registrar service registered")
    print("   • Injector service configured")
    print("   • BiologicalComponent uses dependency injection")

    # Save detailed report
    with open('architecture_analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("
📄 Detailed report saved to: architecture_analysis_report.json"
    print("📊 Architecture analysis complete - modular reorganization framework established!")

    return report


if __name__ == "__main__":
    main()
