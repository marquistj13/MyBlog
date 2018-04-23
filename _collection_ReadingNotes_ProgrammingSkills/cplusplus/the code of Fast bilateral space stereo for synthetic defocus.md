---
title:  Fast bilateral-space stereo for synthetic defocus
date:   2018-4-22
---


* content
{:toc}

## main
### 读取图像
这个图像是倆放在一起的那种, `cv::Rect`的用法好奇怪。
```cpp
const std::string image_pair_filename = "../data/middlebury_scenes2006_midd1.jpg";
// load stereo pair
cv::Mat stereo_images[2];
cv::Mat pair_image;
pair_image = cv::imread(image_pair_filename, CV_LOAD_IMAGE_COLOR);

if (pair_image.cols > 0)
{
    stereo_images[0] = pair_image(cv::Rect(0, 0, pair_image.cols >> 1, pair_image.rows)).clone();
    stereo_images[1] = pair_image(cv::Rect(pair_image.cols >> 1, 0, pair_image.cols >> 1, pair_image.rows)).clone();
}
else
{
    std::cout << "failed to load " << image_pair_filename << std::endl;
    return -1;
}

cv::imshow("stereo image pair", pair_image);
cv::waitKey(16);

// convert to gray scale
```

### 转化图像的scale和数值类型
```cpp
cv::Mat input_confidence_fl;
stereo_matcher.get_output().conf_disp_image.convertTo(input_confidence_fl, CV_32FC1, 1.0f / 255.0f);

```

## bilateral_grid_simplified
###  这个用来建立grid
grid矩阵的维度是： $n_vertex\times \n_pixel$， 即对于每一行来说，如果这个pixel属于该行对应的vertex，那么对应的元素就为1.
```cpp
// with this hash function we can convert each 5 dimensional coordinate to 1 unique number
std::int64_t hash_vec[5];
for (int i = 0; i < 5; ++i)
    hash_vec[i] = static_cast<std::int64_t>(std::pow(255, i));

std::unordered_map<std::int64_t /* hash */, int /* vert id */> hashed_coords;
hashed_coords.reserve(w*h);

const unsigned char* pref = (const unsigned char*)reference_yuv.data;
int vert_idx = 0;
int pix_idx = 0;
```
还有下边：
```cpp
std::int64_t coord[5];
coord[0] = x / sigma_spatial;
coord[1] = y / sigma_spatial;
coord[2] = pref[0] / sigma_luma;
coord[3] = pref[1] / sigma_chroma;
coord[4] = pref[2] / sigma_chroma;

// convert the coordinate to a hash value
std::int64_t hash_coord = 0;
for (int i = 0; i < 5; ++i)
    hash_coord += coord[i] * hash_vec[i];
// pixels whom are alike will have the same hash value.
// We only want to keep a unique list of hash values, therefore make sure we only insert
// unique hash values.
auto it = hashed_coords.find(hash_coord);
if (it == hashed_coords.end())
{
    hashed_coords.insert(std::pair<std::int64_t, int>(hash_coord, vert_idx));
    tripletList.push_back(T(vert_idx, pix_idx, 1.0f));
    ++vert_idx;
}
else
{
    tripletList.push_back(T(it->second, pix_idx, 1.0f));

}

pref += 3; // skip 3 bytes (y u v)
++pix_idx;
```

### 建立splate matrix
这个splate matrix的维度为，$n_vertex\times n_vertex$, 用来表明哪些vertex是在一起的，也就是，如果某几个vertex处于各自的邻域内，那么对应的元素就为1.
```cpp
for (int i = 0; i < 5; ++i)
    {
        std::int64_t offset_hash_coord = -1 * hash_vec[i];

        tripletList.clear();
        for (auto it = hashed_coords.begin(); it != hashed_coords.end(); ++it)
        {
            std::int64_t neighb_coord = it->first + offset_hash_coord;
            auto it_neighb = hashed_coords.find(neighb_coord);
            if (it_neighb != hashed_coords.end())
            {
                tripletList.push_back(T(it->second, it_neighb->second, 1.0f));
            }

        }
        mat_b_left.setZero();
        mat_b_left.setFromTriplets(tripletList.begin(), tripletList.end());


        offset_hash_coord = 1 * hash_vec[i];

        tripletList.clear();
        for (auto it = hashed_coords.begin(); it != hashed_coords.end(); ++it)
        {
            std::int64_t neighb_coord = it->first + offset_hash_coord;
            auto it_neighb = hashed_coords.find(neighb_coord);
            if (it_neighb != hashed_coords.end())
            {
                tripletList.push_back(T(it->second, it_neighb->second, 1.0f));
            }

        }
        mat_b_right.setZero();
        mat_b_right.setFromTriplets(tripletList.begin(), tripletList.end());

        mat_blur += mat_b_left;
        mat_blur += mat_b_right;
    }
```

