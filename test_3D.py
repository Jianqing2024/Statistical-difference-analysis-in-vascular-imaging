import numpy as np
import pyvista as pv

def cylindrical_to_cartesian_volume(data, r_max=3072, z_max=27000):
    """
    data: (Nr, Ntheta, Nz)
    r_max: 最大半径（物理尺寸，可设为1）
    z_scale: z方向缩放（用于校正比例）
    """
    Nr, Ntheta, Nz = data.shape

    # ===== 构建柱坐标 =====
    r = np.linspace(0, r_max, Nr)
    theta = np.linspace(0, 2*np.pi, Ntheta, endpoint=False)
    z = np.linspace(0, z_max, Nz)

    R, Theta, Z = np.meshgrid(r, theta, z, indexing='ij')

    # ===== 转换到笛卡尔 =====
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)

    return X, Y, Z


def show_volume_with_pyvista(data):
    """
    data: (Nr, Ntheta, Nz)
    """

    # ===== 坐标转换 =====
    X, Y, Z = cylindrical_to_cartesian_volume(data)

    # ===== 创建StructuredGrid =====
    grid = pv.StructuredGrid(X, Y, Z)

    # ⚠️ 注意：需要flatten（按Fortran顺序）
    grid["values"] = data.flatten(order="F")

    # ===== 可视化 =====
    plotter = pv.Plotter()

    plotter.add_volume(
        grid,
        scalars="values",
        cmap="hot",
        opacity="sigmoid",   # 很适合血管
        shade=True
    )

    plotter.add_axes()
    plotter.show_grid()

    plotter.show()

# ======================
# 示例调用
# ======================
if __name__ == "__main__":

    # 假数据（替换成你的）
    Nr, Ntheta, Nz = 100, 180, 200
    data = np.random.rand(Nr, Ntheta, Nz)

    # 模拟一个“血管样结构”
    data *= np.exp(-((np.linspace(0,1,Nr)[:,None,None]-0.5)**2)*20)

    show_volume_with_pyvista(data)