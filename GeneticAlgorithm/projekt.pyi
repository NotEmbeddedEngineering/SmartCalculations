"""Kontenery, grupa 6. Deklaracje klas do wspólnej implementacji."""

from dataclasses import dataclass
from enum import Enum


class ModuleType(Enum):
    EMPTY = 0       # Wolne pole: przejście lub plac.
    LIVING = 1      # Moduł mieszkalny.
    KITCHEN = 2
    SANITARY = 3
    COMMON = 4


class DoorSide(Enum):
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


@dataclass
class Cell:
    """Jedno pole planszy. Puste pole ma NONE, kontener ma jedną stronę drzwi."""

    module_type: ModuleType
    door: DoorSide = DoorSide.NONE


@dataclass
class SimulationConfig:
    """Wymiary planszy, minimalny udział wolnych pól i liczba mieszkań na moduł usługowy."""

    rows: int
    cols: int
    min_empty_ratio: float = 0.25
    max_living_per_kitchen: int = 8
    max_living_per_sanitary: int = 6
    max_living_per_common: int = 12


class LayoutIndividual:
    """Jedna propozycja osiedla. grid[wiersz][kolumna] opisuje jedno pole."""

    grid: list[list[Cell]]
    fitness: float

    def __init__(self, grid: list[list[Cell]]) -> None: ...
    def clone(self) -> "LayoutIndividual":
        """Kopiuje planszę razem z komórkami, aby mutacja kopii nie zmieniała rodzica."""
        ...


class FitnessEvaluator:
    """Ocenia liczbę mieszkań, przejścia, odległości i dostępność usług."""

    config: SimulationConfig

    def __init__(self, config: SimulationConfig) -> None: ...
    def evaluate(self, individual: LayoutIndividual) -> float:
        """Zwraca ocenę układu. Większa wartość oznacza lepszy wynik."""
        ...

    def _count_modules(self, grid: list[list[Cell]], target: ModuleType) -> int: ...
    def _count_blocked_doors(self, grid: list[list[Cell]]) -> int:
        """Liczy drzwi skierowane poza planszę albo na zajęte pole."""
        ...

    def _is_fully_accessible_bfs(self, grid: list[list[Cell]]) -> bool:
        """Sprawdza, czy pola przed wszystkimi drzwiami łączy jedna sieć przejść w czterech kierunkach."""
        ...

    def _calculate_avg_distance_to_amenities(self, grid: list[list[Cell]]) -> float:
        """Dla każdego mieszkania mierzy dojście do najbliższej usługi każdego z trzech typów i uśrednia wyniki."""
        ...

    def _calculate_infrastructure_penalties(self, grid: list[list[Cell]]) -> float:
        """Wyznacza karę za niedobór usług względem liczby mieszkań i za zbyt mało wolnego terenu."""
        ...


class GeneticOperators:
    """Tworzy osobniki, wybiera rodziców i modyfikuje plansze potomków."""

    config: SimulationConfig

    def __init__(self, config: SimulationConfig) -> None: ...
    def generate_random_individual(self) -> LayoutIndividual: ...
    def tournament_selection(
        self, population: list[LayoutIndividual], tournament_size: int
    ) -> LayoutIndividual:
        """Losuje uczestników turnieju i zwraca osobnika o najwyższym fitness."""
        ...

    def crossover_2d_block(
        self, parent_a: LayoutIndividual, parent_b: LayoutIndividual
    ) -> tuple[LayoutIndividual, LayoutIndividual]:
        """Tworzy dwoje potomków przez wymianę prostokątnego fragmentu między kopiami rodziców."""
        ...

    def mutate(self, individual: LayoutIndividual, mutation_rate: float) -> None:
        """Z podanym prawdopodobieństwem wykonuje jedną z trzech mutacji bezpośrednio na potomku."""
        ...

    def _mutate_swap_cells(self, grid: list[list[Cell]]) -> None: ...
    def _mutate_change_type(self, grid: list[list[Cell]]) -> None:
        """Zmienia typ pola i dopasowuje drzwi, również przy dodaniu lub usunięciu kontenera."""
        ...

    def _mutate_rotate_door(self, grid: list[list[Cell]]) -> None: ...


class GeneticSolver:
    """Prowadzi ewolucję populacji i zapisuje zwrócone oceny w polu fitness osobników."""

    evaluator: FitnessEvaluator
    operators: GeneticOperators

    def __init__(self, evaluator: FitnessEvaluator, operators: GeneticOperators) -> None: ...
    def run(
        self,
        generations: int,
        population_size: int,
        elitism_count: int,
        mutation_rate: float,
    ) -> LayoutIndividual:
        """Zachowuje elitę, uzupełnia pokolenie potomstwem i na końcu zwraca najlepszy układ."""
        ...


class LayoutVisualizer:
    """Rysuje kolorowe moduły, oznaczenia drzwi, wolne przejścia i legendę."""

    def render(self, individual: LayoutIndividual, output_file: str | None = None) -> None:
        """Wyświetla plan lub zapisuje go do pliku, gdy podano ścieżkę."""
        ...
