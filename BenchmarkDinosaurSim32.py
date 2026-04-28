# Benchmark for the 32x32 dinosaur harvester simulation.

sim_unlocks = Unlocks
sim_items = {
	Items.Cactus: 2000,
	Items.Fertilizer: 2000,
}
sim_globals = {}
seed = 1
speedup = 64

run_time = simulate("DinosaurBoneHarvesterSim32", sim_unlocks, sim_items, sim_globals, seed, speedup)
print("Dinosaur 32x32 simulation time:", run_time)
