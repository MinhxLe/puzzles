import abc
import random
from dataclasses import dataclass, field
from typing import Optional


TRAVEL_TIME = 5
NUM_NODES = 50
NUM_PLANES = 10
NUM_STEPS = 10000


@dataclass
class Node:
    id: int


@dataclass
class Trip:
    id: int
    start: Node
    end: Node
    request_time: int
    real: bool
    start_time: int | None = None
    end_time: int | None = None
    assigned_plane: Optional["Plane"] = None

    def pending(self):
        return self.end_time is None


@dataclass
class Plane:
    curr_node: Node | None
    curr_trip: Trip | None = None


@dataclass
class Simulation(abc.ABC):
    nodes: list[Node]
    planes: list[Plane]
    trips: list[Trip] = field(default_factory=list)
    curr_time: int = 0

    def _next_trip_id(self) -> int:
        return 0 if not self.trips else self.trips[-1].id + 1

    def request_trip(self, start: Node, end: Node, real: bool):
        self.trips.append(Trip(self._next_trip_id(), start, end, self.curr_time, real))

    def assign_trip(self, trip: Trip, plane: Plane):
        assert trip.end_time is None
        assert plane.curr_node == trip.start
        plane.curr_node = None
        plane.curr_trip = trip

        trip.start_time = self.curr_time
        trip.end_time = self.curr_time + TRAVEL_TIME
        trip.assigned_plane = plane

    def complete_trip(self, trip: Trip):
        assert trip.end_time == self.curr_time
        assert trip.assigned_plane is not None
        plane = trip.assigned_plane
        plane.curr_node = trip.end
        plane.curr_trip = None

    def assign_trips(self):
        for trip in self.trips:
            if trip.end_time is None:
                for plane in self.planes:
                    if plane.curr_node == trip.start:
                        self.assign_trip(trip, plane)
                        break

    def complete_trips(self):
        for trip in self.trips:
            if trip.end_time == self.curr_time:
                self.complete_trip(trip)

    def simulate(self, steps: int):
        while self.curr_time < steps:
            self.request_trips()
            self.move_planes()
            self.assign_trips()
            self.complete_trips()
            self.curr_time += 1

    @abc.abstractmethod
    def request_trips(self): ...

    @abc.abstractmethod
    def move_planes(self): ...


class BasicSimulation(Simulation):
    def request_trips(self):
        self.request_trip(random.choice(nodes), random.choice(nodes), real=True)

    def move_planes(self):
        outstanding_trips = [t for t in self.trips if t.end_time is None]
        free_planes = [p for p in self.planes if p.curr_trip is None]
        for trip, plane in zip(outstanding_trips, free_planes):
            assert plane.curr_node is not None
            self.request_trip(plane.curr_node, trip.start, real=False)


nodes = [Node(i) for i in range(NUM_NODES)]
planes = [Plane(random.choice(nodes)) for _ in range(NUM_PLANES)]
simulation = BasicSimulation(nodes, planes)
simulation.simulate(NUM_STEPS)
