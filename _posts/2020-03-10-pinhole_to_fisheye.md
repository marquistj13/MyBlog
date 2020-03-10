---
layout: post
title: 如何将 pinhole 相机的图像转化为 fisheye 相机的图像
categories:  [编程]
tag: [openMVG]
---

* content
{:toc}


## 前言
camera 由两部分组成：
1. Geometry，镜头（lens）：也就是用来改变光路的，光线到达镜头以后发生折射，最后才到达“底片”。 Geometry 就是论文和书里面 相机模型（`camera model`) 要 model 的东西。
2. sensor：也就是用来测量“亮度”的。

pinhole 相机和 fisheye 相机的区别可以认为只有 Geometry 的区别， 因此如果要将 pinhole 相机的图像转化为 fisheye 相机的图像，只需要从 `相机模型` 的角度进行操作即可。
因此问题就转化为：
1. 给定一个  pinhole 相机的图像（`源图像`）， 如何确定变换后（也就是失真后）的鱼眼相机的图像（`目标图像`）的尺寸 (`shape`)。
2. 我们如何确定目标图像中的每一个像素点对应于源图像中的哪一个点。

## 转换过程分析
结合代码来解决的话，思路会更清晰一些。
### openMVG 的安装和使用
由于 opencv 源码和文档较为复杂，不适合我进行利用，因此决定使用另一个较为轻量级的 Multiple View Geometry 库：[OpenMVG (open Multiple View Geometry)](https://github.com/openMVG/openMVG)。

这个库的信条是： "Keep it simple, keep it maintainable".
1. OpenMVG is designed to be easy to read, learn, modify and use.
2. Thanks to its strict test-driven development and samples, the library allows to build trusted larger systems.

事实的确如此，其源码非常容易理解。
由于这个库包含了很多第三方库，例如ceres，因此官方建议不要将 openMVG 装在系统路径，而是安装在home的某个路径。
根据 [Using OpenMVG as a third party library dependency with CMake](https://github.com/openMVG/openMVG/blob/develop/BUILD.md#using-openmvg-as-a-third-party-library-dependency-with-cmake)进行安装即可。

下面说一下我的安装流程。
按照上面的链接先安装依赖库并下载源码，然后在openMVG的同级目录建立build 目录。
```sh
git clone --recursive https://github.com/openMVG/openMVG.git
mkdir -p openMVG_Build/openMVG_instal
```
配置和编译：
```sh
cmake -DCMAKE_BUILD_TYPE=RELEASE ../openMVG/src/ -DCMAKE_INSTALL_PREFIX:STRING="/home/marquis/github/openMVG_Build/openMVG_install"
make -j4
make install
```

好了，怎么去使用这个库呢？现在的cmake支持 `modern target-based approach`，因此，还需要指定：
```cmake
set(OpenMVG_DIR "/home/ssd/openMVG_Build/openMVG_install/share/openMVG/cmake")
find_package(OpenMVG REQUIRED)

add_executable(convertFisheye  main.cpp)

target_link_libraries(convertFisheye
  PRIVATE 
  OpenMVG::openMVG_camera
  OpenMVG::openMVG_exif
  OpenMVG::openMVG_features
  OpenMVG::openMVG_geodesy
  OpenMVG::openMVG_geometry
  OpenMVG::openMVG_graph
  OpenMVG::openMVG_image
  OpenMVG::openMVG_linearProgramming
  OpenMVG::openMVG_matching
  OpenMVG::openMVG_matching_image_collection
  OpenMVG::openMVG_multiview
  OpenMVG::openMVG_numeric
  OpenMVG::openMVG_robust_estimation
  OpenMVG::openMVG_sfm
  OpenMVG::openMVG_system
  )
```
就行了，注意，这里不要使用 `include_directories(${OpenMVG_INCLUDE_DIRS})` 了，事实上，`OpenMVG_INCLUDE_DIRS` 这个 cmake 变量是空的。
只要你在 `target_link_libraries` 中指定了要链接的库，如 `OpenMVG::openMVG_camera` 那么，你的cmake 就能找到 `camera` 库对应的头文件。
这里为了方便，几乎吧所有子库都加进来了，官方貌似不推荐哈哈。

### 从代码的角度分析转换过程
首先来看针孔相机的两个重要函数(`Camera_Pinhole.hpp`)：
```c++
    /**
    * @brief Transform a point from the camera plane to the image plane
    * @param p Camera plane point
    * @return Point on image plane
    */
    Vec2 cam2ima( const Vec2& p ) const override
    {
      return focal() * p + principal_point();
    }

    /**
    * @brief Transform a point from the image plane to the camera plane
    * @param p Image plane point
    * @return camera plane point
    */
    Vec2 ima2cam( const Vec2& p ) const override
    {
      return ( p -  principal_point() ) / focal();
    }

```
这里 `cam2ima` 将 camera plane 的点转化到  image plane， `ima2cam` 是其反函数。
很明显，camera plane 的点是已经归一化后的 2d 点。例如，对于一个 3d 点 `Vec3 X`， 以及 一个 `3x4`的外参矩阵 `[R|t]`，这个2d点就是：`Vec3([R|t] * X.homogeneous()).hnormalized()`。 注意这个是伪代码哈，实际用的时候，将 `[R|t]` 用一个变量表示就行了（具体代码请参考`projection.hpp` 和  `projection.cpp`）。

然后再看一下鱼眼相机的两个重要函数(`Camera_Pinhole_Fisheye.hpp`)：
```c++
 /**
    * @brief Return the un-distorted pixel (with removed distortion)
    * @param p Input distorted pixel
    * @return Point without distortion
    */
    Vec2 get_ud_pixel( const Vec2& p ) const override
    {
      return cam2ima( remove_disto( ima2cam( p ) ) );
    }

    /**
    * @brief Return the distorted pixel (with added distortion)
    * @param p Input pixel
    * @return Distorted pixel
    */
    Vec2 get_d_pixel( const Vec2& p ) const override
    {
      return cam2ima( add_disto( ima2cam( p ) ) );
    }
```
这里的 `cam2ima` 和 `ima2cam` 和上面针孔相机的是一样的。
现在分析两个重要的过程：
1. `remove_disto( ima2cam( p ) )` 就是给定鱼眼相机图像上的一个像素点`p`，找到对应的 camera plane 上的 2d 点，然后再 `remove_disto`，此时 这个 2d 点还在 camera plane 上。
2. `add_disto( ima2cam( p ) )` 就是给定鱼眼相机图像上的一个像素点`p`，找到对应的 camera plane 上的 2d 点，然后再 `add_disto`，此时 这个 2d 点还在 camera plane 上。

这俩过程的区别就是：到底我们是将 camera plane 上的 2d 点 进行 `去失真` 还是 `加失真`。

到这里，前言里提到的两个问题的答案就有了眉目。
>1. 给定一个  pinhole 相机的图像（`源图像`）， 如何确定变换后（也就是失真后）的鱼眼相机的图像（`目标图像`）的尺寸 (`shape`)。
2. 我们如何确定目标图像中的每一个像素点对应于源图像中的哪一个点。

假设我们新建一个 `class Pinhole2Fisheye` 它继承了 `class Pinhole_Intrinsic_Fisheye`用来表示目标图像的内参，并且有一个成员变量 `Pinhole_Intrinsic ori_pinhole_cam;`来表示源图像的内参。
1. 将源图像中的每一个像素点坐标，先`ori_pinhole_cam.ima2cam( p )`到camera plane，然后在camera plane上进行`add_disto`，最后再用目标图像的内参变换到像素坐标系就能的到目标图像的shape了，也就是：`cam2ima( add_disto( ori_pinhole_cam.ima2cam( p ) ) );`
2. 已知目标图像的尺寸，对于其每一个像素点坐标，先用鱼眼相机内参转换到camera plane，然后在camera plane上进行`remove_disto`，最后用源图像的内参变换到像素坐标系，就得到了源图像上的对应的坐标，亦即：`cam2ima( add_disto( ori_pinhole_cam.ima2cam( p ) ) );`

具体代码可借鉴 `Camera_undistort_image.hpp`。我修改后的代码如下：
```c++
/**
   * @brief Get Sampling Grid, and get the right fisheye picture shape
   * @sampling_grid  the result sampling grid
   * @fisheye_w the result fisheye picture width
   * @fisheye_h the result  fisheye picture height
   */
  bool getSamplingGrid(std::vector<std::pair<float,float>>& sampling_grid, int& fisheye_w, int& fisheye_h){
    // 1 - Compute size of the distorted image
    int min_x = std::numeric_limits<int>::max();//x: width index
    int min_y = std::numeric_limits<int>::max();//y: height index
    int max_x = std::numeric_limits<int>::lowest();
    int max_y = std::numeric_limits<int>::lowest();
#ifdef USE_OPENMP
#pragma omp parallel for
#endif
    for(int j=0; j<ori_pinhole_cam.h(); ++j){//height index
      for(int i=0; i<ori_pinhole_cam.w(); ++i){//width index
        const Vec2 undist_pix = get_d_pixel_extended(Vec2(i, j));//(column, row),(width, height)
        const int x_ori = static_cast<int>( undist_pix[0] );
        const int y_ori = static_cast<int>( undist_pix[1] );
        min_x = std::min( x_ori , min_x );
        min_y = std::min( y_ori , min_y );
        max_x = std::max( x_ori , max_x );
        max_y = std::max( y_ori , max_y );
      }
    }

    // Ensure size is at least 1 pixel (width and height)
    const int computed_size_x = std::max( 1 , max_x - min_x + 1 );
    const int computed_size_y = std::max( 1 , max_y - min_y + 1 );

    // Compute real size (ensure we do not have infinite size)
    const uint32_t real_size_x = std::min( ori_pinhole_cam.w() , (uint32_t)computed_size_x );
    const uint32_t real_size_y = std::min( ori_pinhole_cam.h() , (uint32_t)computed_size_y );

    //std::cout<<"real x"<<real_size_x<<" , real y"<<real_size_y<<std::endl;
    // 2. update cam params
    w_ = real_size_x;
    h_ = real_size_y;
    fisheye_w = real_size_x;
    fisheye_h = real_size_y;

    // // if we do not update the ppx and ppy of the fisheye parameter, we should use min_x and min_y in the computation
    // // 3. Compute sampling grid
    // sampling_grid.clear();
    // sampling_grid.reserve(real_size_x * real_size_y);
    // for ( int j = 0; j < real_size_y; ++j ){
    //   for ( int i = 0; i < real_size_x; ++i ){
    //     // compute coordinates without distortion
    //     const Vec2 undist_pix = get_ud_pixel_extended(Vec2(i + min_x, j + min_y));//(column, row),(width, height)
    //     sampling_grid.emplace_back(undist_pix[1], undist_pix[0]);//(row, column)
    //   }
    // }

    K_(0,2) = w_/2;
    K_(1,2) = h_/2;
    // if we update the ppx and ppy, we should not use min_x and min_y in the computation
    // 3. Compute sampling grid
    sampling_grid.clear();
    sampling_grid.reserve(real_size_x * real_size_y);
    for ( int j = 0; j < real_size_y; ++j ){
      for ( int i = 0; i < real_size_x; ++i ){
        // compute coordinates without distortion
        const Vec2 undist_pix = get_ud_pixel_extended(Vec2(i, j));//(column, row),(width, height)
        sampling_grid.emplace_back(undist_pix[1], undist_pix[0]);//(row, column)
      }
    }

    return true;
  }
  /**
   * @brief Return the un-distorted pixel (with removed distortion), note that we use a pinhole camera to project the camera coordinates into the image pixels
   * @param p Input distorted pixel
   * @return Point without distortion
   */
  Vec2 get_ud_pixel_extended( const Vec2& p ) const
  {
    return ori_pinhole_cam.cam2ima( remove_disto( ima2cam( p ) ) );
  }

  /**
   * @brief Return the distorted pixel (with removed distortion), note that we use a pinhole camera to project the pixels into the camera coordinates
   * @param p Input distorted pixel
   * @return Point with distortion
   */
  Vec2 get_d_pixel_extended( const Vec2& p ) const
  {
    return cam2ima( add_disto( ori_pinhole_cam.ima2cam( p ) ) );
  }
```

## 实现过程中的其他技巧
### enum class 的正确用法
一开始我一直纠结enum class该怎么用在 `std::vector` 中，后来搜索发现，`std::vector` 不是这么用的，因此我就将其用在了`std::map`中，让 enum class 作为key来使用。
```c++ 
  enum class HybridCam{
                     PINHOLE_WIDTH=0,
                     PINHOLE_HEIGHT,
                     PINHOLE_FOCAL_LENGTH,
                     PINHOLE_PPX,
                     PINHOLE_PPY,
                     FISHEYE_W,
                     FISHEYE_H,
                     FISHEYE_FOCAL,
                     FISHEYE_PPX,
                     FISHEYE_PPY,
                     FISHEYE_K1,
                     FISHEYE_K2,
                     FISHEYE_K3,
                     FISHEYE_K4
};
std::map<HybridCam, double> params；
```
### 设计模式之 Pototype
参考自：[Prototype in C++: Before and after](https://sourcemaking.com/design_patterns/prototype/cpp/1)

在实现上面的转换代码的过程中，我需要判断是使用hard-coded 相机模型参数，还是加载存在文件中的相机模型参数文件。
这时候我们就可以先建立一个指针 `Pinhole2Fisheye *cam_ptr;`，如果是使用hard-coded 相机模型参数，也就是写在code中的参数，就很好办了，直接`cam_ptr = new Pinhole2Fisheye(cam_params);` 就行了。
如果是加载模型文件，也就是`cam_ptr->load(archive);`，我们就得先实例化指针`cam_ptr`，也就是一般我们的类`Pinhole2Fisheye`得有一个不带参数的构造函数，或者全是默认参数的构造函数。
如果我们不想这样呢？
就可以使用Prototype。根据以上参考链接，只需要实现一个 `clone`方法就行了。

实际上，我们的基类的基类就默认继承了这么一个抽象基类，即`Clonable`,(详见：`Camera_Intrinsics.hpp`)：
```c++
/**
* @brief Struct used to force "clonability"
*/
template<typename T>
struct Clonable
{
  virtual T * clone() const = 0;
};

/**
* @brief Base class used to store common intrinsics parameters
*/
struct IntrinsicBase : public Clonable<IntrinsicBase>
{
  /// Width of image
  unsigned int w_;
  /// Height of image
  unsigned int h_;
```

因此我们实现的时候需要将class写成这样：
```c++
class Pinhole2Fisheye : public openMVG::cameras::Pinhole_Intrinsic_Fisheye
{
  using class_type = Pinhole2Fisheye;
    /**
   * @brief Clone the object
   * @return A clone (copy of the stored object)
   */
  Pinhole2Fisheye * clone( void ) const override
  {
    return new class_type( *this );
  }
```

怎么使用呢？
```c++
    Pinhole2Fisheye *cam_ptr;
    cam_ptr = (new Pinhole2Fisheye)->clone();
    cam_ptr->load(archive);
```

### 模型序列化
openMVG 使用 `cereal` 来实现序列化。
例如 `Camera_Intrinsics_ip.hpp`:

```c++ 
#include <cereal/types/polymorphic.hpp>

template <class Archive>
void openMVG::cameras::IntrinsicBase::save( Archive & ar ) const
{
  ar( cereal::make_nvp( "width", w_ ) );
  ar( cereal::make_nvp( "height", h_ ) );
}

template <class Archive>
void openMVG::cameras::IntrinsicBase::load( Archive & ar )
{
  ar( cereal::make_nvp( "width", w_ ) );
  ar( cereal::make_nvp( "height", h_ ) );
}
  
```
和其test文件 `Camera_IO_test.cpp`:

```c++ 
    const std::string filename("camera_io.json");

    // Writing
    {
      std::ofstream stream(filename, std::ios::binary | std::ios::out);
      CHECK(stream.is_open());

      cereal::JSONOutputArchive archive(stream);
      archive(cereal::make_nvp("intrinsics", intrinsic));
    }
    // Reading
    {
      std::ifstream stream(filename, std::ios::binary | std::ios::in);
      CHECK(stream.is_open());

      cereal::JSONInputArchive archive(stream);
      archive(cereal::make_nvp("intrinsics", intrinsic));
    }  
```
注意：
1. 由于写的时候只有 `archive` class析构的时候才会真正进行，因此要把写的过程放到大括号里，读的过程应该同理（未核实）。
2. save 和 load 函数看起来长得一样，实际上传入的 ar 的类型不一样，一个读，一个写。

而`cameras::IntrinsicBase`的子类则比较复杂，因为涉及到多态等问题，因此一般需要显式地告诉cereal你的各个类的继承关系，例如`Camera_Pinhole_Fisheye_io.hpp`中：

```c++ 
#include <cereal/types/polymorphic.hpp>
#include <cereal/types/vector.hpp>

template <class Archive>
inline void openMVG::cameras::Pinhole_Intrinsic_Fisheye::save( Archive & ar ) const
{
    ar(cereal::base_class<Pinhole_Intrinsic>(this));
    ar( cereal::make_nvp( "fisheye", params_ ) );
}

template <class Archive>
inline void openMVG::cameras::Pinhole_Intrinsic_Fisheye::load( Archive & ar )
{
    ar(cereal::base_class<Pinhole_Intrinsic>(this));
    ar( cereal::make_nvp( "fisheye", params_ ) );
}

CEREAL_REGISTER_TYPE_WITH_NAME( openMVG::cameras::Pinhole_Intrinsic_Fisheye, "fisheye" );
CEREAL_REGISTER_POLYMORPHIC_RELATION(openMVG::cameras::IntrinsicBase, openMVG::cameras::Pinhole_Intrinsic_Fisheye)
```
上面，`CEREAL_REGISTER_TYPE_WITH_NAME`就是告诉 cereal 你这个 `Pinhole_Intrinsic_Fisheye` 需要注册一下，还给它一个名字"fisheye"，当然不带名字也可以，`CEREAL_REGISTER_POLYMORPHIC_RELATION(openMVG::cameras::IntrinsicBase, openMVG::cameras::Pinhole_Intrinsic_Fisheye)`就是告诉cereal这个`Pinhole_Intrinsic_Fisheye` 的基类是谁。

我在实现自己的类 `Pinhole2Fisheye` 的时候，还参考了 `Camera_Pinhole_ip.hpp`

```c++ 
template <class Archive>
void openMVG::cameras::Pinhole_Intrinsic::save( Archive & ar ) const
{
    IntrinsicBase::save(ar);
    ar( cereal::make_nvp( "focal_length", K_( 0, 0 ) ) );
    const std::vector<double> pp {K_( 0, 2 ), K_( 1, 2 )};
    ar( cereal::make_nvp( "principal_point", pp ) );
}


/**
* @brief  Serialization in
* @param ar Archive
*/
template <class Archive>
void openMVG::cameras::Pinhole_Intrinsic::load( Archive & ar )
{
    IntrinsicBase::load(ar);
    double focal_length;
    ar( cereal::make_nvp( "focal_length", focal_length ) );
    std::vector<double> pp( 2 );
    ar( cereal::make_nvp( "principal_point", pp ) );
    *this = Pinhole_Intrinsic( w_, h_, focal_length, pp[0], pp[1] );
}

CEREAL_REGISTER_TYPE_WITH_NAME(openMVG::cameras::Pinhole_Intrinsic, "pinhole");
CEREAL_REGISTER_POLYMORPHIC_RELATION(openMVG::cameras::IntrinsicBase, openMVG::cameras::Pinhole_Intrinsic);  
```

不知为何，我没法使用 cereal 官方推荐的 ` ar(cereal::base_class<Pinhole_Intrinsic>(this));` 这种方式进行基类的序列化，只能采用显式的基类save方法：

```c++ 
/**
   * @brief Serialization out
   * @param ar Archive
   */

  template <class Archive>
  inline void save( Archive & ar ) const{
    //ar(cereal::base_class<Pinhole2Fisheye>(this));
    openMVG::cameras::Pinhole_Intrinsic_Fisheye::save(ar);
    ar(cereal::make_nvp("pinhole2fisheye", ori_pinhole_cam));
  }

  /**
   * @brief  Serialization in
   * @param ar Archive
   */
  template <class Archive>
  inline void load( Archive & ar ){
    //ar(cereal::base_class<Pinhole2Fisheye>(this));
    openMVG::cameras::Pinhole_Intrinsic_Fisheye::load(ar);
    ar(cereal::make_nvp("pinhole2fisheye", ori_pinhole_cam));
  } 
  CEREAL_REGISTER_TYPE_WITH_NAME(Pinhole2Fisheye, "pinhole2fisheye");
  CEREAL_REGISTER_POLYMORPHIC_RELATION(openMVG::cameras::Pinhole_Intrinsic_Fisheye, Pinhole2Fisheye);
```
保存好的模型文件长这个样子：
```json 
{
    "value0": {
        "width": 855,
        "height": 665,
        "focal_length": 323.0,
        "principal_point": [
            427.0,
            332.0
        ]
    },
    "fisheye": [
        0.0749,
        -0.00115,
        0.00225,
        -0.001677
    ],
    "pinhole2fisheye": {
        "width": 1280,
        "height": 720,
        "focal_length": 250.0,
        "principal_point": [
            640.0,
            360.0
        ]
    }
}  
```

### `去失真`中的解方程
openMVG用的鱼眼模型和openCV的一样，代码貌似也一样，只是代码更精简而已。
参照：[opencv模型](https://huningxin.github.io/opencv_docs/db/d58/group__calib3d__fisheye.html)。
世界坐标系中的点 `X`，经过 R 和 T之后得到 Xc，即：`Xc = R X + T`
令
$$
x = Xc_1 \\ y = Xc_2 \\ z = Xc_3
$$
那么我们上面提到的camera plane实际上是normalized camera plane，上面的点其实是：
$a = x / z \ and \ b = y / z$

现在回到openMVG的源码`Camera_Pinhole_Fisheye.hpp`，鱼眼相机的 `add_disto` 函数就是简单地在 camera plane 加了一个非线性变换：
1. 首先计算入射角
$$
r^2 = a^2 + b^2 \\ \theta = atan(r)
$$
2. 然后加失真：
$$
\theta_d = \theta (1 + k_1 \theta^2 + k_2 \theta^4 + k_3 \theta^6 + k_4 \theta^8) \\
x' =a (\theta_d / r)  \\ y' = b(\theta_d / r) 
$$

若记 $p=[a,b]$，那么代码为：
```c++ 
    const double r = std::hypot( p(0), p(1) );
    const double theta = std::atan( r ); 
    const double
        theta2 = theta * theta,
        theta3 = theta2 * theta,
        theta4 = theta2 * theta2,
        theta5 = theta4 * theta,
        theta6 = theta3 * theta3,
        theta7 = theta6 * theta,
        theta8 = theta4 * theta4,
        theta9 = theta8 * theta;
      const double theta_dist = theta + k1 * theta3 + k2 * theta5 + k3 * theta7 + k4 * theta9;
      const double inv_r = r > eps ? 1.0 / r : 1.0;
      const double cdist = r > eps ? theta_dist * inv_r : 1.0;
      return  p * cdist;
```


那么怎么进行`去失真`呢？也就是我们已知 $x'$ 和 $y'$，怎么求 $a$ 和 $b$？

显然，由于：
$$
x' =a (\theta_d / r)  \\ y' = b(\theta_d / r)
$$
因此 
$$
\theta_d = \sqrt{x'^2+y'^2} \\
a=\frac{x'}{\theta_d}r=\frac{x'}{\sqrt{x'^2+y'^2}}r=\frac{x'}{\sqrt{x'^2+y'^2}}\tan{\theta} \\
b=\frac{y'}{\theta_d}r=\frac{y'}{\sqrt{x'^2+y'^2}}r=\frac{y'}{\sqrt{x'^2+y'^2}}\tan{\theta}
$$

问题转化为：已知 $\theta_d = \theta (1 + k_1 \theta^2 + k_2 \theta^4 + k_3 \theta^6 + k_4 \theta^8)$ 如何解 $\theta$。


记 $p=[x',y']$，先看代码：
```c++ 
double theta = theta_dist;
for ( int j = 0; j < 10; ++j )
{
    const double
    theta2 = theta * theta,
    theta4 = theta2 * theta2,
    theta6 = theta4 * theta2,
    theta8 = theta6 * theta2;
    theta = theta_dist /
    ( 1 + params_[0] * theta2
    + params_[1] * theta4
    + params_[2] * theta6
    + params_[3] * theta8 );
}
```
很显然就是先给定 $\theta$ 一个初始值 $\theta_d$，然后迭代十次：
$\theta_{i+1}=\frac{\theta_d}{1 + k_1 \theta_{i}^2 + k_2 \theta_{i}^4 + k_3 \theta_{i}^6 + k_4 \theta_{i}^8}$
