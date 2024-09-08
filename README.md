# EasySPC: Python Statistical Process Control Library

## Overview

**EasySPC** is a Python-based library designed to simplify the implementation of Statistical Process Control (SPC) in your quality management and process improvement efforts. This library provides tools for monitoring and controlling processes through statistical techniques, helping engineers, data scientists, and quality professionals ensure that processes operate at their full potential.

Statistical Process Control is a methodology for monitoring, controlling, and improving processes by identifying and controlling variations. By using EasySPC, you can quickly create control charts, perform process capability analysis, and detect trends or anomalies that could impact the quality of your products or services.

## Features

- **Control Charts:** Easily generate various control charts, including X-Bar, R, S, p, np, c, and u charts.
- **Process Capability Analysis:** Compute capability indices like Cp, Cpk, Pp, and Ppk to assess process performance against specification limits.
- **Outlier Detection:** Spot special cause variations and outliers using established statistical rules (e.g., Western Electric rules).
- **Data Integration:** Seamlessly integrate with pandas DataFrames for streamlined data handling and analysis.
- **Customizable:** Tailor control limits, sampling sizes, and statistical rules to meet the specific needs of your process.

## Installation

Install EasySPC via pip:

```bash
pip install -U easyspc
```

## Usage

Here is an example of how to use the EasySPC library:

```python
import pandas as pd
from easyspc import XBarChart, ProcessCapability

# Sample data
data = pd.DataFrame({
    'measurements': [23, 21, 22, 25, 24, 22, 23, 21, 24, 22]
})

# Create an X-Bar chart
xbar_chart = XBarChart(data['measurements'], subgroup_size=5)
xbar_chart.plot()

# Perform process capability analysis
process_capability = ProcessCapability(data['measurements'], specification_limits=(20, 26))
capability_indices = process_capability.calculate()
print(capability_indices)
```

## Advantages of Using Statistical Process Control (SPC)

1.	**Proactive Quality Management**: EasySPC helps detect process variations early, preventing defects and reducing waste.
2.	**Process Optimization**: Analyzing control charts allows you to fine-tune processes for better efficiency and quality.
3.	**Cost Reduction**: Reducing variation and preventing defects can significantly lower production costs, especially in high-volume environments.
4.	**Data-Driven Decisions**: EasySPC provides statistical insights for informed decision-making, reducing reliance on guesswork.
5.	**Compliance**: EasySPC supports quality control standards such as ISO and Six Sigma, making it easier to maintain compliance.

## Contributing

We welcome contributions! If you want to contribute to EasySPC, feel free to submit a pull request or open an issue.

## License

This project is licensed under the BSD-3 License - see the <LICENSE.md> file for details.
