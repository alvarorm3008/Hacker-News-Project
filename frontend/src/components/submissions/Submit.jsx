import React, { useState } from "react";
import APIService from "../../services/ApiService";
import Header from "../Header";

const SubmitForm = () => {
  const [formData, setFormData] = useState({
    title: "",
    url: "",
    text: "",
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState("");
  const [apiError, setApiError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setErrors({ ...errors, [name]: null }); // Limpiar errores al escribir
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validación básica
    const newErrors = {};
    if (!formData.title) {
      newErrors.title = "Title is required.";
    }
    if (formData.url && !isValidUrl(formData.url)) {
      newErrors.url = "Invalid URL.";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      const response = await APIService.post("/submit", formData); // Usamos el servicio API
      if (response.status === 201) {
        setSuccessMessage("Submission created successfully!");
        setFormData({ title: "", url: "", text: "" });
        setApiError("");
      } else if (response.status === 200) {
        setSuccessMessage("Submission already exists!");
      } else {
        setApiError("An unexpected error occurred.");
      }
    } catch (error) {
      console.error("API Error:", error);
      setApiError(error.response?.data?.detail || "An error occurred.");
    }
  };

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch (error) {
      return false;
    }
  };

  return (
    <div className="main-container">
      {/* Contenedor del contenido */}
      <div className="container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
            />
            {errors.title && <div className="error">{errors.title}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="url">Url:</label>
            <input
              type="url"
              id="url"
              name="url"
              className="url-input"
              value={formData.url}
              onChange={handleChange}
            />
            {errors.url && <div className="error">{errors.url}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="text">Text:</label>
            <textarea
              name="text"
              rows="4"
              cols="49"
              wrap="virtual"
              value={formData.text}
              onChange={handleChange}
            ></textarea>
          </div>

          <button type="submit">Submit</button>
          <p>
            Leave url blank to submit a question for discussion. If there is no
            url, text will appear at the top of the thread. If there is a url,
            text is optional.
          </p>
        </form>

        {/* Mensajes de éxito o error */}
        {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        {apiError && <p style={{ color: "red" }}>{apiError}</p>}
      </div>
    </div>
  );
};

export default SubmitForm;
