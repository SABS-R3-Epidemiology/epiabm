#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <functional>

struct function_converter
{
  /// @note Registers converter from a python callable type to the
  ///       provided type.
  template <typename FunctionSig>
  function_converter&
  from_python()
  {
    boost::python::converter::registry::push_back(
      &function_converter::convertible,
      &function_converter::construct<FunctionSig>,
      boost::python::type_id<boost::function<FunctionSig>>());

    // Support chaining.
    return *this;
  }

  /// @brief Check if PyObject is callable.
  static void* convertible(PyObject* object)
  {
    return PyCallable_Check(object) ? object : NULL;
  }

  /// @brief Convert callable PyObject to a C++ boost::function.
  template <typename FunctionSig>
  static void construct(
    PyObject* object,
    boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    namespace python = boost::python;
    // Object is a borrowed reference, so create a handle indicting it is
    // borrowed for proper reference counting.
    python::handle<> handle(python::borrowed(object));

    // Obtain a handle to the memory block that the converter has allocated
    // for the C++ type.
    typedef boost::function<FunctionSig> functor_type;
    typedef python::converter::rvalue_from_python_storage<functor_type>
                                                                storage_type;
    void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;

    // Allocate the C++ type into the converter's memory block, and assign
    // its handle to the converter's convertible variable.
    new (storage) functor_type(python::object(handle));
    data->convertible = storage;
  }
};