## stereo_matcher_birchfield_tomasi
### 小的blur （滤波啦） boxFilter
```cpp
// a small blur
cv::Mat stereo_filt_images[2];
cv::boxFilter(stereo_images[0], stereo_filt_images[0], -1, cv::Size(2, 2));
cv::boxFilter(stereo_images[1], stereo_filt_images[1], -1, cv::Size(2, 2));
```

### create 和 赋值不是一回事
```cpp
cv::Mat& min_disp_image = current_output.min_disp_image;
    cv::Mat& max_disp_image = current_output.max_disp_image;
    min_disp_image.create(stereo_images[0].rows, stereo_images[0].cols, CV_16SC1);
    max_disp_image.create(stereo_images[0].rows, stereo_images[0].cols, CV_16SC1);
    min_disp_image = cv::Scalar(std::numeric_limits<int16_t>::max());
    max_disp_image = cv::Scalar(-std::numeric_limits<int16_t>::max());
```


### 遍历稀疏矩阵的两层循环
```cpp
for (int vertex_id = 0, vertex_id_end = nb_vertices; vertex_id < vertex_id_end; ++vertex_id)
    {
        int counter = 0;
        int* plookup = &lookup[vertex_id * disparity_range];
        for (Eigen::SparseMatrix<float, Eigen::RowMajor>::InnerIterator it(grid.get_splat_matrix(), vertex_id); it; ++it) // loop through pixels of that vertex
        {
            const int pixel_id = it.index();
            const int pixel_weight = static_cast<int>(it.value());

            int gj = 0;
            for (int j = max_disp_image.at<int16_t>(pixel_id) + 1 - disparity_min; j < disparity_range; ++j)
            {
                gj += pixel_weight;
                plookup[j] += gj;
            }

            gj = 0;
            for (int j = (int)min_disp_image.at<int16_t>(pixel_id) - 1 - disparity_min; j >= 0; --j)
            {
                gj += pixel_weight;
                plookup[j] += gj;
            }

        }

    }
```


## CMakeLists
```
project (fast_bilateral_space_stereo)

cmake_minimum_required(VERSION 3.0)
cmake_policy(VERSION 3.0)

set(CMAKE_CXX_FLAGS   "-std=c++11")             # c++11
set(CMAKE_CONFIGURATION_TYPES Debug Release CACHE TYPE INTERNAL FORCE )

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

find_package(Eigen)
find_package(OpenCV 3)
find_package(Ceres)

# Source files
SET(FAST_BIL_SOURCES
    src/main.cpp
    src/bilateral_grid_simplified.cpp
    src/bilateral_grid_simplified.h
    src/fast_bilateral_solver.cpp
    src/fast_bilateral_solver.h
    src/stereo_matcher_birchfield_tomasi.cpp
    src/stereo_matcher_birchfield_tomasi.h
)

include_directories(${EIGEN_INCLUDE_DIR} ${OpenCV_INCLUDE_DIRS} ${GLOG_INCLUDE_DIR} ${CERES_INCLUDE_DIRS})

# Create the executable
add_executable(fast_bilateral_space_stereo ${FAST_BIL_SOURCES})
if(MSVC)
    set(LINK_LIBRARY ${CERES_LIBRARIES} ${OpenCV_LIBS} ${GLOG_LIBRARIES} shlwapi.lib)
else()
    set(LINK_LIBRARY ${CERES_LIBRARIES} ${OpenCV_LIBS} ${GLOG_LIBRARIES})
endif()
target_link_libraries(fast_bilateral_space_stereo ${LINK_LIBRARY})
```

