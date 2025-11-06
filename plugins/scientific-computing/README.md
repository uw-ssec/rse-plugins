# Scientific Computing Plugin

Agents and skills for high-performance computing, numerical methods, and computational science.

## Status

**Current Status:** Planned - Plugin structure in place, agents and skills coming soon

This plugin will provide specialized agents and skills for researchers and developers working with:
- High-performance computing (HPC) systems
- Numerical algorithms and computational methods
- Scientific simulations and modeling
- Parallel and distributed computing
- Performance optimization for scientific code

## Planned Focus Areas

### High-Performance Computing (HPC)

- **Parallel Computing**
  - MPI (Message Passing Interface) for distributed computing
  - OpenMP for shared-memory parallelism
  - GPU computing with CUDA and OpenCL
  - Hybrid CPU-GPU workflows

- **Job Scheduling and Resource Management**
  - SLURM, PBS, LSF job schedulers
  - Resource allocation and optimization
  - Queue management and priority scheduling
  - Batch job scripting and automation

- **Performance Optimization**
  - Profiling with Scalasca, TAU, Intel VTune, NVIDIA Nsight
  - Identifying bottlenecks and hotspots
  - Memory optimization and cache efficiency
  - Vectorization and compiler optimization

### Numerical Computing

- **Numerical Algorithms**
  - Linear algebra (direct and iterative solvers)
  - Optimization methods
  - Integration and differentiation
  - Root finding and equation solving

- **Scientific Libraries**
  - NumPy and SciPy for Python
  - BLAS/LAPACK for linear algebra
  - PETSc for parallel scientific computing
  - Julia scientific computing ecosystem

- **Numerical Stability**
  - Floating-point arithmetic considerations
  - Conditioning and error analysis
  - Precision management
  - Verification and validation

### Scientific Simulations

- **Simulation Methods**
  - Finite element methods (FEM)
  - Finite difference methods (FDM)
  - Monte Carlo simulations
  - Molecular dynamics
  - Computational fluid dynamics (CFD)

- **Workflow Management**
  - Multi-scale simulations
  - Uncertainty quantification
  - Parameter sweeps and sensitivity analysis
  - Data management for large simulations

### Computational Science Best Practices

- **Reproducibility**
  - Version control for computational code
  - Environment management and containerization
  - Workflow documentation
  - Data provenance tracking

- **Testing and Validation**
  - Unit testing for numerical code
  - Regression testing
  - Verification against analytical solutions
  - Code review for scientific accuracy

## Planned Technologies

### Languages
- Python (NumPy, SciPy, CuPy, Numba, Dask)
- C/C++ (MPI, OpenMP, CUDA)
- Fortran (legacy scientific code)
- Julia (modern scientific computing)
- MATLAB (prototyping and analysis)

### HPC Tools
- **Schedulers:** SLURM, PBS Pro, LSF, SGE
- **MPI Implementations:** OpenMPI, Intel MPI, MPICH
- **Compilers:** GCC, Intel, NVIDIA HPC SDK
- **Profilers:** Scalasca, TAU, Intel VTune, NVIDIA Nsight

### GPU Computing
- CUDA (NVIDIA GPUs)
- OpenCL (cross-platform GPUs)
- ROCm (AMD GPUs)
- cuPy (NumPy-compatible CUDA)
- JAX (composable transformations)

### Scientific Libraries
- NumPy, SciPy, Pandas
- MPI4Py (Python MPI bindings)
- Dask (parallel computing)
- PETSc (parallel solvers)
- Trilinos (solver frameworks)

## Example Use Cases

Once agents and skills are available, they will help with:

1. **Optimizing parallel algorithms** for HPC clusters
2. **Implementing numerical methods** with appropriate precision and stability
3. **Profiling and debugging** performance bottlenecks
4. **Designing scientific simulation** workflows
5. **Managing large-scale computations** across distributed systems
6. **Migrating code to GPU** for acceleration
7. **Setting up reproducible** computational environments
8. **Implementing best practices** for numerical software

## Contributing

We welcome contributions of agents and skills for scientific computing! If you have expertise in HPC, numerical methods, or computational science, please consider contributing.

See the main [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on creating agents and skills.

### Potential Agent Topics

Ideas for agents in this category:

- HPC Workflow Optimization Expert
- Parallel Computing Specialist (MPI, OpenMP)
- GPU Computing and CUDA Expert
- Numerical Methods Advisor
- Performance Profiling Specialist
- Scientific Simulation Designer
- Computational Reproducibility Expert

### Potential Skill Topics

Ideas for skills in this category:

- SLURM Job Scheduling Patterns
- MPI Programming Best Practices
- GPU Acceleration with CUDA
- Profiling Scientific Code
- Numerical Stability Techniques
- Finite Element Method Implementation
- Reproducible HPC Workflows

## Resources

### HPC Training
- [HPC Carpentry](https://www.hpc-carpentry.org/)
- [LLNL HPC Tutorials](https://hpc.llnl.gov/training)
- [ARCHER2 Training](https://www.archer2.ac.uk/training/)
- [XSEDE Training](https://www.xsede.org/for-users/training)

### Numerical Computing
- [Numerical Recipes](http://numerical.recipes/)
- [SciPy Lectures](https://lectures.scientific-python.org/)
- [Numerical Methods for Engineers](https://www.numerical.engineering/)

### Performance Optimization
- [Intel Optimization Guide](https://www.intel.com/content/www/us/en/developer/articles/guide/developer-guide-for-intel-oneapi-toolkits.html)
- [NVIDIA CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [OpenMP Programming Guide](https://www.openmp.org/)

### Related Plugins
- [Python Development Plugin](../python-development/) - For Scientific Python development

## Questions or Ideas?

If you have suggestions for agents or skills that should be included in this plugin, please open an issue on [GitHub](https://github.com/uw-ssec/rse-agents/issues) with the label `scientific-computing`.
